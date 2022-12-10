from rest_framework import serializers

from ..models import Card, CardUsageRecord, ExperationPeriod


class CardUsageRecordSerializer(serializers.ModelSerializer):
     class Meta:
        model = CardUsageRecord
        fields = [
            'operation_sum',
            'created_at',
            'place',
        ]


class ExperationPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperationPeriod
        fields = [
            'experation_period',
        ]


class CardSerializer(serializers.ModelSerializer):
    records = CardUsageRecordSerializer(many=True, read_only=True)
    card_experation = ExperationPeriodSerializer()
    class Meta:
        model = Card
        fields = [
            'id',
            'series',
            'number',
            'owner',
            'discount',
            'is_active',
            'created_at',
            'card_experation',
            'records',
        ]