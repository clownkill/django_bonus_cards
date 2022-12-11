from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .serializers import UserSerializer
from .permissions import UserPermission

UserModel = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = UserPermission,