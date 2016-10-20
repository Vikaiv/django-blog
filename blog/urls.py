# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from blog import views
from blog.views import PostsListView, PostDetailView, PrivatePostList, UserDetailView

app_name = 'blog'
urlpatterns = [
    url(r'^$', PostsListView.as_view(), name='list'),  # то есть по URL http://имя_сайта/blog/
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='detail'),# а по URL http://имя_сайта/blog/число/
    url(r'^place_search/$', PostsListView.as_view(), name='post_search'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^myposts/$', PrivatePostList.as_view(), name='private_list'),
    url(r'^register/$', views.RegisterFormView.as_view(), name='register'),
    url(r'^user/(?P<pk>\d+)/$', UserDetailView.as_view(), name='user_detail'),
]