from django.conf.urls import include, url
from django.conf import settings
urlpatterns = [
    url(r'^', include('mainapp.urls', namespace='mainapp')),
]
