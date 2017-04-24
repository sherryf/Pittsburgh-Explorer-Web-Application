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
import math
import operator


week = ['Monday', 'Tuesday',  'Wednesday', 'Thursday',  'Friday', 'Saturday','Sunday']
month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# Action for the default /planner/ route.
@ensure_csrf_cookie
@login_required
def home(request):
	form = SearchForm()
	context = {}
	curr_user = request.user
	plans  =  Plan.objects.all().filter(user = curr_user)
	print(plans)
	context["plans"] = plans
	print("get in function home for search.html")
	return render(request, 'planner/search.html', {'form':form, 'plans':plans})

@ensure_csrf_cookie
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

    ## connect with google API
    gmaps = googlemaps.Client(key='AIzaSyAn-6XiiENx0RGqGcI8_BjKzTUUQAiI7T8')

    ## get geocode for start place 
    ## Center Street & Morewood Street reformat starting point 
    # [Street Name A] & [Street Name B], City]
    geocode_result = gmaps.geocode(form.cleaned_data['startStreet'] + " & " + form.cleaned_data['startCrossStreet'] + ", Pittsburgh")
    if len(geocode_result) == 0 :
        context['form'] = SearchForm()
        context['error'] = "Wrong Address!"
        return render(request, 'planner/search.html', context)

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
    context['start'] =  form.cleaned_data['startStreet'] + " & "+ form.cleaned_data['startCrossStreet']

    ## get interest to perform search 
    interest = form.cleaned_data['interest']
    context['interest'] = interest ## return interest back 

    ## get budget constraint
    if form.cleaned_data['budget'] == 'Bankrupt':
        cost_limit = 10
    elif form.cleaned_data['budget'] == 'Economy':
        cost_limit = 20
    elif form.cleaned_data['budget'] == 'Salary Day':
        cost_limit = 1000

    ## OperationalError: Could not decode to UTF-8 column 'ShortDesc' with text
    connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")

    ## search for all objects that in the interest category and below budget constraint
    Objects = Attractions.objects.all().filter(cost__lte = cost_limit).filter(category = interest)

    ## if no objects satisfy 
    if Objects.count() < 1 :
        context['form'] = form
        context['Error'] = "No activities match your choice!"
        return render(request, 'planner/search.html', context)

    ## random select two options for morning and afternoon 
    ## distance of all objects
    distance_rank = {}
    for o in Objects:
        dis = math.pow(o.lat - context['slat'],2) + math.pow(o.lng - context['slng'],2)
        distance_rank[o.id] = dis
    

    
    ## sort list in distance 
    sorted_distance_rank = sorted(distance_rank.iteritems(), key=operator.itemgetter(1), reverse=True)
    

    for i in range(0,len(sorted_distance_rank)):
        distance_rank[sorted_distance_rank[i][0]]= i+1 


    object_rank = {}

    for o in Objects:
        
        score = 0.5 * distance_rank[o.id]+  0.5 * o.rate
        object_rank[o.id] =  score

    

    distance_rank = sorted(distance_rank.items(), key=operator.itemgetter(1), reverse=True)
    

    i = distance_rank[0][0]
    j = distance_rank[1][0]
 
    ## return objects, morning event, afternoon event
    context['morning_event'] = Attractions.objects.all().filter(id  = i)[0]
    context['afternoon_event']= Attractions.objects.all().filter(id  = j)[0]
    id1 = i
    id2 = j
    context['objects'] = Attractions.objects.all().filter(cost__lte = cost_limit).filter(category = interest).exclude(id__in = [id1,id2])

    ## find lunch 
    lunch  =  Attractions.objects.all().filter(category = "Restaurant").filter(cost__lte = cost_limit)

    lunch_distance_rank = {}

    for l in lunch:
        dis_1 = math.pow(l.lat - context['morning_event'].lat,2) + math.pow(l.lng - context['morning_event'].lng,2) 
        print(l.lat)
        print(context['morning_event'].lat)
        print(dis_1)
        dis_2 = math.pow(l.lat - context['afternoon_event'].lat,2) + math.pow(l.lng - context['afternoon_event'].lng,2)
        print(dis_2)

        lunch_distance_rank[l.id] = (dis_1 + dis_1)/2

    

     ## sort list in distance 
    sorted_lunch_distance_rank = sorted(lunch_distance_rank.iteritems(), key=operator.itemgetter(1), reverse=True)


    for i in range(0,len(sorted_lunch_distance_rank)):
        lunch_distance_rank[sorted_lunch_distance_rank[i][0]]= i+1 


    lunch_object_rank = {}

    for l in lunch:
        score = 0.5 * lunch_distance_rank[l.id]+  0.5 * l.rate
        lunch_object_rank[l.id] =  score


    lunch_object_rank = sorted(lunch_object_rank.items(), key=operator.itemgetter(1), reverse=True)
    ##import pdb; pdb.set_trace();

    y = lunch_object_rank[0][0]
    context['lunch'] =  Attractions.objects.all().filter(id = y)[0]

    ## calculate for travel ban 

    ##distance_matrix
    time = []
    ## 1 start place to morning event
    start = form.cleaned_data['startStreet'] + " at " +form.cleaned_data['startCrossStreet']
    destination  = context['morning_event'].address

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

    ## incase missing value
    try:
        x = float(context['morning_event'].recommended_length_of_visit)
    except ValueError:
        x = 1

    play_time = datetime.timedelta(seconds = x*60*60)
    play_time_str =  str(play_time)[:-3]
    time.append(play_time_str)

    ## 3 morning event to lunch 
    starttime = starttime + play_time
    starttime_str = starttime.time().strftime('%H:%M')
    time.append(starttime_str)

    start = destination
    destination = context['lunch'].address

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

    ## incase missing value
    try:
        x = float(context['lunch'].recommended_length_of_visit)
    except ValueError:
        x = 1


    lunch_time = datetime.timedelta(seconds = x*60*60)
    lunch_time_str = str(lunch_time)[:-3]
    time.append(lunch_time_str)

    ## 5 lunch event to afternoon_event 
    starttime = starttime + lunch_time
    starttime_str = starttime.time().strftime('%H:%M')
    time.append(starttime_str)

    start = destination
    destination = context['afternoon_event'].address

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
        x = float(context['afternoon_event'].recommended_length_of_visit) 
    except ValueError:
        x = 1

    play_time = datetime.timedelta(seconds = x*60*60)
    play_time_str = str(play_time)[:-3]
    time.append(play_time_str)

    endtime = starttime + play_time
    endtime_str = endtime.time().strftime('%H:%M')
    time.append(endtime_str)


    ## 7 return to start point 
    start = destination
    destination = form.cleaned_data['startStreet'] + " at " +form.cleaned_data['startCrossStreet']

    travel_time = gmaps.distance_matrix(start,destination)["rows"][0]["elements"][0]["duration"]['value']
    travel_time = datetime.timedelta(seconds=travel_time)
    travel_time += datetime.timedelta(seconds=1800)
    travel_time_str =  str(travel_time)[:-3]
    time.append(travel_time_str)

    totalend = endtime + travel_time
    totalend_str = totalend.time().strftime('%H:%M')

    time.append(totalend_str)

    print(time)
    context["timeline"] = time

    ## transform rate
    if int(context['morning_event'].rate) !=  context['morning_event'].rate:
        context['morning_event_rate'] = str(int(context['morning_event'].rate))+"-half"
    else:
        context['morning_event_rate'] = str(int(context['morning_event'].rate))

    if int(context['afternoon_event'].rate) != context['afternoon_event'].rate:
        context['afternoon_event_rate']= str(int(context['afternoon_event'].rate))+"-half"
    else:
        context['afternoon_event_rate'] = str(int(context['afternoon_event'].rate))

    if int(context['lunch'].rate) != context['lunch'].rate:
        context['lunch_rate'] = str(int(context['lunch'].rate))+"-half"
    else:
        context['lunch_rate'] = str(int(context['lunch'].rate))

    total =  context['morning_event'].cost+ context['afternoon_event'].cost + context['lunch'].cost
    context['total'] = total

    context["budget"] = form.cleaned_data['budget']     
    context["estimateDate"] = form.cleaned_data['estimateDate']
    context["plannid"] = ""

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


# @csrf_exempt
def save(request):
    if request.method == 'POST':
        output= {}
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            #Always use get on request.POST. Correct way of querying a QueryDict.
            time = request.POST.get("estimateDate")
            # validate time 
            try:
                datetime.datetime.strptime(time, '%B %d, %Y')
            except ValueError:
                output["message"] = "Wrong Date" 
                response_text =  json.dumps(output)
                return HttpResponse(response_text, content_type='application/json')

            # get all     
            objects = json.loads(request.POST.get("objects"))
        
            ## validate start time 
            starttime = request.POST.get("starttime")
            timeformat = "%H:%M"
            try:
                validtime = datetime.datetime.strptime(caminput1, timeformat)
            except ValueError:
                output["message"] = "Wrong Time" 
                response_text =  json.dumps(output)
                return HttpResponse(response_text, content_type='application/json')

            # validate budget
            budget = request.POST.get("budget")
            if budget not in ["Bankrupt","Economy","Salary Day"]:
                output["message"] = "Wrong Budget" 
                response_text =  json.dumps(output)
                return HttpResponse(response_text, content_type='application/json')

            # validate interest
            interest = request.POST.get("interest")
            if interest not in ["Museums","Parks","Sights","WaterSports","Concerts","Fun&Games","Outdoor","Shopping","Workshops","Tour"]:
                output["message"] = "Wrong Interest" 
                response_text =  json.dumps(output)
                return HttpResponse(response_text, content_type='application/json')

            # validate itemcount 
            itemcount = int(request.POST.get("itemCount"))
            if itemcount > 5:
                output["message"] = "Itemcount greater than 5" 
                response_text =  json.dumps(output)
                return HttpResponse(response_text, content_type='application/json')
            
            start = request.POST.get("start")

            formated_object = {}

            connection.cursor()
            connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")

            for i in range(1,itemcount+1):
                o = json.loads(objects[str(i)])
                # import pdb; pdb.set_trace();
                try:
                    formated_object ["event" + str(i)] = Attractions.objects.all().get(id =int(o["id"]))
                except DoesNotExist:
                    output= {}
                    output["message"] = "Wrong Information" 
                    response_text =  json.dumps(output)
                    return HttpResponse(response_text, content_type='application/json')

                if o["duration"][:-1][o["duration"][:-1].index(":")+1:] == "00" :
                    formated_object["duration" + str(i)] =float(o["duration"][:-1][:o["duration"][:-1].index(":")])
                else:
                    formated_object["duration" + str(i)] =float(o["duration"][:-1][:o["duration"][:-1].index(":")] + ".5")
                   
            for i in range(itemcount+1, 5 + 1):
                formated_object["event" + str(i)] = None
                formated_object["duration" + str(i)] = None

            # import pdb; pdb.set_trace();
            time = datetime.datetime.strptime(time,'%B %d, %Y').date()

            if request.POST.get("plan_id") == "":
                new_plan = Plan(date=time, 
                                start = start,
                                starttime =  starttime,
                                interest = interest,
                                budget = budget,
                                event1 = formated_object["event1"],
                                event2 = formated_object["event2"],
                                event3 = formated_object["event3"],
                                event4 = formated_object["event4"],
                                event5 = formated_object["event5"],
                                duration1 = formated_object["duration1"],
                                duration2 = formated_object["duration2"],
                                duration3 = formated_object["duration3"],
                                duration4 = formated_object["duration4"],
                                duration5 = formated_object["duration5"])
                new_plan.save()
                # import pdb; pdb.set_trace()
                new_plan.user.add(User.objects.get(username = request.user))
                new_plan.save()

                ui = UserInfo.objects.get(username = User.objects.get(username = request.user).username)
                ui.plans.add(new_plan)
                ui.save()
            else:
                try:
                    obj = Plan.objects.get(id=equest.POST.get("plan_id"))
                    ## check if the user has right to change a existing plan
                    if plan_id in UserInfo.objects.get(username = User.objects.get(username = request.user).username).plan:
                        obj.date = time
                        obj.start = start
                        obj.starttime =  starttime,
                        obj.interest = interest,
                        obj.budget = budget,
                        obj.event1 = formated_object["event1"]
                        obj.event2 = formated_object["event2"]
                        obj.event3 = formated_object["event3"]
                        obj.event4 = formated_object["event4"]
                        obj.event5 = formated_object["event5"]
                        obj.duration1 = formated_object["duration1"]
                        obj.duration2 = formated_object["duration2"]
                        obj.duration3 = formated_object["duration3"]
                        obj.duration4 = formated_object["duration4"]
                        obj.duration5 = formated_object["duration5"]
                        obj.save()
                    else:
                        output["error"] = "Wrong Information" 
                except Model.DoesNotExist:
                    output["error"] = "Wrong Information" 

            output= {}
            output["message"] = "ok" 
            output["plan_id"] = new_plan.id
            response_text =  json.dumps(output)
            return HttpResponse(response_text, content_type='application/json')
    response_text = []
    return render_to_response(response_text, 'planner/search.html',context_instance = RequestContext(request))

def get_plan(request, planid):
	print("gettinginto get_plan");

	## OperationalError: Could not decode to UTF-8 column 'ShortDesc' with text
	connection.cursor()
	connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")

	context = {}
	plan = Plan.objects.get(id = planid)

	## connect with google API
	gmaps = googlemaps.Client(key='AIzaSyAn-6XiiENx0RGqGcI8_BjKzTUUQAiI7T8')

	## get geocode for start place
	start = plan.start
	fuhao = start.index("&")
	startStreet = start[0:fuhao]
	startCrossStreet = start[(fuhao+1):len(start)]
	geocode_result = gmaps.geocode(startStreet + " at " +startCrossStreet)
	geocode = geocode_result[0]['geometry']['location']
	context['slat'] = geocode_result[0]['geometry']['location']['lat'] ## get start place lat
	context['slng']= geocode_result[0]['geometry']['location']['lng'] ## get start place lng
	context['start'] = start

	## split estimateDate to Month, Day, Day of Week
	datetime_object = plan.date
	context['mon'] = month[datetime_object.month-1]
	context['date']= datetime_object.day
	context['dow'] = week[datetime_object.weekday()]

	## get start time
	context['startTime'] = plan.starttime

	## get events
	context['event1'] = plan.event1
	context['event2'] = plan.event2
	context['event3'] = plan.event3
	context['event4'] = plan.event4
	context['event5'] = plan.event5

	## search for all objects
	Objects = Attractions.objects.all()
	## calculate for travel ban

	##distance_matrix

	time = []
	## 1 start place to morning event
	destination  = plan.event1.address
	if destination == "":
		destination = "875 Greentree Rd #106, Pittsburgh, PA 15220"

	time.append(str(plan.starttime)[:-3])

	print(start)
	print(destination)
	travel_time = gmaps.distance_matrix(start,destination)["rows"][0]["elements"][0]["duration"]['value']
	travel_time = datetime.timedelta(seconds=travel_time+1800)
	travel_time_str =  str(travel_time)[:-3]
	time.append(travel_time_str)


	## 2 event1 and stay at event1
	starttime = datetime.datetime.combine(datetime.date(1, 1, 1), plan.starttime)+ travel_time
	starttime_str = starttime.time().strftime('%H:%M')
	time.append(starttime_str)

	try:
		x = float(plan.event1.recommended_length_of_visit)
	except ValueError:
		x = 1

	play_time = datetime.timedelta(seconds = x *60)*60
	play_time_str =  str(play_time)[:-3]
	time.append(play_time_str)

	## 3 event1 to event2
	starttime = starttime + play_time
	starttime_str = starttime.time().strftime('%H:%M')
	time.append(starttime_str)

	start = destination
	destination = plan.event2.address

	if destination == "":
		destination = "875 Greentree Rd #106, Pittsburgh, PA 15220"

	print(start)
	print(destination)

	travel_time = gmaps.distance_matrix(start,destination)["rows"][0]["elements"][0]["duration"]['value']
	travel_time = datetime.timedelta(seconds=travel_time+1800)
	travel_time_str =  str(travel_time)[:-3]
	time.append(travel_time_str)

	## 4 event2 event and stay
	starttime = starttime+ travel_time
	starttime_str = starttime.time().strftime('%H:%M')
	time.append(starttime_str)

	try:
		x = float(plan.event3.recommended_length_of_visit)
	except ValueError:
		x = 1

	play_time = datetime.timedelta(seconds = 60*60)
	play_time_str = str(play_time)[:-3]
	time.append(play_time_str)

	## 5 event 2 to event 3
	starttime = starttime + play_time
	starttime_str = starttime.time().strftime('%H:%M')
	time.append(starttime_str)

	start = destination
	destination = plan.event3.address

	if destination == "":
		destination = "875 Greentree Rd #106, Pittsburgh, PA 15220"

	print(start)
	print(destination)

	travel_time = gmaps.distance_matrix(start,destination)["rows"][0]["elements"][0]["duration"]['value']
	travel_time = datetime.timedelta(seconds=travel_time+1800)
	travel_time_str =  str(travel_time)[:-3]
	time.append(travel_time_str)

	## 6 event3  event to stay

	starttime = starttime+ travel_time
	starttime_str = starttime.time().strftime('%H:%M')
	time.append(starttime_str)

	try:
		x = float(plan.event3.recommended_length_of_visit)
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
	destination = startStreet+ " at " + startCrossStreet

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
	if int(plan.event1.rate) !=  plan.event1.rate:
		context['event1_rate'] = str(int(plan.event1.rate))+"-half"
	else:
		context['event1_rate'] = str(int(plan.event1.rate))

	if int(plan.event2.rate) != plan.event2.rate:
		context['event2_rate']= str(int(plan.event2.rate))+"-half"
	else:
		context['event2_rate'] = str(int(plan.event2.rate))

	if int(plan.event3.rate) != plan.event3.rate:
		context['event3_rate'] = str(int(plan.event3.rate))+"-half"
	else:
		context['event3_rate'] = str(int(plan.event3.rate))

	# if int(event4.rate) != event4.rate:
	#     context['event4_rate'] = str(int(event4.rate))+"-half"
	# else:
	#     context['event4_rate'] = str(int(event4.rate))

	# if int(event5.rate) != event5.rate:
	#     context['event5_rate'] = str(int(event5.rate))+"-half"
	# else:
	#     context['event5_rate'] = str(int(event5.rate))

	total =  plan.event1.cost+ plan.event2.cost + plan.event3.cost
	context['total'] = total

	context["budget"] = plan.budget
	context["estimateDate"] = plan.date



	 # send the current users all plan ids back
	curr_user=request.user
	plans  =  Plan.objects.all().filter(user = curr_user)
	context["plans"] = plans
	context["currplan"] = plan
	ui = UserInfo.objects.get(username = User.objects.get(username = request.user).username)
	context["ui"] = ui

	print("get plan function ended")
	return render(request, 'planner/plan.html', context)

















