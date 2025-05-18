from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from django.shortcuts import render, redirect

# Create your views here.
def editor(request):
    
        # Render the editor template
        return render(request, 'editor.html')