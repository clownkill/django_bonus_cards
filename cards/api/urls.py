from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('cards', views.CardViewSet)

app_name = 'cards'

urlpatterns = [
    path('', include(router.urls)),
    path(
        'cards/<pk>/<str:place>/<str:sum>/',
        views.CardViewSet.as_view({'post': 'record'}),
        name='add_record'
    ),
]