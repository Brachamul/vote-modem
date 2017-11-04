# -*- coding: utf-8 -*-

import os, uuid, json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Max, F

from datetime import datetime, timedelta


class Election(models.Model):

	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	start = models.DateTimeField()
	end = models.DateTimeField()
	description = models.TextField(max_length=5000)
	choices = models.CharField(max_length=1024, help_text='\
		[{"text": "Alain Juppé", "slug": "alain-juppe"}, {"text": "François Fillon", "slug": "francois-fillon"}]')
	max_number_of_choices = models.PositiveSmallIntegerField(default=1)
	number_of_voters = models.IntegerField()

	def options(self): 
		return json.loads(self.choices)

	def option_name(self, slug):
		options = self.options()
		for option in options :
			if option['slug'] == slug :
				return option['text']
		return slug

	def save(self, *args, **kwargs):
		super(Election, self).save(*args, **kwargs)
		# TODO : this should probably be a signal...
		# moved all the code after the save, because otherwise we couldn't attach 
		# the new vote objects to the election, since it didn't exist yet
		# when an "election" instance is modified, we regenerate codes to make sure
		# there are enough for everyone, but not too many
		number_of_codes = Vote.objects.filter(election=self).count()
		number_of_codes_required = self.number_of_voters - number_of_codes
		if number_of_codes_required < 0 :
			# there are two many codes, must delete some !
			# just fyi, there is a verification step to make sure one does not do anything stupid
			# see the forms.py entry for Election
			number_of_extra_codes = -number_of_codes_required
			Vote.objects.filter(election=self, already_used=False).delete() # delete all unused codes
			number_of_used_codes = Vote.objects.filter(election=self, already_used=True).count()
			number_of_codes_required = self.number_of_voters - number_of_used_codes # regenerate codes
		if number_of_codes_required > 0 :
			# there aren't enough codes, must create more !
			Vote.objects.bulk_create([Vote(election=self) for i in range(number_of_codes_required)])

	def get_results(self):
		votes = Vote.objects.filter(election=self, already_used=True)
		number_of_votes = votes.count()
		registrar = {}
		for vote in votes :
			choices = []
			try :
				values = json.loads(vote.value)
				# multivotes are registered as JSON
				# so if this check passes, the vote is a multivote
			except ValueError :
				# if the test fails, it's a single vote
				choices.append(vote.value)
			else :
				# otherwise, it's a multivote
				for value in values :
					choices.append(value)
			for choice in choices :
				if choice in registrar : registrar[choice] += 1
				else : registrar[choice] = 1
		return (number_of_votes, registrar)

	def __str__(self):
		return str(self.name)

	class Meta:
		get_latest_by = 'start'
		verbose_name = 'élection'



class Vote(models.Model):

	election = models.ForeignKey(Election, on_delete=models.CASCADE)
	code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	value = models.CharField(max_length=255, blank=True, null=True)
	already_used = models.BooleanField(default=False)
	stamp = models.DateTimeField(auto_now=True, null=True)

	def save(self, *args, **kwargs):
		# Set "already_used" to true when value is set
		if self.value :
			self.already_used = True
		else :
			self.already_used = False
		super(Vote, self).save(*args, **kwargs)

	def __str__(self):
		return str(self.code)