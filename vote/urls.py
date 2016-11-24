from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
	url(r'^(?P<code>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
		views.vote, name='vote_with_code'
		),
	url('^',	views.vote, name='vote' ),
	url(r'^results/', views.results, name='results' ),
]