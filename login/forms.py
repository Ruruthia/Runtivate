from django import forms

class NameForm(forms.Form):
    weight = forms.IntegerField(label='Your weight', required=True)
    height= forms.IntegerField(label='Your height', required=True)
    age = forms.IntegerField(label='Your age', required=True)
    c =[("Female", "Female"), ("Male", "Male")]
    gender = forms.ChoiceField(choices=c, label="Your gender", required=True)
