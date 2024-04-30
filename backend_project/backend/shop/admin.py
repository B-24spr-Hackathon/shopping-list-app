from django.contrib import admin
from .models import User, List, Member, Item

# Register your models here.

admin.site.register(User)
admin.site.register(List)
admin.site.register(Member)
admin.site.register(Item)


