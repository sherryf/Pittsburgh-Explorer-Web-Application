from django import forms
from datetime import datetime

from django.contrib.auth.models import User
# from django.utils.translation import gettext as _

from models import *
from choice import *

MAX_UPLOAD_SIZE = 2500000

class RegistrationForm(forms.Form):
	# first_name = forms.CharField(max_length=20)
	# last_name  = forms.CharField(max_length=20)
	username   = forms.CharField(max_length = 20)
	email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput())
	# age        = forms.IntegerField(min_value=0)

	
	password1  = forms.CharField(max_length = 200, 
								 label='Password', 
								 widget = forms.PasswordInput())
	password2  = forms.CharField(max_length = 200, 
								 label='Confirm password',  
								 widget = forms.PasswordInput())

	# Customizes form validation for properties that apply to more
	# than one field.  Overrides the forms.Form.clean function.
	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		cleaned_data = super(RegistrationForm, self).clean()

		# Confirms that the two password fields match
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")

		# We must return the cleaned data we got from our parent.
		return cleaned_data

	# Customizes form validation for the username field.
	def clean_username(self):
		# Confirms that the username is not already present in the
		# User model database.
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username is already taken.")

		# We must return the cleaned data we got from the cleaned_data
		# dictionary
		return username

	def clean_password2(self):
		# Confirms that the two password fields match
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")
		
		# We must return the cleaned data we got from the cleaned_data
		# dictionary
		return password2


class SearchForm(forms.Form):
	
	estimateDate = forms.DateField(label="Estimate Date", widget=forms.DateInput(format = '%m/%d/%Y'),
                                 input_formats=('%m/%d/%Y',),initial=datetime.now())
	startTime  = forms.TimeField(label="start Time",widget=forms.TimeInput(format='%H:%M'),initial="9:30")
	# endTime    = forms.TimeField(label="End Time",widget=forms.TimeInput(format='%H:%M'))
	startStreet = forms.CharField(label="Start Street", max_length = 20,initial="Center")
	startCrossStreet = forms.CharField(label="Start Cross Street", max_length = 20,initial="Morewood")
	# budget = forms.CharField(max_length=20, label="budget")
	# interest = forms.CharField(max_length=20,label="interest")
	# groupSize = forms.IntegerField(label="group size")
	# budget = forms.ChoiceField(choices=["Bankrupt","Economy","Salary Day"])
	# interest = forms.ChoiceField(choices=["Water Sports","Parks","Nights","Sights","Museums","Concerts","Fun & Games","Food","Outdoor","Shopping","Workshops","Tour"])
	# groupSize = forms.IntegerField(label="group size")

	budget    = forms.ChoiceField(choices = BUDGET_CHOICES, label="Budget", initial="Economy", widget=forms.Select(), required=True)
	interest = forms.ChoiceField(choices = INTEREST_CHOICES, label="Interest", initial="Art", widget=forms.Select(), required=True)
	groupSize = forms.ChoiceField(choices = GROUPSIZE_CHOICES, label="Group Size", initial=1, widget=forms.Select(), required=True)

	# Customizes form validation for properties that apply to more
	# than one field.  Overrides the forms.Form.clean function.
	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		cleaned_data = super(SearchForm, self).clean()

		# # Confirms that the two password fields match
		# password1 = cleaned_data.get('password1')
		# password2 = cleaned_data.get('password2')
		# if password1 and password2 and password1 != password2:
		# 	raise forms.ValidationError("Passwords did not match.")

		# We must return the cleaned data we got from our parent.
		return cleaned_data

class phoneForm(forms.Form):
	
	phoneNumber = forms.CharField(label="Mobile Phone Number", initial="+1xxxxxxxxxx")

