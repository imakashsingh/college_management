from django import forms

from onlineapp.models import *

class AddCollege(forms.ModelForm):
    class Meta:
        model = College
        exclude = ['id']
        widgets = {
            'name': forms.TextInput(),
            'location': forms.TextInput(),
            'acronym': forms.TextInput(),
            'contact': forms.EmailInput()
        }

class AddStudent(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['college','id']
        widgets = {
            'name': forms.TextInput(),
            'email': forms.EmailInput(),
            'dob': forms.DateInput(),
            'dropped_out': forms.CheckboxInput(),
            'db_folder': forms.TextInput(),
        }

class Mockdetails(forms.ModelForm):
    class Meta:
        model = MockTest1
        exclude = ['id','student','total']
        widgets = {
            'marks1' : forms.NumberInput(),
            'marks2' : forms.NumberInput(),
            'marks3' : forms.NumberInput(),
            'marks4' : forms.NumberInput(),
        }
class Login_form(forms.Form):
    class Meta:
        fields = '__all__'
        widgets = {
            'username' : forms.TextInput(),
            'password' : forms.PasswordInput(),
        }

class SignUp_form(forms.Form):
    class Meta:
        widgets = {
            'first_name' : forms.TextInput(),
            'last_name' : forms.TextInput(),
            'username' : forms.TextInput(),
            'password' : forms.PasswordInput(),
        }