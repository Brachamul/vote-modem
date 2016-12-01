from django.contrib import admin

from .models import *



class VoteAdmin(admin.ModelAdmin):
	model = Vote
	list_display = ("election", "code", "already_used", "stamp")
	readonly_fields = ("election", "code", "value", "already_used", "stamp")

admin.site.register(Vote, VoteAdmin)



class VotesInline(admin.TabularInline):
	model = Vote
	list_per_page = 2000

class ElectionAdmin(admin.ModelAdmin):
	model = Election
	inlines = [VotesInline, ]

admin.site.register(Election, ElectionAdmin)
