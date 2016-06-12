from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^grocery_list', views.grocery_list, name='grocery_list')
]
