from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from datetime import datetime, timedelta
from vote.models import *



class RestaurantTestCase(TestCase):


	def setUp(self):

		self.client = Client()
		
		self.singleChoiceElection = Election.objects.create(
			name = "Single Choice Election",
			slug = "single-choice-election",
			start = datetime.now(),
			end = datetime.now() + timedelta(days=1),
			description = "A single choice election test.",
			choices = '''[{"text": "Alain Juppé", "slug": "alain-juppe"}, {"text": "François Fillon", "slug": "francois-fillon"}]''',
			max_number_of_choices = 1,
			number_of_voters = 12,
			)

		self.multipleChoiceElection = Election.objects.create(
			name = "Multiple Choice Election",
			slug = "multiple-choice-election",
			start = datetime.now(),
			end = datetime.now() + timedelta(days=1),
			description = "A multiple choice election test.",
			choices = '''[{"text": "Alain Juppé", "slug": "alain-juppe"}, {"text": "François Fillon", "slug": "francois-fillon"}]''',
			max_number_of_choices = 2,
			number_of_voters = 12,
			)


	def test_vote_single_choice(self):

		''' Est-il possible de voter pour une élection à un choix ? '''

		election = self.singleChoiceElection
		election_votes = Vote.objects.filter(election=election)
		code = election_votes[0].code
		vote = Vote.objects.get(code=code)
		vote.value = "alain-juppe"
		vote.save()

		number_of_votes, registrar = election.get_results()

		self.assertEqual(registrar['alain-juppe'], 1)



	def test_vote_multiple_choice(self):

		''' Est-il possible de voter pour une élection à plusieurs choix ? '''

		election = self.multipleChoiceElection
		election_votes = Vote.objects.filter(election=election)
		code = election_votes[0].code
		vote = Vote.objects.get(code=code)
		vote.value = '''["alain-juppe","francois-fillon"]'''
		vote.save()

		number_of_votes, registrar = election.get_results()

		self.assertEqual(registrar['alain-juppe'], 1)