from rest_framework import serializers
from django.contrib.auth import get_user_model

from cards.api.serializers import CardSerializer

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    cards = CardSerializer(many=True, read_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = UserModel
        fields = [
            'id',
            'username',
            'password',
            'cards',
        ]
