from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from MyServer.models import *


import string 
import random
import re
from datetime import datetime
import json
import os

# TRACKING_DOMAIN_NAME = "http://127.0.0.1:8000/tracking"
# DOMAIN_NAME = "http://127.0.0.1:8000"
TRACKING_DOMAIN_NAME = os.environ.get('TRACKING_DOMAIN_NAME')
DOMAIN_NAME = os.environ.get('DOMAIN_NAME')


# Create your views here.

def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_data(request):
	browser = request.user_agent.browser.family + " "+ request.user_agent.browser.version_string
	os = request.user_agent.os.family + " "+ request.user_agent.os.version_string
	device = request.user_agent.device.family

	device_type=""

	if(request.user_agent.is_mobile):
		device_type="Mobile"

	if(request.user_agent.is_tablet):
		device_type="Tablet"

	if(request.user_agent.is_pc):
		device_type="PC/Laptop"

	if(request.user_agent.is_bot):
		device="bot"

	resp = {"browser":browser,"os":os,"device_type":device_type,"device":device}

	print(resp)
	return resp



@csrf_exempt
def create_shortened_url(request):
	original_url = request.POST['URL']
	random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
	random_chars2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))

	#append to domain name
	shortened_link = DOMAIN_NAME + "/" + random_chars
	tracking_link = TRACKING_DOMAIN_NAME + "/" + random_chars2

	#What if randomly generated chars already exist?
	#Check the url in db before comitting - FUTUTRE WORK

	
	#Store in the DB
	store_links = Links(short_url=shortened_link,redirect_url=original_url,tracking_url=tracking_link)
	store_links.save()

	print("LINK SHORTENED : ",shortened_link)
	# return JsonResponse({'shortened_link':shortened_link,'tracking_link':tracking_link})
	return render(request,'index.html',context={'shortened_link':shortened_link,'tracking_link':tracking_link})


def redirect_test(request):
	return redirect("https://facebook.com")

def ip_test(request):
	return HttpResponse(get_client_ip(request))

def user_agent_test(request):
	browser = request.user_agent.browser.family
	os = request.user_agent.os.family
	device = request.user_agent.device.family

	if(request.user_agent.is_pc):
		device = "PC"
	return HttpResponse(browser+"\n"+os+" "+device)


def redirect_now(request,short_link):
	shortened_link = DOMAIN_NAME + "/" + short_link.strip()

	#fetch for this in DB and retrieve the redirect URL
	fetched = Links.objects.filter(short_url=shortened_link)[0]

	redirect_url = formaturl(fetched.redirect_url)

	client_data = get_client_data(request)

	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


	#Before redirecting, log neccessary data into DB
	log_data = TrackingData(tracking_url=fetched.tracking_url,short_url=shortened_link,
		ip_address=get_client_ip(request),browser=client_data['browser'],os=client_data['os']
		,device_type=client_data['device_type'],device=client_data['device'],time=dt_string)

	log_data.save()


	return redirect(redirect_url)


def fetch_tracking_data(request,tracking_link):
	tracking_url = TRACKING_DOMAIN_NAME + "/" + tracking_link.strip()
	fetch = TrackingData.objects.filter(tracking_url=tracking_url)

	res = []
	k = 1
	for row in fetch:
		
		temp = {}
		temp['ip_address'] = row.ip_address
		temp['browser'] = row.browser
		temp['os'] = row.os
		temp['device_type'] = row.device_type
		temp['device'] = row.device
		temp['time'] = row.time

		res.append(temp)
		# res['Device'+str(k)] = temp
		# k+=1



	# return JsonResponse(json.dumps(res),safe=False)
	print("resp : ",res)
	return render(request,'tracking_display.html',{'resp':res,'shortened_link':fetch[0].short_url})


def home(request):
	return render(request,'index.html')

