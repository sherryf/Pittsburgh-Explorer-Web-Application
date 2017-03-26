from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, get_user

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

# Imports from Model and Forms
from planner.models import *
from planner.forms import *

from datetime import datetime
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core import serializers

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator
# Used to send mail from within Django
from django.core.mail import send_mail
from s3 import s3_upload, s3_delete


# Action for the default /planner/ route.
@ensure_csrf_cookie
def home(request):
	print("get in function home for search.html")
    
	return render(request, 'planner/search.html', {})

@login_required
def itinerary(request):
	print("get in function itinerary for default plan page")
   
	return render(request, 'planner/home.html', {})

@transaction.atomic
def register(request):
	context = {}
	# errors = []
	# context['errors'] = errors

	# Just display the registration form if this is a GET request.
	if request.method == 'GET':
		context['form'] = RegistrationForm()    
		return render(request, 'planner/register.html', context)

	# Creates a bound form from the request POST parameters and makes the 
	# form available in the request context dictionary.
	form = RegistrationForm(request.POST)
	context['form'] = form

	# Validates the form.
	if not form.is_valid():
		return render(request, 'planner/register.html', context)

	# At this point, the form data is valid.  Register and login the user.
	new_user1 = User.objects.create_user(username=form.cleaned_data['username'], 
										password=form.cleaned_data['password1'],
										# first_name=form.cleaned_data['first_name'],
										# last_name=form.cleaned_data['last_name'],
										email=form.cleaned_data['email'])
	# Mark the user as inactive to prevent login before email confirmation.
	new_user1.is_active = False
	new_user1.save()

	# save the record to UserInfo
	new_user2 = UserInfo(username=form.cleaned_data['username'], 
						# password=form.cleaned_data['password1'],
						
						# first_name=form.cleaned_data['first_name'],
						# last_name=form.cleaned_data['last_name'],
						update_time = datetime.now(),
						email=form.cleaned_data['email'])
	# Mark the user as inactive to prevent login before email confirmation.
	new_user2.is_active = False
	new_user2.save()

	# Generate a one-time use token and an email message body
	token = default_token_generator.make_token(new_user1)
	# token2 = default_token_generator.make_token(new_user2)

	email_body = """
Welcome to the Pittsburgh Explorer.  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(), 
	reverse('confirm', args=(new_user1.username, token)))

	send_mail(subject="Verify your email address",
		message= email_body,
		from_email="yangleip@cmu.edu",
		recipient_list=[new_user1.email])

	context['email'] = form.cleaned_data['email']
	return render(request, 'planner/needs-confirmation.html', context)


@transaction.atomic
def confirm_registration(request, username, token):
	user = get_object_or_404(User, username=username)

	# Send 404 error if token is invalid
	if not default_token_generator.check_token(user, token):
		raise Http404
	# if not default_token_generator.check_token(userInfo, token2):
		# raise Http404

	# Otherwise token was valid, activate the user.
	user.is_active = True
	user.save()
	return render(request, 'planner/confirmed.html', {})






























