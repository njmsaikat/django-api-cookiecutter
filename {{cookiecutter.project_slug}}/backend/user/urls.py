from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from user.views import LoginView, MeView

urlpatterns = [
    # POST {username, password} -> {access, refresh}
    path("login/", LoginView.as_view(), name="user_login"),
    # POST {refresh} -> {access, refresh}
    path("token/refresh/", TokenRefreshView.as_view(), name="user_token_refresh"),
    # GET -> the authenticated user
    path("me/", MeView.as_view(), name="user_me"),
]
