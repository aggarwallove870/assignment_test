from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Tag)
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Like)