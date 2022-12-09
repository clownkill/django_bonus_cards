import datetime

from django.contrib import admin
from babel.dates import format_date

from .models import Card


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
                ('owner', 'discount_amount',),
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
        if obj.owner:
            # created_at = obj.created_at
            # finished_at = created_at + datetime.timedelta(days=30 * int(obj.card_experation))
            return format_date(obj.finished_at(), 'E, d MMMM yyyy', locale='ru')

    @admin.display(description='Карта')
    def card(self, obj):
        if obj.owner:
            return f'{obj.series}{obj.number}'

