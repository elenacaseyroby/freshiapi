from django.contrib import admin

from .models import Nutrient, Unit, UnitConversion


@admin.register(Nutrient)
class NutrientAdmin(admin.ModelAdmin):
    list_display = ['name', 'dv_qty', 'dv_unit', 'usda_nutrient_id']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbr']


@admin.register(UnitConversion)
class UnitConversionAdmin(admin.ModelAdmin):
    list_display = ['from_unit', 'to_unit', 'qty_conversion_coefficient']
