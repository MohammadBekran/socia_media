from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostCreateSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return Post.objects.filter(user=self.request.user)
        return Post.objects.all()
