from django.test import TestCase, Client
from django.urls import reverse
from .models import Team, TeamsLock

class LockEnforcementTests(TestCase):
    def setUp(self):
        self.client = Client()
        TeamsLock.objects.create(pk=1, is_locked=False)
        Team.objects.create(team_name="Alpha & Beta", player1_name="Alpha", player2_name="Beta")

    def test_teams_page_editable_when_unlocked(self):
        response = self.client.get(reverse('teams'))
        self.assertContains(response, 'Add Team')
        self.assertNotContains(response, 'Teams are locked. No changes allowed.')

    def test_teams_page_readonly_when_locked(self):
        lock = TeamsLock.objects.get(pk=1)
        lock.is_locked = True
        lock.save()
        response = self.client.get(reverse('teams'))
        self.assertContains(response, 'Teams are locked. No changes allowed.')
        self.assertNotContains(response, 'Add Team')

    def test_groups_page_hidden_when_unlocked(self):
        response = self.client.get(reverse('groups'))
        self.assertContains(response, 'Teams must be locked before assigning or viewing groups.')

    def test_groups_page_visible_when_locked(self):
        lock = TeamsLock.objects.get(pk=1)
        lock.is_locked = True
        lock.save()
        response = self.client.get(reverse('groups'))
        self.assertContains(response, 'Group 1')
        self.assertNotContains(response, 'Teams must be locked before assigning or viewing groups.')
