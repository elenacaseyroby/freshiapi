"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from django_apps.website.views import index, manifest
from django_apps.users.api_views import UserList, UserCreate
from django_apps.api_auth.api_views import token, revoke

urlpatterns = [
    # API
    path('api/v1/token/', token, name="token"),
    path('api/v1/token/revoke/', revoke, name="revoke"),
    path('api/v1/users/', UserList.as_view()),
    path('api/v1/users/new/', UserCreate.as_view()),

    # Route “host:8000/” to the view that renders the frontend build to serve
    # front and back end at port 8000.
    # Only urls starting with /admin or /api or manifest.jon will be rendered
    # from the backend.
    re_path(r'^(?!admin)(?!api)(?!manifest.json).*', index, name="index"),
    path('admin/', admin.site.urls),
    # Route "host:8000/manifest.json" to frontend/build/manifest.json
    path("manifest.json", manifest, name="manifest"),
]
