"""OLC2_VCD_PY2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from home import views

urlpatterns = [
    path('',views.home),
    path('open',views.opencsv),
    path('archivos',csrf_exempt(views.archivo)),
    path('funcion/fun_1',views.funcion_1),
    path('funcion/fun_2',views.funcion_2),
    path('funcion/fun_3',views.funcion_3),
    path('funcion/fun_4',views.funcion_4),
    path('funcion/fun_5',views.funcion_5),
    path('funcion/fun_6',views.funcion_6),
    path('funcion/fun_7',views.funcion_7),
    path('funcion/fun_8',views.funcion_8),
    path('funcion/fun_9',views.funcion_9),
    path('funcion/fun_10',views.funcion_10),
    path('funcion/fun_11',views.funcion_11),
    path('funcion/fun_12',views.funcion_12),
    path('funcion/fun_13',views.funcion_13),
    path('funcion/fun_14',views.funcion_14),
    path('funcion/fun_15',views.funcion_15),
    path('funcion/fun_16',views.funcion_16),
    path('funcion/fun_17',views.funcion_17),
    path('funcion/fun_18',views.funcion_18),
    path('funcion/fun_19',views.funcion_19),
    path('funcion/fun_20',views.funcion_20),
    path('funcion/fun_21',views.funcion_21)
]
