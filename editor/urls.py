from django.urls import path
from . import views

urlpatterns = [
    path('code/',views.run_code, name='code'),
   
]