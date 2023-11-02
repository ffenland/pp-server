from django.contrib import admin
from .models import PostRecord, ReplyRecord, ResumeLike

# Register your models here.


admin.site.register(PostRecord)
admin.site.register(ReplyRecord)
admin.site.register(ResumeLike)
