from django.db import models
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField
import uuid
import cv2
import os
import time


class Image(models.Model):
    image_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    image_height = models.PositiveIntegerField()
    image_width = models.PositiveIntegerField()
    image_source = models.ImageField(upload_to='images', height_field='image_height', width_field='image_width')
    original_image = models.ImageField(upload_to='original_image', null = True, height_field='org_img_height', width_field='org_img_width')
    org_img_width = models.PositiveIntegerField()
    org_img_height = models.PositiveIntegerField()
    
    
class Annotation(models.Model):
    annotation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_id = models.ForeignKey('Image', on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    coordinates_x = ArrayField(models.FloatField(), null = True)
    coordinates_y = ArrayField(models.FloatField(), null = True)
    shape = models.CharField(max_length=255, default="polygon")
    label = models.CharField(max_length=300)
    
    def __str__(self):
        return self.label

def resize(sender, instance, *args, **kwargs):
        if instance.image_source:
            if (min(instance.image_height, instance.image_width)<200):
                dim = None
                if (instance.image_height < 200 and instance.image_width>=instance.image_height):
                    
                    r = float(200/instance.image_height)
                    dim = (int(instance.image_width * r), 200)
                    # instance.original_image = instance.image_source
                    imgUMat = cv2.imread(instance.image_source.path)
                    resized = cv2.resize(imgUMat, dim, interpolation = cv2.INTER_LANCZOS4)
                    cv2.imwrite(instance.image_source.path, resized)
                    instance.image_height = dim[1]
                    instance.image_width = dim[0]
                elif (instance.image_width < 200 and instance.image_height>instance.image_width):
                    r = float(200/instance.image_width)
                    dim = (200,int(instance.image_height*r))
                    # print(dim)
                    # instance.original_image = instance.image_source
                    imgUMat = cv2.imread(instance.image_source.path)
                    resized = cv2.resize(imgUMat, dim, interpolation = cv2.INTER_LANCZOS4)
                    cv2.imwrite(instance.image_source.path, resized)
                    instance.image_height = dim[1]
                    instance.image_width = dim[0]
                instance.save()
            if (max(instance.image_height, instance.image_width)>600):
                dim = None
                print(instance.image_source.path)
                if (instance.image_height > 600 and instance.image_width<=instance.image_height):
                    
                    r = float(600/instance.image_height)
                    dim = (int(instance.image_width * r), 600)
                    # instance.original_image = instance.image_source
                    imgUMat = cv2.imread(instance.image_source.path)
                    instance.image_source = cv2.resize(imgUMat, dim, interpolation = cv2.INTER_LANCZOS4)
                    cv2.imwrite(instance.image_source.path, resized)
                    instance.image_height = dim[1]
                    instance.image_width = dim[0]
                elif (instance.image_width > 600 and instance.image_height<instance.image_width):
                    r = float(600/instance.image_width)
                    dim = (600,int(instance.image_height*r))
                    # instance.original_image = instance.image_source
                    imgUMat = cv2.imread(instance.image_source.path)
                    resized = cv2.resize(imgUMat, dim, interpolation = cv2.INTER_LANCZOS4)
                    cv2.imwrite(instance.image_source.path, resized)
                    instance.image_height = dim[1]
                    instance.image_width = dim[0]
                instance.save()
post_save.connect(resize, sender=Image)
