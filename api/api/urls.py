from django.contrib import admin
from django.urls import path, include
from rest_api.views import ImageView, AnnotationView, RetrieveAnnotationView, RetrieveImageView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions

from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('annotation/save',AnnotationView.as_view()),
    path('image',ImageView.as_view()),
    path('db/images/', RetrieveImageView.as_view()),
    path('db/annotation', RetrieveAnnotationView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


