import json

from django import forms

from .models import *

class ElectionForm(forms.ModelForm):

	def clean_choices(self):
		choices = self.cleaned_data.get('choices')
		try : json.loads(choices)
		except json.decoder.JSONDecodeError : raise forms.ValidationError("This needs to be valid JSON.")
		return self.cleaned_data["choices"]

	def clean_end(self):
		start = self.cleaned_data.get('start')
		end = self.cleaned_data.get('end')
		if start > end : raise forms.ValidationError("Your election's end date needs to be later than its start date.")
		return self.cleaned_data["end"]

	def clean_number_of_voters(self):
		number_of_voters = self.cleaned_data.get('number_of_voters')
		number_of_existing_codes = Vote.objects.filter(election=self.instance).count()
		unused_codes = Vote.objects.filter(election=self.instance, already_used=False)
		if number_of_voters < number_of_existing_codes :
			# If we need fewer voters than are currently registered
			number_of_extra_codes = number_of_voters - number_of_existing_codes
			# This is how many extra codes we have, that we should delete
			if unused_codes.count() < number_of_extra_codes :
				# There aren't enough unused votes to delete !
				raise forms.ValidationError("Some codes have already been used, so you can't reduce the number of codes automatically, you'll need to go manual.")
		return self.cleaned_data["number_of_voters"]