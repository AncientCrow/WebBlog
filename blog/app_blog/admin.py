from django.contrib import admin
from app_blog import models


@admin.register(models.Post)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'published', 'status')
    list_filter = ('created', 'status')
    search_fields = ('title', 'text')
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('title',)}
