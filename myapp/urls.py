from django.urls import path
from myapp.views import index, api_response

urlpatterns = [
    path('', index, name='index'),
    path('api/', api_response, name='api_response'),
]
