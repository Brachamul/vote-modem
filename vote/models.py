# -*- coding: utf-8 -*-

import os, uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Max, F

from datetime import datetime, timedelta


class Vote(models.Model):

	code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	value = models.CharField(max_length=255, blank=True, null=True)
	already_used = models.BooleanField(default=False)
	stamp = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return '{}		{}'.format(self.code, self.value)