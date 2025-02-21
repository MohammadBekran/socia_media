from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from . import views

app_name = 'accounts'

router = DefaultRouter()
router.register(
    'profile', views.UserProfileUpdateViewSet, basename='profile')
router.register('follow', views.FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls))
]
