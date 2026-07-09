from django.contrib import admin
from .models import AnnotationImage, Polygon


@admin.register(AnnotationImage)
class AnnotationImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'uploaded_by', 'uploaded_at')
    search_fields = ('filename',)


@admin.register(Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'image')
    list_filter = ('image',)
    search_fields = ('label',)
