from django.contrib import admin
from .models import Category,SubCategory, Patch, PatchPermissions

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Patch)
admin.site.register(PatchPermissions)
