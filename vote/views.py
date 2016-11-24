# -*- coding: utf-8 -*-
import csv, logging, sys, random, ast, json

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



def say(something):
	print("======================")
	print(something)
	print("======================")



def vote(request, code=False):
	display_vote_form = False
	if code :
		try : vote = Vote.objects.get(code=code)
		except ObjectDoesNotExist :
			messages.error(request, "Ce lien n'est plus actif.")
		else :
			if request.method == "POST":
				if vote.already_used :
					messages.error(request, "Ce lien a déjà été utilisé pour voter.")
				else : 
					vote.value = request.POST.get('vote')
					vote.already_used = True
					vote.save()
					messages.success(request, "Votre vote a bien été pris en compte !")
			else :
				if vote.already_used :
					messages.info(request, "Votre vote a déjà été pris en compte !")
				else :
					display_vote_form = True
	return render(request, 'vote/vote.html', { 'display_vote_form': display_vote_form })

@login_required
def results(request):
	dashboard = {
		'Nombre de votants': Vote.objects.filter(already_used=True).count(),
		'Valeurs' : Vote.objects.filter(already_used=True).values_list('value', flat=True).distinct(),
	}
	return render(request, 'vote/results.html', { 'dashboard': dashboard })

@login_required
def list_codes(request):
	codes = []
	for vote in Vote.objects.filter(already_used=False) :
		codes.append(vote.code)
	return render(request, 'vote/list_codes.html', { 'page_title' : 'Liste des codes encore utilisables', 'codes': codes })