from django.urls import path
from . import views

urlpatterns = [
    path('code/',views.editor, name='editor'),
   
]