import random
import string
from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from ..models import Card, CardUsageRecord, ExperationPeriod
from .serializers import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    @action(detail=True,
            methods=['post'],
            url_path='<str:place>/<str:sum>',
            authentication_classes=[BasicAuthentication,],
            permission_classes=[IsAuthenticated,])
    def record(self, request, *args, **kwargs):
        record = CardUsageRecord.objects.create(
            card=get_object_or_404(Card, pk=kwargs['pk']),
            operation_sum=Decimal(kwargs['sum']),
            place=kwargs['place']
        )
        return Response({'record_created': True})

@transaction.atomic
@api_view(['POST'])
def generate_cards(request, count, experation):
    for _ in range(count):
        card = Card.objects.create(
            series=''.join(
                [random.choice(string.ascii_uppercase) for _ in range(4)]
            ),
            number=random.randint(1000000000, 9999999999),
            card_experation=get_object_or_404(
                                ExperationPeriod,
                                experation_period=experation
                            )
        )
        card.save()

    return Response(
        {'created': True}
    )

