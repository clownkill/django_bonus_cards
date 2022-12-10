from django.contrib import admin
from babel.dates import format_date

from .models import Card, CardUsageRecord, ExperationPeriod


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    readonly_fields = ('formatted_started_at', 'formatted_finished_at',)
    list_display = (
        'card',
        'owner',
        'formatted_started_at',
        'formatted_finished_at',
        'is_active',
    )
    list_filter = ('owner', 'is_active')
    search_fields = (
        'series',
        'number',
        'created_at',
        'is_active',
    )

    fieldsets = (
        (None, {
            'fields': (
                ('series', 'number', 'is_active',),
                ('owner', 'discount',),
            )
        }),
        (None, {
            'fields':(
                ('card_experation', 'formatted_started_at', 'formatted_finished_at',),
            ),
        })
    )

    @admin.display(description='Дата начала действия карты')
    def formatted_started_at(self, obj):
        return format_date(obj.created_at, 'E, d MMMM yyyy', locale='ru')

    @admin.display(description='Дата окончания действия карты')
    def formatted_finished_at(self, obj):
        if obj.created_at:
            return format_date(obj.finished_at, 'E, d MMMM yyyy', locale='ru')

    @admin.display(description='Карта')
    def card(self, obj):
        if obj.created_at:
            return f'{obj.series}{obj.number}'


@admin.register(CardUsageRecord)
class CardUsageRecordAdmin(admin.ModelAdmin):
    list_display = ('card', 'place', 'created_at', 'operation_sum', 'discount_amount')
    list_filter = ('card', 'created_at',)
    readonly_fields = ('created_at', 'discount_amount',)

    @admin.display(description='Сумма скидки')
    def discount_amount(self, obj):
        if obj.created_at:
            return obj.operation_sum * obj.card.discount / 100


@admin.register(ExperationPeriod)
class ExperationPeriodAdmin(admin.ModelAdmin):
    pass
