from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import AnnotationImage, Polygon
from .serializers import AnnotationImageSerializer, PolygonSerializer


class ImageListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        images = (
            AnnotationImage.objects
            .filter(uploaded_by=request.user)
            .prefetch_related('polygons')
        )
        return Response(AnnotationImageSerializer(images, many=True).data)

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'detail': 'No file provided.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        image = AnnotationImage.objects.create(
            file=file,
            filename=file.name,
            uploaded_by=request.user,
        )
        return Response(
            AnnotationImageSerializer(image).data,
            status=status.HTTP_201_CREATED,
        )


class ImageDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        image = get_object_or_404(AnnotationImage, pk=pk, uploaded_by=request.user)
        return Response(AnnotationImageSerializer(image).data)

    def delete(self, request, pk):
        image = get_object_or_404(AnnotationImage, pk=pk, uploaded_by=request.user)
        image.file.delete(save=False)  # remove file from disk
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PolygonListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_image(self, image_pk, user):
        return get_object_or_404(AnnotationImage, pk=image_pk, uploaded_by=user)

    def get(self, request, image_pk):
        image = self._get_image(image_pk, request.user)
        return Response(PolygonSerializer(image.polygons.all(), many=True).data)

    def post(self, request, image_pk):
        image = self._get_image(image_pk, request.user)
        serializer = PolygonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(image=image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PolygonDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, image_pk, pk):
        image = get_object_or_404(AnnotationImage, pk=image_pk, uploaded_by=request.user)
        polygon = get_object_or_404(Polygon, pk=pk, image=image)
        polygon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
