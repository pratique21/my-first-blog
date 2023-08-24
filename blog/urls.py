from django.urls import path
from . import views

#add the url pattern for the view that will correspond to list of posts

urlpatterns = [
    path('',views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]