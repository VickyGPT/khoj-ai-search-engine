from django.urls import path
from myapp.views import index, api_response , llama_view

urlpatterns = [
    path('', index, name='index'),
    path('api/', api_response, name='api_response'),
    path('llama/', llama_view, name='llama_view'),

]
