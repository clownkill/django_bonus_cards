import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator,
)


class Card(models.Model):
    CARD_EXPERATION = (
        ('1', '1 Месяц'),
        ('6', '6 Месяцев'),
        ('12', '12 Месяцев'),
    )

    series = models.CharField(
        'Серия карты',
        max_length=4,
        validators=[
            RegexValidator(
                regex='[A-Z]{4}',
                message='Серия карты должна содержать 4 латинских символа в верхнем регистре'
            )
        ]
    )
    number = models.PositiveSmallIntegerField('Номер карты')
    owner = models.ForeignKey(
        User,
        related_name='cards',
        on_delete=models.CASCADE,
        verbose_name='Владелец'
    )
    discount_amount = models.PositiveSmallIntegerField(
        'Процент скидки',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    is_active = models.BooleanField(
        'Карта активна?',
        default=False
    )
    created_at = models.DateTimeField(
        'Дата создания карты',
        auto_now_add=True
    )
    card_experation = models.CharField(
        'Срок действия',
        max_length=15,
        choices=CARD_EXPERATION,
        default='1'
    )

    class Meta:
        unique_together = 'series', 'number',
        index_together = 'series', 'number',
        ordering = '-created_at',
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return f'{self.series}{self.number} - {self.owner}'

    def finished_at(self):
        return self.created_at + datetime.timedelta(
            days=30 * int(self.card_experation)
        )
