from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/update/', views.UserProfieUpdateView.as_view(),
         name='profile_update')
]
