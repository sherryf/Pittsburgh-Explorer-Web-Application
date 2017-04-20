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
from dateutil import parser
from django.db import connection
from random import randint
import json
import googlemaps
import datetime

week = ['Monday', 'Tuesday',  'Wednesday', 'Thursday',  'Friday', 'Saturday','Sunday']
month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# Action for the default /planner/ route.
@ensure_csrf_cookie
@login_required
def home(request):
	form = SearchForm();
	print("get in function home for search.html")
    
   	return render(request, 'planner/search.html', {'form':form})

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
						# update_time = datetime.now(),
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

@transaction.atomic
@login_required
def search(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = SearchForm()
        return render(request, 'planner/search.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = SearchForm(request.POST)
    context['form'] = form
   
    # Validates the form.
    if not form.is_valid():
        return render(request, 'planner/search.html', context)

    # print(form.cleaned_data['estimateDate'])
    # print(form.cleaned_data['startTime'])
    # print(form.cleaned_data['startStreet'])
    # print(form.cleaned_data['startCrossStreet'])
    # print(form.cleaned_data['budget'])
    # print(form.cleaned_data['interest'])
    # print(form.cleaned_data['groupSize'])

    # At this point, the form data is valid.  Register and login the user.
    # new_user = User.objects.create_user(username=form.cleaned_data['username'], 
    #                                     password=form.cleaned_data['password1'],
    #                                     email=form.cleaned_data['email'],
    #                                     first_name=form.cleaned_data['first_name'],
    #                                     last_name=form.cleaned_data['last_name'])
    # new_user.save()

    # Logs in the new user and redirects to his/her todo list
    # new_user = authenticate(username=form.cleaned_data['username'],
    #                         password=form.cleaned_data['password1'])
    # login(request, new_user)

    ## connect with google API
    gmaps = googlemaps.Client(key='AIzaSyAn-6XiiENx0RGqGcI8_BjKzTUUQAiI7T8')

    ## get geocode for start place 
    geocode_result = gmaps.geocode(form.cleaned_data['startStreet'] + " at " +form.cleaned_data['startCrossStreet'])
    geocode = geocode_result[0]['geometry']['location']
    context['slat'] = geocode_result[0]['geometry']['location']['lat'] ## get start place lat
    context['slng']= geocode_result[0]['geometry']['location']['lng'] ## get start place lng

    ## split estimateDate to Month, Day, Day of Week
    datetime_object = form.cleaned_data['estimateDate']
    context['mon'] = month[datetime_object.month-1]
    context['date']= datetime_object.day
    context['dow'] = week[datetime_object.weekday()]

    ## get start time 
    context['startTime'] = form.cleaned_data['startTime']

    ## Combine start location 
    context['start'] =  form.cleaned_data['startStreet'] + "&" + form.cleaned_data['startCrossStreet']

    ## get interest to perform search 
    interest = form.cleaned_data['interest']
    context['interest'] = interest ## return interest back 

    ## get budget constraint
    if form.cleaned_data['budget'] == 'Bankrupt':
        cost_limit = 0
    elif form.cleaned_data['budget'] == 'Economy':
        cost_limit = 20
    elif form.cleaned_data['budget'] == 'Salary Day':
        cost_limit = 200

    ## OperationalError: Could not decode to UTF-8 column 'ShortDesc' with text
    connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")

    ## search for all objects that in the interest category and below budget constraint
    Objects = Attractions.objects.all().filter(cost__lte = cost_limit).filter(category = interest)
    
    if Objects.count() < 1 :
        context['form'] = form
        context['Error'] = "No activities match your choice!"
        return render(request, 'planner/search.html', context)

    ## random select two options for morning and afternoon 
    # print(Objects.count())

    i = randint(0,Objects.count()-1)
    j = randint(0,Objects.count()-1) 
    
    ## if i == j select again 
    while i == j:
        j = randint(0,Objects.count()-1) 


    ## return objects, morning event, afternoon event
    context['morning_event'] =  Objects[i]
    context['afternoon_event']= Objects[j]
    id1 = Objects[i].id
    id2 = Objects[j].id 
    context['objects'] = Attractions.objects.all().filter(cost__lte = cost_limit).filter(category = interest).exclude(id__in = [id1,id2])

    ## find lunch 
    lunch  =  Attractions.objects.all().filter(category = "Restaurant").filter(cost__lte = cost_limit)
    y = randint(0,lunch.count()-1)
    context['lunch'] =  lunch[y]

    ## calculate for travel ban 

    ##distance_matrix

    time = []
    ## 1 start place to morning event
    start = form.cleaned_data['startStreet'] + " at " +form.cleaned_data['startCrossStreet']
    destination  = Objects[i].address

    starttime = form.cleaned_data['startTime']
    time.append(str(starttime)[:-3])
    
    print(start)
    print(destination)
    travel_time = gmaps.distance_matrix(start,destination)["rows"][0]["elements"][0]["duration"]['value']
    travel_time = datetime.timedelta(seconds=travel_time+1800)
    travel_time_str =  str(travel_time)[:-3]
    time.append(travel_time_str)

    ## 2 morning event and stay at morning event
    starttime = datetime.datetime.combine(datetime.date(1, 1, 1), form.cleaned_data['startTime'])+ travel_time
    starttime_str = starttime.time().strftime('%H:%M')
    time.append(starttime_str)

    try:
        x = float(Objects[i].recommended_length_of_visit)
    except ValueError:
        x = 1

    play_time = datetime.timedelta(seconds = x *60)*60
    play_time_str =  str(play_time)[:-3]
    time.append(play_time_str)

    ## 3 morning event to lunch 
    starttime = starttime + play_time
    starttime_str = starttime.time().strftime('%H:%M')
    time.append(starttime_str)

    start = destination
    destination = "875 Greentree Rd #106, Pittsburgh, PA 15220"

    print(start)
    print(destination)

    travel_time = gmaps.distance_matrix(start,destination)["rows"][0]["elements"][0]["duration"]['value']
    travel_time = datetime.timedelta(seconds=travel_time+1800)
    travel_time_str =  str(travel_time)[:-3]
    time.append(travel_time_str)

    ## 4 lunch event and stay 
    starttime = starttime+ travel_time
    starttime_str = starttime.time().strftime('%H:%M')
    time.append(starttime_str)

    lunch_time = datetime.timedelta(seconds = 60*60)
    lunch_time_str = str(lunch_time)[:-3]
    time.append(lunch_time_str)

    ## 5 lunch event to afternoon_event 
    starttime = starttime + lunch_time
    starttime_str = starttime.time().strftime('%H:%M')
    time.append(starttime_str)

    start = destination
    destination = Objects[j].address

    print(start)
    print(destination)


    travel_time = gmaps.distance_matrix(start,destination)["rows"][0]["elements"][0]["duration"]['value']
    travel_time = datetime.timedelta(seconds=travel_time+1800)
    travel_time_str =  str(travel_time)[:-3]
    time.append(travel_time_str)

    ## 6 afternoon  event to stay 

    starttime = starttime+ travel_time
    starttime_str = starttime.time().strftime('%H:%M')
    time.append(starttime_str)

    try:
        x = float(Objects[j].recommended_length_of_visit) 
    except ValueError:
        x = 1

    play_time = datetime.timedelta(seconds = x*60)*60
    play_time_str =  str(play_time)[:-3]
    time.append(play_time_str)

    endtime = starttime + play_time
    endtime_str = endtime.time().strftime('%H:%M')
    time.append(endtime_str)


    ## 7 return to start point 
    start = destination
    destination = form.cleaned_data['startStreet'] + " at " +form.cleaned_data['startCrossStreet']

    travel_time = gmaps.distance_matrix(start,destination)["rows"][0]["elements"][0]["duration"]['value']
    travel_time = datetime.timedelta(seconds=travel_time)
    travel_time_str =  str(travel_time)[:-3]
    time.append(travel_time_str)

    totalend = endtime + travel_time
    totalend_str = totalend.time().strftime('%H:%M')

    time.append(totalend_str)

    print(time)
    context["timeline"] = time

    ## transform rate
    if int(Objects[i].rate) !=  Objects[i].rate:
        context['morning_event_rate'] = str(int(Objects[i].rate))+"-half"
    else:
        context['morning_event_rate'] = str(int(Objects[i].rate))

    if int(Objects[j].rate) != Objects[j].rate:
        context['afternoon_event_rate']= str(int(Objects[j].rate))+"-half"
    else:
        context['afternoon_event_rate'] = str(int(Objects[j].rate))

    if int(lunch[y].rate) != lunch[y].rate:
        context['lunch_rate'] = str(int(lunch[y].rate))+"-half"
    else:
        context['lunch_rate'] = str(int(lunch[y].rate))

    total =  Objects[i].cost+ Objects[j].cost + 10
    context['total'] = total

    return render(request, 'planner/home.html', context)



def add_item(request, itemid):
    errors = []
    context = {}
    if request.method == 'POST':
        context['form'] = SearchForm()
        return render(request, 'planner/search.html', context)
    else: 
        print(itemid)
        connection.cursor()
        connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")
        # newItem = Attractions.objects.get(id=itemid)
        # itemAddr = newItem.address
        # itemCate = newItem.category
        # itemCose = newItem.cost
        # itemImgURL = newItem.imageurl
        # itemLat = newItem.lat
        # itemLng = newItem.lng
        # itemLongdes = newItem.longdesc
        # itemName = newItem.name
        # itemRate = newItem.rate
        # itemLength = newItem.recommended_length_of_visit
        # itemShortDes = newItem.shortdesc
        # itemURL = newItem.url
        response_text = serializers.serialize('json', Attractions.objects.all().filter(id = itemid))
    # connection.cursor()
    # connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")
    # response_text = serializers.serialize('json', Attractions.objects.all())
        print("start")
        return HttpResponse(response_text, content_type='application/json')

def get_attrList_json(request):
    # print("yes view")
    connection.cursor()
    connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")
    response_text = serializers.serialize('json', Attractions.objects.all())
    return HttpResponse(response_text, content_type='application/json')



def get_list(request,itemid):
    print(itemid)
    print("yes view")
    connection.cursor()
    connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")
    output = []

    objects = Attractions.objects.filter(category = itemid)

    for o in objects:
        newitem = {}
        newitem['id'] = o.id
        newitem['name'] = o.name
        newitem['imageurl'] = o.imageurl
        newitem['url'] = o.url
        output.append(newitem)

    response_text = json.dumps(output)
    return HttpResponse(response_text, content_type='application/json')


def save(request):
    if request.method == 'POST':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            #Always use get on request.POST. Correct way of querying a QueryDict.
            mon = request.POST.get('mon')
            date = request.POST.get('date')
            dow = request.POST.get("dow")
        
            print(mon)
            print(date)
            print(dow)

            test = InputTest(month=mon,date = date, dow = dow)
            test.save();

    #Get goes hereresponse_text
            output= []
            output["message"] = "ok" 
            response_text =  json.dumps(output)
            return HttpResponse(response_text, content_type='application/json')
























