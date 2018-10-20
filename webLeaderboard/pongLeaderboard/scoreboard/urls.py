from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<str:initialsParam>/<int:scoreParam>/', views.post, name='post'),
    path('get/', views.get, name='get'),
]
