from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models import Q,F
from django.utils.dateformat import DateFormat
from django.core.cache import cache

import traceback
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.pagination import PageNumberPagination
from collections import defaultdict
import traceback
from .models import Post, Reply
from .serializers import (
    PostListSerializer,
    PostSerializer,
    ReplySerializer,
    PostCreateSerializer,
)
from medias.models import Photo


class PostListPagination(PageNumberPagination):
    page_size = 10  # 페이지 당 아이템 수 설정
    page_size_query_param = "pg"  # 페이지 크기를 변경할 수 있는 쿼리 매개변수 설정
    max_page_size = 1000  # 최대 페이지 크기 설정


class PostListView(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = PostListSerializer
    pagination_class = PostListPagination

    def get_queryset(self):
        kind = self.request.query_params.get("kind", None)
        if (kind == "cist" and self.request.user.is_owner):
            return []
        if (kind == "owner" and not self.request.user.is_owner):
            return []
        if kind:
            queryset =  Post.objects.filter(kind=kind)
            queryset = queryset.order_by("-created_at")
            return queryset
        else:
            return []
        


class PostCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostCreateSerializer

    def create_post_photo(self, user, cf_id, description, post):
        Photo.objects.create(
            cf_id=cf_id,
            uploader=user,
            description=description,
            post=post,
        )

    def create(self, request):
        create_data = {
            "kind": request.data.get("kind"),
            "title": request.data.get("title"),
            "article": request.data.get("article"),
            "user": request.user.id,
        }
        serializer = self.get_serializer(data=create_data)
        if serializer.is_valid():
            post = serializer.save()
            # 이미지 업로드 처리
            image_list = request.data.get("image")
            if image_list:
                for image in image_list:
                    self.create_post_photo(
                        user=request.user,
                        cf_id=image,
                        description="",
                        post=post,
                    )

            return Response(
                {"ok": True, "data": serializer.data},
                status=HTTP_201_CREATED,
            )
        else:
            traceback.print_exc()  # Print traceback
            print(serializer.errors)
            return Response({"ok":False, "data":{"erm":serializer.errors}}, status=HTTP_400_BAD_REQUEST)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer

    def get_object(self, pk):
        try:
            post = Post.objects.get(pk=pk)
            return post
        except Post.DoesNotExist:
            raise NotFound

    def retrieve(self, request, pk):
        post = self.get_object(pk=pk)
        user_id = request.user.id

        # CacheKey Create
        cache_key = f"post_view_{post.id}_by_{user_id}"

        if not cache.get(cache_key):
            post.view_count += 1
            post.save()
            cache.set(cache_key, True, 60 * 5)
        serializer = PostSerializer(post)
        return Response({"ok": True, "data": serializer.data})

    def update(self, request, pk):
        post = self.get_object(pk=pk)

        # 현재 로그인한 유저와 Post의 user가 일치하는지 확인
        if request.user != post.user:
            return Response(
                {"error": "You do not have permission to update this post."}, status=403
            )

        serializer = PostSerializer(
            post,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"ok": True, "data": serializer.data})
        return Response(serializer.errors, status=400)


class PostCountView(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return False
    def get(self, request, pk):
        post = self.get_object(pk=pk)
        if post:
            return Response({"ok":True, "data":{"count":post.view_count}})
    def put(self, request, pk):
        post = self.get_object(pk=pk)
        if not post:
            return Response({"ok":False}, status=HTTP_400_BAD_REQUEST)
        post.update(view_count=F("view_count")+1)
        return Response({"ok":True}, status=HTTP_202_ACCEPTED)
        
class ReplyView(APIView):
    def get_object(self, pk):
        try:
            post = Post.objects.get(pk=pk)
            return post
        except Post.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        post = self.get_object(pk=pk)
        replys = Reply.objects.filter(post=post).order_by("-created_at")
        serializer = ReplySerializer(
            replys,
            many=True,
        )
        return Response({"ok": True, "data": serializer.data})
