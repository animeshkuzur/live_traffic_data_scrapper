import sys
import os
import shutil
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from threading import Thread
#from time import sleep
from decimal import Decimal, getcontext

from config import TOP_LAT, TOP_LOG, BOTTOM_LAT, BOTTOM_LOG

class Coordinates(object):
	def __init__(self,lat,log):
		self._lat = lat
		self._log = log

	def get_lat(self):
		return self._lat

	def get_log(self):
		return self._log

	def get_url(self):
		return "https://adzippy.com/traffic/data?lat="+self._lat+"&long="+self._log

class Crawl(Coordinates):
	def __init__(self,obj,c):
		self._point = obj
		self._c = str(c)
		self._dict={}

		self._top=""
		self._bottom=""
		self._left=""
		self._right=""

		self._thread_dict={}
		self._browser = webdriver.Firefox()


	def scrapper(self):
		while True:
			time.sleep(240)
			print("refeshing browser:"+self._c)
			self._browser.refresh()
			time.sleep(60)
			t = time.strftime("%H:%M:%S")
			print("window "+self._c+" screenshot : "+t)
			self._browser.save_screenshot("./data/"+self._c+"/"+t+".png")

	def run(self):
		# browser = webdriver.Firefox()
		self._browser.maximize_window()
		self._browser.get(self._point.get_url())
		self._top=self._browser.find_element_by_id("tl").text
		self._bottom=self._browser.find_element_by_id("bl").text
		self._left=self._browser.find_element_by_id("ll").text
		self._right=self._browser.find_element_by_id("rl").text
		print("Creating description file...")
		file = open("./data/"+self._c+"/DESC","w")
		file.write(self._top+"\n")
		file.write(self._bottom+"\n") 
		file.write(self._left+"\n")
		file.write(self._right+"\n")
		file.close()

		print("Creating a new Thread...")
		self._thread_dict[self._c]=Thread(target=self.scrapper, args=())
		self._thread_dict[self._c].start()

		return 0

class App(Coordinates):	
	def __init__(self,tl,tr,bl,br):
		self._lat_diff=Decimal(0)
		self._log_diff=Decimal(0)
		self.callibrate()

	def check_dir(self,name):
		flag = 0
		if not os.path.exists(name):
			flag = 0
		else:
			flag = 1
		return flag

	def callibrate(self):
		print("\nInitiating Callibration")
		if not self.check_dir("data"):
			os.makedirs("data")
		browser = webdriver.Firefox()
		browser.maximize_window()
		browser.get(tl.get_url())
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
		lat_diff1 = abs(Decimal(top)-Decimal(tl.get_lat()))
		lat_diff2 = abs(Decimal(bottom)-Decimal(tl.get_lat()))
		print(lat_diff1,lat_diff2)
		lat_diff = min(lat_diff1,lat_diff2)
		a=Decimal(tl.get_lat())
		self._lat_diff=lat_diff;
		x=0
		while(a>Decimal(bl.get_lat())):
			a=a-Decimal(lat_diff*2)
			x=x+1
		print(str(x)+" rows windows")
		
		log_diff1 = abs(Decimal(left)-Decimal(tl.get_log()))
		log_diff2 = abs(Decimal(right)-Decimal(tl.get_log()))
		print(log_diff1,log_diff2)
		log_diff = min(log_diff1,log_diff2)
		b=Decimal(tl.get_log())
		y=0
		self._log_diff=log_diff;
		while(b<Decimal(tr.get_log())):
			b=b+Decimal(log_diff*2)
			y=y+1
		print(str(y)+" column windows")
		return x*y

	def start(self):
		dict={}
		getcontext().prec = 6
		temp_lat=Decimal(tl.get_lat())
		c=0
		while(temp_lat>=Decimal(bl.get_lat())): #Decimal(bl.get_lat())
			temp_long=Decimal(tl.get_log())
			while(temp_long<=Decimal(tr.get_log())):
				c+=1
				print("\nProcessing Block Number: ",c)
				print("------------------------")
				if not self.check_dir("data/"+str(c)):
					os.makedirs("data/"+str(c))
				temp_long=temp_long+(self._log_diff*2)
				dict[c]=Coordinates(str(temp_lat),str(temp_long))
				print("creating object ",c)
				Crawl(dict[c],c).run()
			temp_lat=temp_lat-(self._lat_diff*2)
			break #temp
		return 0

print("checking previous cache data")
if os.path.exists("data"):
	print("clearing cache data\n")
	shutil.rmtree("data", ignore_errors=True)

print("Co-ordinates")
print("\n-----Top left-----")
print(TOP_LAT,TOP_LOG)
tl=Coordinates(TOP_LAT,TOP_LOG)

print("\n-----Top right-----")
print(TOP_LAT,BOTTOM_LOG)
tr=Coordinates(TOP_LAT,BOTTOM_LOG)

print("\n-----Bottom right-----")
print(BOTTOM_LAT,BOTTOM_LOG)
br=Coordinates(BOTTOM_LAT,BOTTOM_LOG)

print("\n-----Bottom left-----")
print(BOTTOM_LAT,TOP_LOG)
bl=Coordinates(BOTTOM_LAT,TOP_LOG)

x=App(tl,tr,br,bl)
x.start()