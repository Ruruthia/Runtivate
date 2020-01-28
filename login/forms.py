import datetime
from django import forms
from bootstrap_datepicker_plus import DatePickerInput


class NameForm(forms.Form):
    weight = forms.IntegerField(label='Your weight', min_value=30, required=True)
    height = forms.IntegerField(label='Your height', min_value=100, required=True)
    age = forms.IntegerField(label='Your age', min_value=16, required=True)
    choice = [("Female", "Female"), ("Male", "Male")]
    gender = forms.ChoiceField(choices=choice, label="Your gender", required=True)


class ActivityForm(forms.Form):
    date = forms.DateField(label='Date of activity', required=True, initial=datetime.datetime.now(),
                           widget=DatePickerInput(format='%d/%m/%Y'))
    duration = forms.IntegerField(label='Duration of activity', min_value=1, required=True)
    distance = forms.FloatField(label='Distance of activity', min_value=1, required=True)
    comment = forms.CharField(label='Comment', max_length=120, widget=forms.Textarea, required=False)
