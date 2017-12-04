from django.conf.urls import url
from hc.blog import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^post/(?P<slug>[^\.]+)$',
        views.view_post,
        name='view_blog_post'),
    url(r'^category/(?P<slug>[^\.]+)$',
        views.view_category,
        name='view_blog_category'),
    url(r'^create_post/$',
        views.create_post,
        name='create_blog_post'),
]
