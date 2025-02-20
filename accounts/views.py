from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import UserProfileUpdateSerializer


class UserProfieUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        ser_data = UserProfileUpdateSerializer(
            instance=profile, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
