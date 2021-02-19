from django.contrib import admin

from .models import Nutrient, Unit, UnitConversion


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
