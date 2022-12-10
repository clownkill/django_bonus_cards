import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator,
)


class ExperationPeriod(models.Model):
    experation_period = models.PositiveSmallIntegerField(
        'Срок действия в месяцах',
    )

    class Meta:
        verbose_name = 'Срок действия'
        verbose_name_plural = 'Сроки действия'

    def __str__(self):
        return f'{self.experation_period} месяц (а/ев)'


class Card(models.Model):
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
        null=True,
        blank=True,
        verbose_name='Владелец'
    )
    discount = models.PositiveSmallIntegerField(
        'Процент скидки',
        default=5,
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
    finished_at = models.DateTimeField(
        'Дата окончания действия карты'
    )
    card_experation = models.ForeignKey(
        ExperationPeriod,
        related_name='cards',
        on_delete=models.CASCADE,
        verbose_name='Период действия карты'
    )

    class Meta:
        unique_together = 'series', 'number',
        index_together = 'series', 'number',
        ordering = '-created_at',
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return f'{self.series}{self.number}'

    def save(self, *args, **kwargs):
        print(self.card_experation.experation_period)
        self.finished_at = datetime.datetime.now() + datetime.timedelta(
            days=30 * int(self.card_experation.experation_period)
        )
        super(Card, self).save(*args, **kwargs)



class CardUsageRecord(models.Model):
    card = models.ForeignKey(
        Card,
        related_name='records',
        on_delete=models.CASCADE,
        verbose_name='Карта'
    )
    created_at = models.DateTimeField(
        'Дата использования карты',
        auto_now_add=True
    )
    operation_sum = models.DecimalField(
        'Сумма операции',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01),]
    )
    place = models.CharField(
        'Место совершения операции',
        max_length=200
    )

    class Meta:
        ordering = '-created_at',
        verbose_name = 'Запись о использовании карты'
        verbose_name_plural = 'Записи о использовании карты'

    def __str__(self):
        return f'{self.card.series}{self.card.number} ' \
               f'({self.created_at.strftime("%d.%m.%Y %H:%m")})'
