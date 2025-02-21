from django.contrib import admin
from .models import Post, Like, Comment, CommentLike, Save


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'user', 'picture', 'created', 'updated')
    autocomplete_fields = ('user',)
    prepopulated_fields = {
        'slug': ('title',)
    }
    search_fields = ('title',)


@admin.register(Save)
class SaveAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created')
    autocomplete_fields = ('user', 'post')


admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(CommentLike)
