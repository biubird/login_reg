from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='_index'),
    url(r'^register$', views.register, name='_register'),
    url(r'^login$', views.login, name='_login'),
    url(r'^success$', views.success, name='_success'),
    url(r'^logout$', views.logout, name='_logout')
]
