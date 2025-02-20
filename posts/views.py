from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Like, Comment, CommentLike
from .serializers import PostCreateSerializer, LikeSerializer, CommentSerializer, CommentLikeSerializer


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filerset_fields = ['user', 'created']
    search_fields = ['title', 'slug', 'body']
    ordering_fields = '__all__'

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            return Post.objects.all()
        return Post.objects.filter(user=self.request.user)


class LikeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        likes = Like.objects.all()
        ser_data = LikeSerializer(instance=likes, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        like = get_object_or_404(Like, pk=kwargs['pk'])
        ser_data = LikeSerializer(instance=like)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        like, created = Like.objects.get_or_create(
            user=request.user, post=post)

        if not created:
            return Response({'detail': 'You already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Post has been liked successfully'})

    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Updating likes is not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'Updating likes is not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        like = Like.objects.filter(user=request.user, post=post)

        if like.exists():
            like.delete()
            return Response({'detail': 'Your like has been deleted succesfully'})

        return Response({'detail': "You haven't like this post"})


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])

        serializer.save(user=self.request.user, post=post)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return Response({'detail': 'You can only delete your comments'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class CommentLikeViewSet(ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])

        serializer.save(user=self.request.user, comment=comment)
        return super().perform_create(serializer)

    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Updating likes is not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'Updating likes is not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
