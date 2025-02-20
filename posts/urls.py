from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.PostViewSet, basename='posts')

post_likes_router = NestedDefaultRouter(router, '', lookup='post')
post_likes_router.register('likes', views.LikeViewSet, basename='post-likes')

post_comments_router = NestedDefaultRouter(router, '', lookup='post')
post_comments_router.register(
    'comments', views.CommentViewSet, basename='post-comments')

post_comment_likes_router = NestedDefaultRouter(
    post_comments_router, 'comments', lookup='comment')
post_comment_likes_router.register(
    'likes', views.CommentLikeViewSet, basename='comment-likes')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(post_comments_router.urls)),
    path('', include(post_comment_likes_router.urls)),
    path('', include(post_likes_router.urls))
]
