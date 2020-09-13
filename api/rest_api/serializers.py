from rest_framework import serializers
from .models import Image, Annotation


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ['image_id','image_source', 'image_height', 'image_width']
     
class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        # fields = ['annotation_id', 'image_id', 'coordinates_x', 'coordinates_y', 'label']
        fields = '__all__'
