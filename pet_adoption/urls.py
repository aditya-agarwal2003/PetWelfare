from django.urls import path, re_path
from . import views

urlpatterns = [
    path('landing_page/', views.landing_page, name = 'landing_page'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name = 'contact'),
    path('create_post/', views.create_post, name = 'create_post'),
    re_path(r'see_details/(?P<post_id>\d+)/$', views.see_details, name = 'see_details'),
    re_path(r'delete_post/(?P<post_id>\d+)/$', views.delete_post, name = 'delete_post'),
    re_path(r'make_adopt_request/(?P<post_id>\d+)/$', views.make_adopt_request, name = 'make_adopt_request'),
    re_path(r'delete_adopt_request/(?P<ad_id>\d+)/$', views.delete_adopt_request, name = 'delete_adopt_request'),
]