from django import forms
from .models import Group, Team, GroupAssignment, Court, Match

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'player1_name', 'player2_name']
        widgets = {
            'team_name': forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Team Name'}),
            'player1_name': forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Player 1 Name'}),
            'player2_name': forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Player 2 Name'}),
        }

class GroupAssignmentForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.filter(is_locked=True), label="Team")
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Group")

class ScheduleForm(forms.Form):
    round_name = forms.ChoiceField(choices=Match.ROUND_CHOICES, label="Round")
    num_courts = forms.ChoiceField(choices=[(4, '4 Courts'), (8, '8 Courts')], label="Number of Courts")
    start_time = forms.DateTimeField(label="Start Time", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
