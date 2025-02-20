from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import SAFE_METHODS
from .models import Post
from .serializers import PostCreateSerializer


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
