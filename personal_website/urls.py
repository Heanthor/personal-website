from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^grocery_list$', views.grocery_list, name='grocery_list'),
    url(r'^grocery_list/save_purchase$', views.save_purchase, name='save_purchase'),
    url(r'^grocery_visits', views.grocery_visits, name='grocery_visits'),
    url(r'^auth/signup', views.sign_up, name='sign_up'),
    url(r'^auth/login', views.log_in, name='log_in')
]
