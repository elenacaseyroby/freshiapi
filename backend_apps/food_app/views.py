from django.shortcuts import render

def index(request):
    # Add a view that renders the frontend build directory to serve front and back end at port 8000.
    return render(request, "build/index.html") 

def manifest(request):
    # View renders frontend/build/manifest.json.
    return render(request, "build/manifest.json") 