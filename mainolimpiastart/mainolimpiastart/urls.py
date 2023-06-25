"""
URL configuration for mainolimpiastart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from main.views import *
from django.urls import  path, include

from mainolimpiastart import settings
from  rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r'user', UserViewSet, basename='women')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    # path('api/v1/drf-auth/', include('rest_framework.urls')),
    # path('api/v1/user/<int:pk>/', UserAPIUpdate.as_view()),
    # path('api/v1/userdelete/<int:pk>/', UserAPIDestroy.as_view()),
    # path('api/v1/profile/<int:pk>/', ProfileAPIUpdate.as_view()),
    # path('api/v1/auth/', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path('api/v1/profile/', ProfileAPIList.as_view()),
    # path('api/v1/', include(router.urls)),
    # path('api/v1/profiledetail/<int:pk>/', ProfileAPIDetailView.as_view()),
    # path('api/v1/profilelist/', ProfileAPIView.as_view()),
    # path('api/v1/profilelist/<int:pk>/', ProfileAPIView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound

