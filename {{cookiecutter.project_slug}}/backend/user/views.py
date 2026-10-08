from django.shortcuts import get_object_or_404

from rest_framework.generics import RetrieveAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import User
from user.serializers import LoginSerializer, UserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class MeView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        # Auth is stateless: request.user is a TokenUser built from the JWT, so load the real row.
        return get_object_or_404(User, pk=self.request.user.id)
