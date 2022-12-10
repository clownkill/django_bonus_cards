import datetime

from .models import Card

def deactivate_expired_cards():
    expired_cards = Card.objects.filter(finished_at__lte=datetime.datetime.now())
    for card in expired_cards:
        card.is_active = False
