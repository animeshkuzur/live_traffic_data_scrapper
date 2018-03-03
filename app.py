import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from threading import Thread
from time import sleep
from decimal import Decimal, getcontext

class Coordinates(object):
	def __init__(self,lat,log):
		self._lat = lat
		self._log = log

	def get_lat(self):
		return self._lat

	def get_log(self):
		return self._log

class Crawl(object):
	def __init__(self):
		pass

class App(Coordinates):
	
	def __init__(self,tl,tr,bl,br):
		self._lat_diff=Decimal(0)
		self._log_diff=Decimal(0)
		self.callibrate();

	def get_url(self,lat,lng):
		url = "https://adzippy.com/traffic/data?lat="+lat+"&long="+lng
		return url

	def callibrate(self):
		print("\nInitiating Callibration")
		browser = webdriver.Firefox()
		browser.get(self.get_url(tl.get_lat(),tl.get_log()))
		top=browser.find_element_by_id("tl").text
		bottom=browser.find_element_by_id("bl").text
		left=browser.find_element_by_id("ll").text
		right=browser.find_element_by_id("rl").text
		browser.quit()
		print(top,bottom,left,right)
		map_parts = self.compute(top,bottom,left,right)
		print(str(map_parts)+" total windows")
		
		return 0

	def compute(self,top,bottom,left,right):
		getcontext().prec = 6
		#print(Decimal(top),Decimal(tl.get_lat()))
		lat_diff1 = abs(Decimal(top)-Decimal(tl.get_lat()))
		lat_diff2 = abs(Decimal(bottom)-Decimal(tl.get_lat()))
		print(lat_diff1,lat_diff2)
		lat_diff = min(lat_diff1,lat_diff2)
		a=Decimal(tl.get_lat())
		self._lat_diff=a;
		x=0
		while(a>Decimal(bl.get_lat())):
			a=a-Decimal(lat_diff*2)
			x=x+1
		print(str(x)+" column windows")
		
		log_diff1 = abs(Decimal(left)-Decimal(tl.get_log()))
		log_diff2 = abs(Decimal(right)-Decimal(tl.get_log()))
		print(log_diff1,log_diff2)
		log_diff = min(log_diff1,log_diff2)
		b=Decimal(tl.get_log())
		y=0
		self._log_diff=b;
		while(b<Decimal(tr.get_log())):
			b=b+Decimal(log_diff*2)
			y=y+1
		print(str(y)+" row windows")
		return x*y

	def start(self,):
		return 0

print("Enter the co-ordinates")
print("\n-----Top left-----")
temp_lat = input('lat: ')
temp_long = input('long: ')
tl=Coordinates(temp_lat,temp_long)

print("\n-----Top right-----")
temp_lat = input('lat: ')
temp_long = input('long: ')
tr=Coordinates(temp_lat,temp_long)

print("\n-----Bottom right-----")
temp_lat = input('lat: ')
temp_long = input('long: ')
br=Coordinates(temp_lat,temp_long)

print("\n-----Bottom left-----")
temp_lat = input('lat: ')
temp_long = input('long: ')
bl=Coordinates(temp_lat,temp_long)

x=App(tl,tr,br,bl)