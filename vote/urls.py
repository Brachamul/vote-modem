from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
	url(r'^$', views.vote, name='vote' ),
	url(r'^aa4438b0-d845-4dc9-9334-922691735c22/', views.insert_code, name='insert_code' ),
	url(r'^(?P<code>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.vote, name='vote_with_code' ),
	url(r'^results/', views.results, name='results' ),
	url(r'^list-codes/', views.list_codes, name='list_codes' ),
]

