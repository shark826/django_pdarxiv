"""arxivpd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include
from pdarxiv.views import PdCreateView, PdListDestroy, PdDetailView, \
                        index0, PdList, PdUpdateView, PdDeleteView, \
   LoginUser, logout_view, load_streets
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin/', admin.site.urls),
    path('arxpd/', login_required(PdList), name='arxpd'),
    path('arxpd/opis', PdListDestroy.as_view(), name='opis'),
    path('arxpd/<int:pk>/', PdDetailView.as_view(), name='viewarxpd'),
    path('arxpd/add/', PdCreateView.as_view(), name='addarxpd'),
    path('arxpd/<int:pk>/update', PdUpdateView.as_view(), name='updatearxpd'),
    path('arxpd/<int:pk>/delete', PdDeleteView.as_view(), name='deletearxpd'),
    path('load-streets/', load_streets, name='ajax_load_streets'),
    path('', login_required(index0),name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', login_required(logout_view), name='logout'),
]
