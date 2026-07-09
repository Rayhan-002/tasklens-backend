from django.db import models
from django.contrib.auth.models import User


class AnnotationImage(models.Model):
    file = models.ImageField(upload_to='annotation_images/')
    filename = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='annotation_images',
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.filename


class Polygon(models.Model):
    image = models.ForeignKey(
        AnnotationImage,
        on_delete=models.CASCADE,
        related_name='polygons',
    )
    label = models.CharField(max_length=100, blank=True, default='')
    # Stored as a JSON array of {x, y} objects, e.g. [{"x": 10, "y": 20}, ...]
    points = models.JSONField(default=list)

    def __str__(self):
        return f'Polygon({self.label}) on {self.image.filename}'
