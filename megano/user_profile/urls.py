from django.urls import path, include
from user_profile import views
from .views import SignUpView, SignInView, ProfileView, ProfilePassword, ProfileAvatar

app_name = "user_profile"

urlpatterns = [
    path("sign-up", SignUpView.as_view(), name="register"),
    path("sign-in", SignInView.as_view(), name="login"),
    path("sign-out", views.signOut),
    path("profile", ProfileView.as_view(), name="profile"),
    path("profile/password", ProfilePassword.as_view(), name="profile_password"),
    path("profile/avatar", ProfileAvatar.as_view(), name="profile_avatar"),
]
