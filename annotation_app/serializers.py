from rest_framework import serializers
from .models import AnnotationImage, Polygon


class PolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polygon
        fields = ['id', 'label', 'points', 'image']
        read_only_fields = ['id', 'image']


class AnnotationImageSerializer(serializers.ModelSerializer):
    polygons = PolygonSerializer(many=True, read_only=True)

    class Meta:
        model = AnnotationImage
        fields = ['id', 'file', 'filename', 'uploaded_at', 'polygons']
        read_only_fields = ['id', 'filename', 'uploaded_at']
