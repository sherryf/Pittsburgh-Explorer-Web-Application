from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import *
from models import *



# Data model for a Plans
class Attraction(models.Model):
	name      = models.CharField(max_length=100)
	category  = models.CharField(max_length=50)
	imageurl  = models.CharField(max_length=256)
	shortdesc = models.CharField(max_length=256)
	longdesc  = models.CharField(max_length=256)
	rating    = models.DecimalField(blank=True,max_digits=3, decimal_places=2)
	cost      = models.DecimalField(blank=True,max_digits=5, decimal_places=2)
	weburl    = models.CharField(max_length=256)
	latitude  = models.DecimalField(blank=True,max_digits=20, decimal_places=15)
	longitude = models.DecimalField(blank=True,max_digits=20, decimal_places=15)
	rectime   = models.DecimalField(blank=True,max_digits=3, decimal_places=3)
	mintime   = models.DecimalField(blank=True,max_digits=3, decimal_places=3)
	monopentime = models.TimeField(auto_now=False, auto_now_add=False)
	tueopentime = models.TimeField(auto_now=False, auto_now_add=False)
	wedopentime = models.TimeField(auto_now=False, auto_now_add=False)
	thuopentime = models.TimeField(auto_now=False, auto_now_add=False)
	friopentime = models.TimeField(auto_now=False, auto_now_add=False)
	satopentime = models.TimeField(auto_now=False, auto_now_add=False)
	sunopentime = models.TimeField(auto_now=False, auto_now_add=False)
	monclosetime = models.TimeField(auto_now=False, auto_now_add=False)
	tueclosetime = models.TimeField(auto_now=False, auto_now_add=False)
	wedclosetime = models.TimeField(auto_now=False, auto_now_add=False)
	thuclosetime = models.TimeField(auto_now=False, auto_now_add=False)
	friclosetime = models.TimeField(auto_now=False, auto_now_add=False)
	satclosetime = models.TimeField(auto_now=False, auto_now_add=False)
	sunclosetime = models.TimeField(auto_now=False, auto_now_add=False)
	blackoutdate = models.CharField(blank=True,max_length=255)
	phone = models.CharField(blank=True,max_length=20)

	def __unicode__(self):
		return 'id=' + str(self.id) + ',name=' + str(self.name) +')'


# Data model for a Plans
class Plan(models.Model):
	date = models.DateField(auto_now=False, auto_now_add=False)
	startstreet1 = models.CharField(max_length=50)
	startstreet2 = models.CharField(max_length=50)
	starttime = models.TimeField(auto_now=False, auto_now_add=False)
	endtime   = models.TimeField(auto_now=False, auto_now_add=False)
	interest  = models.CharField(max_length=25,blank=True)
	budget    = models.CharField(max_length=25,blank=True)
	isstudent = models.CharField(max_length=25,blank=True)
	transportation = models.CharField(max_length=25,blank=True)
	groupsize = models.PositiveIntegerField(blank=True)
	morningattr = models.ForeignKey(Attraction,default=None,related_name='morningattr')
	lunch       = models.ForeignKey(Attraction,default=None,related_name='lunch')
	afternoonattr = models.ForeignKey(Attraction,default=None,related_name='afternoonattr')
	morningstarttime = models.TimeField(auto_now=False, auto_now_add=False,blank=True)
	lunchstarttime   = models.TimeField(auto_now=False, auto_now_add=False,blank=True)
	afternoonstarttime = models.TimeField(auto_now=False, auto_now_add=False,blank=True)
	morningendtime = models.TimeField(auto_now=False, auto_now_add=False,blank=True)
	lunchendtime   = models.TimeField(auto_now=False, auto_now_add=False,blank=True)
	afternoonendtime = models.TimeField(auto_now=False, auto_now_add=False,blank=True)
	morningduration = models.DecimalField(blank=True,max_digits=3, decimal_places=3)
	lunchduration   = models.DecimalField(blank=True,max_digits=3, decimal_places=3)
	afternoonduration = models.DecimalField(blank=True,max_digits=3, decimal_places=3)
	tb1time = models.DecimalField(blank=True,max_digits=3, decimal_places=3)
	tb2time = models.DecimalField(blank=True,max_digits=3, decimal_places=3)
	tb3time = models.DecimalField(blank=True,max_digits=3, decimal_places=3)
	tb4time = models.DecimalField(blank=True,max_digits=3, decimal_places=3)
	tb1url  = models.CharField(blank=True, max_length=600)
	tb2url  = models.CharField(blank=True, max_length=600)
	tb3url  = models.CharField(blank=True, max_length=600)
	tb4url  = models.CharField(blank=True, max_length=600)
	user = models.ManyToManyField(User)

	def __unicode__(self):
		return 'id=' + str(self.id) + ',user=' + str(self.date) +',user='+str(self.user)+')'

# Data model for userinfo, in order to save personal plans
class UserInfo(models.Model):
    
	# first_name    = models.CharField(max_length=20, blank=True)
	# last_name     = models.CharField(max_length=20, blank=True)
	username      = models.CharField(max_length=20, blank=True) 
	# picture       = models.CharField(blank=True, max_length=256)
	# content_type  = models.CharField(max_length=50, blank=True)
	update_time   = models.DateTimeField(blank=True)
	plans         = models.ManyToManyField(Plan)
	email         = models.CharField(blank=True, max_length=32)                   

	def __unicode__(self):
		return 'UserInfo(id=' + str(self.id) + ',username='+str(self.username)+',plan='+str(self.email) +')'

































