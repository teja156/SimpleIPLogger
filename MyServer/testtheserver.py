import requests
import re

def validate_url(url):
	regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

	return re.match(regex,url) is not None


op = int(input("1. Shorten URL\n2. Track URL\nEnter option : "))

if(op==1):
	inp = input(">Enter URL to shorten : ")
	if(not(validate_url(inp))):
		print("URL format is wrong, try again. (include http/https)")
	else:
		data = {'URL':inp}
		r = requests.post('http://127.0.0.1:8000/shorten/',data=data)
		print(r.text)

if(op==2):
	inp = input("Enter Tracking LINK : ")
	r = requests.get(inp)
	print(r.text)
