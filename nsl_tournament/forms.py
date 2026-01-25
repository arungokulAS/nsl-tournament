from django import forms
from .models import Team

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'player1_name', 'player2_name']
        widgets = {
            'team_name': forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Team Name'}),
            'player1_name': forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Player 1 Name'}),
            'player2_name': forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Player 2 Name'}),
        }
