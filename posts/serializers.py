from django.utils.text import slugify
from rest_framework import serializers
from .models import Post, Like, Comment, CommentLike


class PostCreateSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'body',
                  'slug', 'total_likes', 'picture')
        extra_kwargs = {
            'slug': {'required': False},
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)

    def get_total_likes(self, obj):
        likes = Like.objects.filter(post=obj)

        return likes.count()


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ('id', 'user', 'post')

    def get_user(self, obj):
        user = obj.user

        return {
            'id': user.id,
            'username': user.username,
        }

    def get_post(self, obj):
        post = obj.post

        return {
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'body': post.body
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'parent', 'body', 'created', 'updated')
        extra_kwargs = {
            'user': {'read_only': True},
            'post': {'read_only': True}
        }


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ('id', 'user', 'comment')
        extra_kwargs = {
            'user': {'read_only': True},
            'comment': {'read_only': True}
        }
