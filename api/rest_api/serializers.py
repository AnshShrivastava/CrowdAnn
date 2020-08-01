from rest_framework import serializers
from .models import Image, Annotation


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ['image_id','image_source',]
     
class AnnotationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Annotation
        fields = ['annotation_id', 'image_id', 'coordinates', 'label']