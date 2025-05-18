from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response

# Create your views here.
class EditorView(generics.GenericAPIView):
    def get(self, request):
        # Render the editor template
        return render(request, 'editor/editor.html')