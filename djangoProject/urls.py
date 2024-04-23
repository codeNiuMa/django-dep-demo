"""djangoProject URL Configuration

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
from django.contrib import admin
from django.urls import path
from app01 import views
from app02 import views

urlpatterns = [
    ### app01 ###
    # # path('admin/', admin.site.urls),
    # # 用户访问index，执行函数views.index
    # path('index/', views.index),
    # path('user/list/', views.user_list),
    # path('user/add/', views.user_add),
    # path('tpl/', views.tpl),
    # path('gp/', views.getpost),
    # path('bili/', views.redi),
    # path('orm/', views.orm),

    ### app02 ###
    path('dep/list/', views.dep_list),
    path('dep/add/', views.add),
    path('dep/del/', views.dele),
    # <<int:id>>代表传递url必须dep/edit/数字/
    path('dep/edit/<int:id>/', views.edit),

]
