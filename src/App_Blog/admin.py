from django.contrib import admin
from App_Blog.models import Blog, Comment, like

# Register your models here.

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(like)
