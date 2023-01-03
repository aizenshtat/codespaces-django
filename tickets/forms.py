from django import forms

class WaitingRoomForm(forms.Form):
    name = forms.CharField(max_length=100)

class CounterForm(forms.Form):
    name = forms.CharField(max_length=100)

class EmployeeForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
