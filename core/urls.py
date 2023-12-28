from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('register/',register_view,name='register'),
    path('login/',login_view,name='login'),
    path("logout/", logout_view, name="logout"),
    path("blog_detail/<int:pk>/",blog_detail,name='blog_detail'),
    path('like_blog/<int:blog_id>/',like_blog,name='like_blog'),
    path('write_comment/<int:pk>/',write_comment,name='write_comment'),
    path('contact/',contact,name='contact'),
    path('new_blog/',new_blog,name='new_blog'),
    path('about/',about,name='about')
]
