from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Avatar, Profile


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(required=False, partial=True)

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]

    def update(self, instance, validated_data):
        print("val_data:", validated_data)

        instance.fullName = validated_data.get("fullName", instance.fullName)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.email = validated_data.get("email", instance.email)

        instance.save()

        return instance
