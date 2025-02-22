from rest_framework import serializers
from .models import Post, Like, Comment, CommentLike, Save


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    saves = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'body',
                  'slug', 'picture', 'likes', 'saves', 'comments')
        extra_kwargs = {
            'slug': {'required': False},
            'user': {'read_only': True},
            'slug': {'read_only': True}
        }

    def get_likes(self, obj):
        likes = Like.objects.filter(post=obj)

        return [
            {
                'id': like.id,
                'user': like.user.id,
                'created': like.created
            }
            for like in likes
        ]

    def get_saves(self, obj):
        saves = Save.objects.filter(post=obj)

        return [
            {
                'id': save.id,
                'user': save.user.id,
                'created': save.created
            }
            for save in saves
        ]

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj)

        return [
            {
                'id': comment.id,
                'body': comment.body,
                'user': comment.user.id,
                'post': comment.post.id,
                'parent': comment.parent.id if comment.parent else None,
                'comment_likes': [
                    {
                        'id': comment_like.id,
                        'user': comment_like.user.id,
                        'created': comment_like.created,
                    }
                    for comment_like in comment.comment_likes.all()
                ],
                'created': comment.created

            }
            for comment in comments
        ]


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ('id', 'user', 'post')

    def get_user(self, obj):
        if obj.user:
            return {
                'id': obj.user.id,
                'username': obj.user.username,
            }
        else:
            return None

    def get_post(self, obj):
        post = obj.post

        return {
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'body': post.body
        }


class CommentSerializer(serializers.ModelSerializer):
    comment_likes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'parent', 'body',
                  'comment_likes', 'created', 'updated')
        extra_kwargs = {
            'user': {'read_only': True},
            'post': {'read_only': True}
        }

    def get_comment_likes(self, obj):
        comment_likes = CommentLike.objects.filter(comment=obj)

        return [
            {
                'id': comment_like.id,
                'user': comment_like.user.id,
                'created': comment_like.created
            }
            for comment_like in comment_likes
        ]


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ('id', 'user', 'comment')
        extra_kwargs = {
            'user': {'read_only': True},
            'comment': {'read_only': True}
        }


class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Save
        fields = ('id', 'user', 'post', 'created')
        extra_kwargs = {
            'user': {'read_only': True},
            'post': {'read_only': True}
        }
