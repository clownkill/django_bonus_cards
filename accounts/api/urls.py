from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('accounts', views.UserViewSet)


app_name = 'accounts'

urlpatterns = [
    path('', include(router.urls)),
]