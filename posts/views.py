from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models import Q
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
from .models import Post, Reply
from .serializers import (
    PostListSerializer,
    PostSerializer,
    ReplySerializer,
    POSTCreateSerializer,
)


class PostListPagination(PageNumberPagination):
    page_size = 10  # 페이지 당 아이템 수 설정
    page_size_query_param = "pg"  # 페이지 크기를 변경할 수 있는 쿼리 매개변수 설정
    max_page_size = 1000  # 최대 페이지 크기 설정


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    pagination_class = PostListPagination

    def get_queryset(self):
        kind_param = self.request.query_params.get("kind", None)
        valid_choices = [choice[0] for choice in Post.PostKindChoices.choices]
        kind = kind_param if kind_param in valid_choices else None
        queryset = Post.objects.all()
        if kind:
            queryset = queryset.filter(kind=kind)
        queryset = queryset.order_by("-created_at")
        return queryset


class PostCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = POSTCreateSerializer


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

    def post(self, request, pk):
        # pk=post_pk
        pass
