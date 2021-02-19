from django.contrib import admin
from .models import Photo, InternetImage


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['file_name']


@admin.register(InternetImage)
class InternetImageAdmin(admin.ModelAdmin):
    fields = ('url', )
    readonly_fields = ('url', )
