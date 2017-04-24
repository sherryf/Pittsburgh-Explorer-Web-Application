from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import *
from models import *

class Attractions(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    category = models.TextField(db_column='Category', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    imageurl = models.TextField(db_column='ImageURL', blank=True, null=True)  # Field name made lowercase.
    shortdesc = models.TextField(db_column='ShortDesc', blank=True, null=True)  # Field name made lowercase.
    recommended_length_of_visit = models.TextField(db_column='Recommended_length_of_visit', blank=True, null=True)  # Field name made lowercase.
    rate = models.FloatField(db_column='Rate', blank=True, null=True)  # Field name made lowercase.
    geocode = models.TextField(db_column='Geocode', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    lat = models.TextField(db_column='Lat', blank=True, null=True)  # Field name made lowercase. 
    lng = models.TextField(db_column='Lng', blank=True, null=True)  # Field name made lowercase. 
    url = models.TextField(db_column='URL', blank=True, null=True)  # Field name made lowercase.
    longdesc = models.TextField(db_column='LongDesc', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase. 

    class Meta:
        managed = True
        db_table = 'Attractions'


# Data model for a Plans
class Plan(models.Model):
	date = models.DateField(auto_now=False, auto_now_add=False)
	user = models.ManyToManyField(User)
	start = models.CharField(max_length=50)
	starttime = models.TimeField(auto_now=False, auto_now_add=False)
	interest  = models.CharField(max_length=25,blank=True)
	budget    = models.CharField(max_length=25,blank=True)
	event1 = models.ForeignKey(Attractions,related_name='event1',null=True)
	event2 = models.ForeignKey(Attractions,related_name='event2',null=True)
	event3 = models.ForeignKey(Attractions,related_name='event3',null=True)
	event4 = models.ForeignKey(Attractions,related_name='event4',null=True)
	event5 = models.ForeignKey(Attractions,related_name='event5',null=True)
	duration1 = models.DecimalField(blank=True,max_digits=3, decimal_places = 1,null=True)
	duration2 = models.DecimalField(blank=True,max_digits=3, decimal_places = 1,null=True)
	duration3 = models.DecimalField(blank=True,max_digits=3, decimal_places = 1,null=True)
	duration4 = models.DecimalField(blank=True,max_digits=3, decimal_places = 1,null=True)
	duration5 = models.DecimalField(blank=True,max_digits=3, decimal_places = 1,null=True)
	

	def __unicode__(self):
		return 'id=' + str(self.id) + ',user=' + str(self.date) +',user='+str(self.user)+')'

# Data model for userinfo, in order to save personal plans
class UserInfo(models.Model):
    
	# first_name    = models.CharField(max_length=20, blank=True)
	# last_name     = models.CharField(max_length=20, blank=True)
	username      = models.CharField(max_length=20, blank=True) 
	# picture       = models.CharField(blank=True, max_length=256)
	# content_type  = models.CharField(max_length=50, blank=True)
	# update_time   = models.DateTimeField(blank=True)
	plans         = models.ManyToManyField(Plan)
	email         = models.CharField(blank=True, max_length=32)                   

	def __unicode__(self):
		return 'UserInfo(id=' + str(self.id) + ',username='+str(self.username)+',plan='+str(self.email) +')'


class InputTest(models.Model):
	month = models.CharField(max_length=20,blank = True)
	date = models.IntegerField(blank = True)
	dow = models.CharField(max_length=20,blank = True)






























