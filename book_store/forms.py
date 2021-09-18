import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


class Napomny(forms.Form):
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)
    date = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_date(self):
        now = timezone.now()
        data = self.cleaned_data['date']

        if data > (now + datetime.timedelta(days=2)) or data < now:
            raise ValidationError('Wrong date!')
