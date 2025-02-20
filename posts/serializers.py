from django.utils.text import slugify
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post


class PostListserializsr(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'slug', 'body', 'slug', 'picture')


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'body', 'slug', 'picture')
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
