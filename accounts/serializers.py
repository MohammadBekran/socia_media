from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from posts.models import Post
from .models import Profile

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    liked_posts = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('liked_posts',)

    def get_liked_posts(self, obj):
        liked_posts = Post.objects.filter(likes__user=obj)

        return [{'id': liked_post.id, 'title': liked_post.title} for liked_post in liked_posts]


class CustomUserCreateSerializer(UserCreateSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email',
                  'password', 'password2', 'first_name', 'last_name')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match')
        return data

    def validate_email(self, value):
        user = User.objects.filter(email=value).exists()

        if user:
            raise serializers.ValidationError(
                'This user has been taken before')
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        return super().create(validated_data)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name',
                  'last_name', 'age', 'bio', 'picture')
