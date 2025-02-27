from django import forms
from .models import *

# Create your forms here.

class ControlPanelForm(forms.ModelForm):
    class Meta:
        model = ControlPanel
        fields = ['name', 'description']  # Поля для редактирования
