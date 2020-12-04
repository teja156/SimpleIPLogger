"""IPLoggerServer URL Configuration

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
from django.urls import path
from MyServer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('shorten/', views.create_shortened_url,name='shorten'),
    path('test_redirect/', views.redirect_test),
    path('ip_test/', views.ip_test),
    path('user_agent_test/', views.user_agent_test),
    path('<slug:short_link>/', views.redirect_now),
    path('tracking/<slug:tracking_link>/', views.fetch_tracking_data),
]
