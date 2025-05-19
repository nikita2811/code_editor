from django.urls import path
from . import views

urlpatterns = [
    path('execute/', views.execute_python, name='execute_docker'),
]
