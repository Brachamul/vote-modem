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