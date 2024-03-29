from django.contrib import admin

from .models import (
    Nutrient, Unit, UnitConversion, Food, NutritionFact, NutrientHealthBenefit,
    HealthBenefit, USDACategory,
)
from django_admin_inline_paginator.admin import TabularInlinePaginated

from backend.settings import BASE_DIR


class HealthBenefitNutrientInline(admin.TabularInline):
    model = NutrientHealthBenefit
    extra = 0

    fields = (
        'nutrient',
    )


class FoodInline(TabularInlinePaginated):
    model = Food
    extra = 0
    per_page = 30
    show_change_link = True
    fields = (
        'name',
    )
    readonly_fields = (
        'name',
    )


class NutrientHealthBenefitInline(admin.TabularInline):
    model = NutrientHealthBenefit
    extra = 0

    fields = (
        'health_benefit',
    )


@admin.register(HealthBenefit)
class HealthBenefit(admin.ModelAdmin):
    fields = ('description', )
    inlines = [HealthBenefitNutrientInline, ]


@admin.register(USDACategory)
class USDACategory(admin.ModelAdmin):
    fields = ('name', )
    readonly_fields = ('name', )
    inlines = [FoodInline, ]


@admin.register(Nutrient)
class NutrientAdmin(admin.ModelAdmin):
    fields = ('name', 'dv_qty', 'dv_unit')
    exclude = ['usdanutrients']
    inlines = [NutrientHealthBenefitInline, ]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    fields = ('name', 'abbr')


@admin.register(UnitConversion)
class UnitConversionAdmin(admin.ModelAdmin):
    fields = ('from_unit', 'to_unit', 'qty_conversion_coefficient')


class NutritionFactInline(admin.TabularInline):
    model = NutritionFact
    extra = 0

    def usdanutrient_ids(self, obj):
        label = ''
        for index, nid in enumerate(obj.nutrient.usdanutrient_ids):
            label = (
                f'{label}, {nid}'
                if index != 0 else
                str(nid)
            )
        return label

    # custom fields must be in readonly_fields

    def dv_percent(self, obj):
        if not obj.nutrient.dv_qty:
            return '--'
        food_nutrient_qty = float(obj.nutrient_qty)
        nutrient_dv_qty = float(obj.nutrient.dv_qty)
        percent = str(round(food_nutrient_qty / nutrient_dv_qty) * 100)
        return f'{percent}%'

    # custom fields must be in readonly_fields
    def nutrient_unit(self, obj):
        if not obj.nutrient.dv_unit:
            return '--'
        return obj.nutrient.dv_unit.abbr

    # custom fields must be in readonly_fields
    def nutrient_dv_qty(self, obj):
        if not obj.nutrient.dv_qty:
            return '--'
        return obj.nutrient.dv_qty

    # custom fields must be in readonly_fields
    def nutrient_dv_unit(self, obj):
        if not obj.nutrient.dv_unit:
            return '--'
        return obj.nutrient.dv_unit.abbr

    fields = (
        'nutrient',
        'usdanutrient_ids',
        'nutrient_qty',
        'nutrient_unit',
        'nutrient_dv_qty',
        'nutrient_dv_unit',
        'dv_percent'
    )
    readonly_fields = (
        'usdanutrient_ids',
        'nutrient_unit',
        'nutrient_dv_qty',
        'nutrient_dv_unit',
        'dv_percent'
    )


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    inlines = [
        NutritionFactInline,
    ]

    def fdc_ids(self, obj):
        label = ''
        for index, usdafood in enumerate(obj.usdafoods.all()):
            label = (
                f'{label}, {usdafood.fdc_id}'
                if index != 0 else
                str(usdafood.fdc_id)
            )
        return label

    def one_serving(self, obj):
        if obj.one_serving_description:
            return obj.one_serving_description
        qty = obj.one_serving_qty or ''
        unit = obj.one_serving_unit or ''
        return f'{qty} {unit}'

    fields = ('name', 'id', 'usdacategory',
              'one_serving', 'upc_code', 'fdc_ids', )
    readonly_fields = ('id', 'one_serving', 'fdc_ids', )
    search_fields = ['name', ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
