"""
URL configuration for backend project.

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
# from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from backend.settings import STATIC_URL

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('v1/auth/', include('authentication.urls')),
    path('v1/comm/', include('communication.urls')),
    path('v1/knowledge-base/', include('knowledge_base.urls')),
    path('v1/users/', include('user_manager.urls')),
    path('v1/rsc/', include('file_manager.urls')),
    # re_path(r'^v1/avatar/(?P<path>.*)$', serve, {'document_root': STATIC_URL}),
]
