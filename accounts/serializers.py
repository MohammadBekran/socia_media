from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from posts.models import Post, Comment, CommentLike
from .models import Profile, Follow

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    first_name = serializers.CharField(
        source='profile.first_name', read_only=True)
    last_name = serializers.CharField(
        source='profile.last_name', read_only=True)
    age = serializers.IntegerField(source='profile.age', read_only=True)
    picture = serializers.ImageField(
        source='profile.picture', read_only=True)
    posts = serializers.SerializerMethodField()
    liked_posts = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    comment_likes = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'first_name', 'last_name', 'age', 'picture', 'posts', 'liked_posts', 'comments', 'comment_likes', 'followers', 'followings'
        )

    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj)

        return [
            {
                'id': post.id,
                'title': post.title,
                'body': post.body,
                'slug': post.slug,
                'picture': post.picture.url if post.picture else None,
                'created': post.created,
                'updated': post.updated
            }
            for post in posts
        ]

    def get_liked_posts(self, obj):
        liked_posts = Post.objects.filter(likes__user=obj)

        return [{'id': liked_post.id, 'title': liked_post.title} for liked_post in liked_posts]

    def get_comments(self, obj):
        comments = Comment.objects.filter(user=obj)

        return [
            {
                'id': comment.id,
                'post': comment.post.id,
                'body': comment.body,
                'parent': comment.parent.id if comment.parent else None,
                'created': comment.created,
                'updated': comment.updated
            }
            for comment in comments
        ]

    def get_comment_likes(self, obj):
        comment_likes = CommentLike.objects.filter(user=obj)

        return [
            {
                'id': comment_like.id,
                'comment': comment_like.comment.id,
                'created': comment_like.created,
                'updated': comment_like.updated
            }
            for comment_like in comment_likes
        ]

    def get_followers(self, obj):
        followers = Follow.objects.filter(following=obj)

        return [
            {
                'id': follower.id,
                'follower': follower.follower.id,
                'following': follower.following.id,
                'created': follower.created
            }
            for follower in followers
        ]

    def get_followings(self, obj):
        followings = Follow.objects.filter(follower=obj)

        return [
            {
                'id': following.id,
                'follower': following.follower.id,
                'following': following.following.id,
                'created': following.created
            }
            for following in followings
        ]


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
    posts = serializers.SerializerMethodField()
    liked_posts = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    comment_likes = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'id', 'first_name', 'last_name', 'age', 'bio', 'picture',
            'posts', 'liked_posts', 'comments', 'comment_likes',
            'followers', 'followings'
        )

    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj.user)

        return [
            {
                'id': post.id,
                'title': post.title,
                'body': post.body,
                'slug': post.slug,
                'picture': post.picture.url if post.picture else None,
                'created': post.created,
                'updated': post.updated
            }
            for post in posts
        ]

    def get_liked_posts(self, obj):
        liked_posts = Post.objects.filter(likes__user=obj.user)

        return [{'id': liked_post.id, 'title': liked_post.title} for liked_post in liked_posts]

    def get_comments(self, obj):
        comments = Comment.objects.filter(user=obj.user)

        return [
            {
                'id': comment.id,
                'post': comment.post.id,
                'body': comment.body,
                'parent': comment.parent.id if comment.parent else None,
                'created': comment.created,
                'updated': comment.updated
            }
            for comment in comments
        ]

    def get_comment_likes(self, obj):
        comment_likes = CommentLike.objects.filter(user=obj.user)

        return [
            {
                'id': comment_like.id,
                'comment': comment_like.comment.id,
                'created': comment_like.created,
                'updated': comment_like.updated
            }
            for comment_like in comment_likes
        ]

    def get_followers(self, obj):
        followers = Follow.objects.filter(following=obj.user)

        return [
            {
                'id': follower.id,
                'follower': follower.follower.id,
                'following': follower.following.id,
                'created': follower.created
            }
            for follower in followers
        ]

    def get_followings(self, obj):
        followings = Follow.objects.filter(follower=obj.user)

        return [
            {
                'id': following.id,
                'follower': following.follower.id,
                'following': following.following.id,
                'created': following.created
            }
            for following in followings
        ]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'created')
        extra_kwargs = {
            'follower': {'required': False}
        }
