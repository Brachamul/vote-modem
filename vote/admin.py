from django.contrib import admin

from .models import *



class VoteAdmin(admin.ModelAdmin):
	model = Vote
	list_display = ("code", "already_used", "stamp")
	readonly_fields = ( "code", "value", "already_used", "stamp")

admin.site.register(Vote, VoteAdmin)