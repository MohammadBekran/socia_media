from django.contrib import admin
from .models import Post, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'user', 'picture', 'created', 'updated')
    autocomplete_fields = ('user',)
    prepopulated_fields = {
        'slug': ('title',)
    }


admin.site.register(Like)
