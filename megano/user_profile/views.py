from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from rest_framework import status, request, permissions
from rest_framework.response import Response
import json
from rest_framework.views import APIView

from user_profile.models import Profile, Avatar

from user_profile.serializers import ProfileSerializer


class SignInView(APIView):
    def post(self, request):
        user_data = json.loads(request.body)
        username = user_data.get("username")
        password = user_data.get("password")

        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    def post(self, request):
        user_data = json.loads(request.body)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")
        print(user_data)

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, fullName=name)
        print(user)
        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def signOut(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)

        print("serial_data:", serializer.data)

        return Response(serializer.data)

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        print("seria:", serializer)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilePassword(APIView):
    def post(self, request):
        password_data = request.data
        current_password = password_data.get("currentPassword")
        new_password = password_data.get("newPassword")
        print(current_password)
        print(new_password)

        if new_password != current_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return Response(status=status.HTTP_201_CREATED)


class ProfileAvatar(APIView):
    def post(self, request):
        file = request.FILES["avatar"]
        avatar = Avatar()
        avatar.src = file
        profile = Profile.objects.get(user=request.user.id)
        print(avatar.src)
        print(file)
        print("info: ", profile, profile.fullName, profile.avatar)

        file_name = "avatar_user_id_{user_id}".format(user_id=profile.pk)
        avatar.alt = file_name

        print("avatar_alt: ", avatar.alt)

        avatar.save()

        print("avatar_pk:", avatar.pk)

        profile.avatar = avatar

        profile.save()
        return Response(status=status.HTTP_201_CREATED)
