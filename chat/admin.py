from django.contrib import admin
from .models import ChatMessage, ChatRoom

# Register your models here.


class ChatMessageAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sender" or db_field.name == "receiver":
            chat_room_id = request.GET.get("chat_room", None)
            if chat_room_id:
                chat_room = ChatRoom.objects.get(id=chat_room_id)
                kwargs["queryset"] = chat_room.first_user | chat_room.second_user
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(ChatRoom)
