from django.contrib import admin
from .models import Post, Category


@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


admin.site.register(Category)