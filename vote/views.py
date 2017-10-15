# -*- coding: utf-8 -*-
import csv, logging, sys, random, ast, json, datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Max, F
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from .models import *
from .forms import *



def now():
	# time difference with pythonanywhere uk servers
	return datetime.now() + timedelta(hours=1)

def expired_elections():
	return Election.objects.filter(end__lt=now()).exclude(end__lt=now()-timedelta(days=1))

def current_elections():
	return Election.objects.filter(start__lt=now(), end__gt=now())

def upcoming_elections():
	return Election.objects.filter(start__gt=now())


def welcome(request):
	return render(request, 'vote/welcome.html', {
		'expired_elections':  expired_elections(),
		'current_elections': current_elections(),
		'upcoming_elections': upcoming_elections(),
		})

def vote(request, election, code=False):
	election = get_object_or_404(Election, slug=election)
	if election in current_elections() :
		if code :
			try : vote = Vote.objects.get(code=code)
			except ObjectDoesNotExist :
				messages.error(request, "Ce lien n'est plus actif.")
			else :
				if request.method == "POST":
					if vote.already_used :
						messages.error(request, "Ce lien a déjà été utilisé pour voter.")
					else : 
						if election.max_number_of_choices > 1 :
							vote.value = request.POST.getlist('vote')
						else :
							vote.value = request.POST.get('vote')
						vote.already_used = True
						vote.save()
						messages.success(request, "Votre vote a bien été pris en compte !")
				else :
					if vote.already_used :
						messages.info(request, "Votre vote a déjà été pris en compte !")
					else :
						return render(request, 'vote/vote.html', { 'election': election, 'display_vote_form': True })
		else :
			messages.info(request, "Pour voter, cliquez sur le lien inclus dans votre email de convocation au vote.")
	elif election in upcoming_elections():
		messages.info(request, "Le vote n'est pas encore ouvert !")
	elif election in expired_elections():
		messages.error(request, "Le vote est désormais clos.")
	return render(request, 'vote/vote.html', { 'election': election, 'display_vote_form': False })



@login_required
def results(request, election):
	election = get_object_or_404(Election, slug=election)
	total_number_of_votes = Vote.objects.filter(election=election, already_used=True).count()
	values = Vote.objects.filter(election=election, already_used=True).values_list('value', flat=True).distinct()
	results = []
	for value in values :
		option = election.option_name(value)
		number = Vote.objects.filter(election=election, value=value).count()
		percentage = (number/total_number_of_votes)*100
		results.append('{} : {}% ({} votes)'.format(option, round(percentage, 2), number))
	dashboard = {
		'Nombre de votants': total_number_of_votes,
		'Resultats' : results,
	}
	return render(request, 'vote/results.html', { 'election': election, 'dashboard': dashboard })

@login_required
def list_codes(request, election):
	election = get_object_or_404(Election, slug=election)
	codes = []
	for vote in Vote.objects.filter(election=election, already_used=False):
		codes.append(vote.code)
	return render(request, 'vote/list_codes.html', { 'page_title' : 'Liste des codes encore utilisables', 'election': election, 'codes': codes })