from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework import views
from .serializers import ImageSerializer, AnnotationSerializer
from .models import Image, Annotation
from scipy.spatial import distance
import json


def scale_image( height, width, canvas_size,x,y):
    origin      =(canvas_size[0][0],canvas_size[0][1], 0)
    right_bottom=(canvas_size[1][0], canvas_size[1][1], 0)
    left_top    =(canvas_size[2][0],canvas_size[2][1], 0)
        
    length_str=distance.euclidean(origin,right_bottom)/width
    width_str=distance.euclidean(origin,left_top)/height
        
    actual_x=(distance.euclidean(origin,x)/length_str)
    actual_y=(distance.euclidean(origin,y)/width_str)
        
    return actual_x,actual_y

def get_image(request):
    id = int(request.GET.get('id'))
    annotated_images = Annotation.objects.all()
    images = Image.objects.exclude(image_id__in = annotated_images)
    serializer = ImageSerializer(data =images, many= True)
    serializer.is_valid()
    list_size = images.count()
    if id >= list_size:
        id = id%list_size
    return JsonResponse(serializer.data[id], safe=False)
         
class AnnotationView(views.APIView):
    model = Image, Annotation
    serializer = ImageSerializer, AnnotationSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            # post_data = json.loads(request.body.decode("utf-8"))
            post_data = request.data
            # print(post_data)
            if post_data == '':
                print("No Data Provided")
            result = {}
            if request.method == 'POST':
                
                canvas_size = post_data['canvas_size']
                x_cor = post_data['x_cor']
                y_cor = post_data['y_cor']
                newCoordinates_x = []
                newCoordinates_y = []
                images = Image.objects.get(pk=post_data['image_id'])
                # print(images.image_id)
                for i, j in zip(x_cor, y_cor):
                    x, y = scale_image(images.image_height, images.image_width, canvas_size, i, j)
                    newCoordinates_x.append(x)
                    newCoordinates_y.append(y)
                new_annotation = Annotation()
                new_annotation.image_id = images
                new_annotation.label = post_data['label']
                new_annotation.user = 'abcd'
                new_annotation.coordinates_x = newCoordinates_x
                new_annotation.coordinates_y = newCoordinates_y
                new_annotation.save()
                result['status'] = True
                return JsonResponse(result, safe=False)
        except:
            result['status'] = False
            return JsonResponse(result, safe=False)
