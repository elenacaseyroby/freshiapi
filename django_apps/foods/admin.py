from django.contrib import admin

from .models import (
    Nutrient, Unit, UnitConversion, Food, NutritionFact, NutrientHealthBenefit,
    HealthBenefit
)


class NutrientHealthBenefitInline(admin.TabularInline):
    model = NutrientHealthBenefit
    extra = 0

    fields = (
        'nutrient',
    )


@admin.register(HealthBenefit)
class HealthBenefit(admin.ModelAdmin):
    fields = ('description', )
    inlines = [NutrientHealthBenefitInline, ]


@admin.register(Nutrient)
class NutrientAdmin(admin.ModelAdmin):
    fields = ('name', 'dv_qty', 'dv_unit')
    exclude = ['usdanutrients']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    fields = ('name', 'abbr')


@admin.register(UnitConversion)
class UnitConversionAdmin(admin.ModelAdmin):
    fields = ('from_unit', 'to_unit', 'qty_conversion_coefficient')


class NutritionFactInline(admin.TabularInline):
    model = NutritionFact
    extra = 0

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
        'nutrient_qty',
        'nutrient_unit',
        'nutrient_dv_qty',
        'nutrient_dv_unit',
        'dv_percent'
    )
    readonly_fields = (
        'nutrient',
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

    def one_serving(self, obj):
        if obj.one_serving_description:
            return obj.one_serving_description
        qty = obj.one_serving_qty or ''
        unit = obj.one_serving_unit or ''
        return f'{qty} {unit}'

    fields = ('name', 'usdacategory', 'one_serving',)
    readonly_fields = ('one_serving',)
    search_fields = ['name', ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
