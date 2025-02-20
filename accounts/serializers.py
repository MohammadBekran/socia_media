from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from .models import Profile

User = get_user_model()


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
    class Meta:
        model = Profile
        fields = ('id', 'first_name',
                  'last_name', 'age', 'bio', 'picture')
