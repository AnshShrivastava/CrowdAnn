from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid


class Image(models.Model):
    image_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    image_height = models.PositiveIntegerField()
    image_width = models.PositiveIntegerField()
    image_source = models.ImageField(upload_to='images', height_field='image_height', width_field='image_width')
    provider_id = models.CharField(max_length=20, null=True)
    aspect_ratio = models.FloatField()
    
    
    

class Annotation(models.Model):
    annotation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_id = models.ForeignKey('Image', on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    coordinates_x = ArrayField(models.IntegerField(), null = True)
    label = models.CharField(max_length=300)
    coordinates_y = ArrayField(models.IntegerField(), null = True)
    def __str__(self):
        return self.label