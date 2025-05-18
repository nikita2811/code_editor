
from django.urls import path,include
from . import views

urlpatterns = [
    path('editor/',views.editor, name='editor'),
   
]