"""
URL configuration for mywebproj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

import myblog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',myblog.views.index),
    path('trans/',myblog.views.result_transaction),
    path('result/',myblog.views.result),
    path('add_bookmark/',myblog.views.add_bookmark),
    path('bookmark/',myblog.views.show_bookmark),
    path('delete_bookmark/<int:dish_id>', myblog.views.delete_bookmark),
]
