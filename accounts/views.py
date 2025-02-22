from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from social_media.utils import skip_for_swagger
from .models import Profile, Follow
from .serializers import UserProfileUpdateSerializer, FollowSerializer


class UserProfilePagination(PageNumberPagination):
    page_size = 10


class UserProfileUpdateViewSet(ModelViewSet):
    queryset = User.objects.all().select_related(
        'profile').prefetch_related('posts', 'followers', 'followings')
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserProfilePagination

    @skip_for_swagger
    def get_queryset(self):
        if not self.request.user.is_staff and self.request.method == 'GET':
            raise PermissionDenied(
                'You do not have permission to see profiles')
        return Profile.objects.all()


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    @skip_for_swagger
    def get_queryset(self):
        if self.request.method in SAFE_METHODS and not self.request.user.is_staff:
            return Follow.objects.filter(followrs=self.request.user)
        return Follow.objects.all()

    def create(self, request, *args, **kwargs):
        following_user_id = request.data.get('following')
        if not following_user_id:
            return Response({'detail': 'Following is required'}, status=status.HTTP_400_BAD_REQUEST)
        following = get_object_or_404(User, pk=following_user_id)

        if request.user == following:
            return Response({'detail': 'You can not follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(
            follower=request.user, following=following)

        if not created:
            return Response({'detail': 'Your already is following this user'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': f'You are following this user now'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Updating follow is not allowed'})

    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'Updating follow is not allowed'})
