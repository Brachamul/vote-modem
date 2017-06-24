from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
	url(r'^$', views.welcome, name='vote_welcome' ),
	url(r'^(?P<election>[-\w]+)/$', views.vote, name='vote_witout_code'), 
	url(r'^(?P<election>[-\w]+)/(?P<code>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.vote, name='vote_with_code' ),
	url(r'^(?P<election>[-\w]+)/results/', views.results, name='results' ),
	url(r'^(?P<election>[-\w]+)/list-codes/', views.list_codes, name='list_codes' ),
]

