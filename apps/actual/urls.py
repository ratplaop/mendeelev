from django.urls import path
from .views import index, actual_detail

app_name = 'actual'

urlpatterns = [
    path('', index, name='actual_index'),
    path('actual/<int:actual_id>/', actual_detail, name='actual_detail'),
]
