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
	choices = models.CharField(max_length=1024)
	# [{"text": "Alain Juppé", "slug": "alain-juppe"}, {"text": "François Fillon", "slug": "francois-fillon"}]

	def options(self): 
		return json.loads(self.choices)

	def option_name(self, slug):
		options = self.options()
		for option in options :
			if option['slug'] == slug :
				return option['text']
		return slug

	def __str__(self):
		return str(self.name)

	class Meta:
		get_latest_by = 'start'
		verbose_name = 'élection'



class Vote(models.Model):

	election = models.ForeignKey(Election)
	code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	value = models.CharField(max_length=255, blank=True, null=True)
	already_used = models.BooleanField(default=False)
	stamp = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return str(self.code)



