from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=8, required=True)
    password2 = serializers.CharField(write_only=True, min_length=8, required=True)
    phone_number = serializers.CharField(required=True)
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone_number", "password1", "password2", "profile_image"]

    def validate(self, data):
        """Check password match and add security checks"""
        password1 = data.get("password1")
        password2 = data.get("password2")

        if password1 != password2:
            raise serializers.ValidationError({"password": "Passwords do not match!"})

        if len(password1) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long!"})

        return data

    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2")  # Remove password2 from validated data

        user = User.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            password=password
        )

        # Create UserProfile
        UserProfile.objects.create(
            user=user,
            phone_number=validated_data["phone_number"],
            image=validated_data.get("profile_image")
        )

        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["phone_number", "role", "balance", "image", "is_email_verified"]
