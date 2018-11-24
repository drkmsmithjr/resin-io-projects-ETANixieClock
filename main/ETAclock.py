#!/usr/bin/python

import NixieTube

import googlemaps

import datetime 
import math
import time
import sys
from time import sleep
from threading import Timer
import pickle

# this timer will sychronize to system time time.time().   Great for clocks
class RepeatedSyncTimer(object):
  def __init__(self, interval ,function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.error = 0.0
    # set this so that the interval is at 50% 0f a second, for clock to update
    # only needed if we have seconds
    self.next_call = math.ceil(time.time()) + 0.5
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args,**self.kwargs)

  def start(self):
    if not self.is_running:
      #syncronize the interval to 50% to allow to account for errors in the timer.
      #the timer interval is adjusted to sychronize with real time.  
      # this is important for clocks.  Above this was set at 50% of the interval
      self.next_call += self.interval
      # test to ensure the self.next_call is greater than time
      # this is important when restarting the time
      if self.next_call < time.time():
         self.next_call = math.ceil(time.time()) + 0.5
         print("we needed to catchup time")
      self._timer = Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False

# in this algorithm.  print the time first, followed by each of the destinations 
# in the Array in order.

def PrtTime(timestr):
    global ind
    global TravelDuration
    global dest
    global TravelDurText
    # transtime determine how long in seconds to display the current ETA or Current time.  
    transtime = 5
    now = datetime.datetime.now()
    seconds = int(now.strftime("%S"))
    seconds = seconds % 10
    DigitSec.Write_Display([seconds])
    #print(seconds)
    # use the mod command to loop through all the destinations and print one at a time. 
    # we can use other functions and sequences to follow different activities.  
    ind2 = int(math.floor(ind/transtime))
    if ind2 >= len(dest):
       print(str(now)+ " " +  "The Current Time " + str(now))
       ind += 1
       if ind2 > len(dest):
          ind = 0
    else:
       ETA = now + datetime.timedelta(seconds=TravelDuration[ind2]) + datetime.timedelta(minutes=ETDdelay)
       print(str(now) + " "+ dest[ind2]['toplace'] + " " + str(ETA) + " Travel Time: " + TravelDurText[ind2])
       ind += 1

def PrtCurrentTimeOneNixie(timestr):
    global ind
    global TravelDuration
    global dest
    global TravelDurText
    # transtime determine how long in seconds to display the current ETA or Current time.  
    now = datetime.datetime.now()
    seconds_1digit = int(now.strftime("%S"))
    seconds_1digit = seconds_1digit % 10
    #DigitSec.Write_Display([seconds_1digit])
    Hour = int(now.strftime("%I"))
    Hour_1digit = int(math.floor(Hour/10.0))
    Hour_2digit = Hour % 10  
    Minute = int(now.strftime("%M"))
    Minute_1digit = int(math.floor(Minute/10.0))
    Minute_2digit = Minute % 10
    time_digits= [Hour_1digit,Hour_2digit,Minute_1digit,Minute_2digit]
    # test is we have twenty four hour time
    
    if ind > 4:
       ind = 0
    if ind == 4:
       z = time_digits[3]
       #DigitSec.Write_Fade_Out()
       time.sleep(.05)
       for y in range (0,10):
          z+=1
          if z > 9:
             z = 0
          DigitSec.Write_Display([z,z,z,z,z,z])
          time.sleep(.0075)
       DigitSec.Display_Off() 
    else:
       #DigitSec.Display_Off()
       #time.sleep(0.02)
       #DigitSec.Ramp_Display([time_digits[ind]])
       #DigitSec.Write_Display([time_digits[ind]])
       if ind == 0:
          #DigitSec.Write_Fade_In([time_digits[ind],time_digits[ind]])
          DigitSec.Write_Display([time_digits[ind],time_digits[ind],time_digits[ind],time_digits[ind],time_digits[ind],time_digits[ind]])
       else:
          #DigitSec.Write_Fade_Out_Fade_In([time_digits[ind],time_digits[ind]])
          DigitSec.Write_Display([time_digits[ind],time_digits[ind],time_digits[ind],time_digits[ind],time_digits[ind],time_digits[ind]])
       print(str(now), time_digits, time_digits[ind])
    ind += 1

def PrtCurrentTimeSixNixie(timestr):
    global ind
    global TravelDuration
    global dest
    global TravelDurText
    global pre_time_digits
    global pre_BlankCntrl

    # how many time to display current time before spin
    time_series = 5
    # after displaying time, provide a spin
    # then display all the locations for this amount of time each (in seconds)
    location_series = 4
    # flow description
    # 1. first time_series seconds, display the time
    # 2. spin display at end of time
    # 3. present each location for location_series seconds (location number, blank, four digits)
    # 3.5 spin at each change of location.   
    # 4. repeat at 1
 
    # transtime determine how long in seconds to display the current ETA or Current time.  
    now = datetime.datetime.now()
    # test to determine if we should be using a ETA
    #print("ind")
    #print(ind)
    ind3 = 0

    if ind-time_series > 0: 
       ind3 = math.floor((ind-time_series) / location_series/1.0)
       ind3 = int(ind3)
       #print("ind3")
       if ind3 >= len(TravelDuration):
          ind3 = len(TravelDuration)-1
       #print(ind3)
       now = now + datetime.timedelta(seconds=TravelDuration[ind3]) + datetime.timedelta(minutes=ETDdelay)

    seconds = int(now.strftime("%S"))
    seconds_1digit = int(math.floor(seconds/10.0))
    seconds_2digit = seconds % 10
    #DigitSec.Write_Display([seconds_1digit])
    Hour = int(now.strftime("%I"))
    Hour_1digit = int(math.floor(Hour/10.0))
    Hour_2digit = Hour % 10  
    Minute = int(now.strftime("%M"))
    Minute_1digit = int(math.floor(Minute/10.0))
    Minute_2digit = Minute % 10
    if ind-time_series <  0:
       time_digits= [Hour_1digit,Hour_2digit,Minute_1digit,Minute_2digit,seconds_1digit,seconds_2digit]
       if Hour_1digit == 1:
          BlankCntrl = []
       else:
          BlankCntrl = [False,True,True,True,True,True]
          #BlankCntrl = [True,True,True,True,True,True] 
    else:
       time_digits = [ind3+1,0,Hour_1digit,Hour_2digit,Minute_1digit, Minute_2digit]
       if Hour_1digit == 1:
          BlankCntrl = [True,False,True,True,True,True]
       else:
          BlankCntrl = [True,False,False,True,True,True]
          
    if ind > time_series + location_series*len(TravelDuration):
       ind = 0
    # spin at end of displaying time or at the end of each location_series display
    if (ind == time_series) or (ind-time_series>0 and ((ind-time_series)%location_series == 0)):
       z = pre_time_digits
       zbc = pre_BlankCntrl
       #DigitSec.Write_Fade_Out()
       time.sleep(.05)
       DigitSec.Write_Spin_Digits(z,BlankCntrl,10)
       #DigitSec.Write_Spin_To_Digits(z,time_digits,zbc, BlankCntrl,5,3)
       DigitSec.Display_Off() 
    else:
       #DigitSec.Display_Off()
       #time.sleep(0.02)
       #DigitSec.Ramp_Display([time_digits[ind]])
       #DigitSec.Write_Display([time_digits[ind]])
       #blink the seconds
       #BlkCntrl2 = BlankCntrl
       if ind-time_series <  0:
          if Hour_1digit == 1:
             DigitSec.Write_Display(time_digits,[True,True,True,True,False,False])
          else:
             DigitSec.Write_Display(time_digits,[False,True,True,True,False,False])
          time.sleep(.05)
       else:
          if Hour_1digit == 1:
             DigitSec.Write_Display(time_digits,[False,False,True,True,True,True])
          else:
             DigitSec.Write_Display(time_digits,[False,False,False,True,True,True])
          time.sleep(.05)
       DigitSec.Write_Display(time_digits,BlankCntrl)
       #print(str(now), time_digits)
       print("Prt-SixNixie: Displayed Time %s"  % str(now))
       print("Prt-SixNixie: tube Display   %s"  % time_digits)
    ind += 1
    if ind > time_series + location_series*len(TravelDuration):
       ind = 0
    pre_time_digits = time_digits
    pre_BlankCntrl = BlankCntrl

def updateETA():
     global clientkey
	 #create the google maps object using the key
     ConnectionOK = True
     try:
        gmaps = googlemaps.Client(key=clientkey)
        #gooogle gmaps will need this key to create the object.   
     except:
        print("There was trouble creating gmaps client key")
        ConnectionOK = False

     for x in range (0,len(dest)):
        now = datetime.datetime.now()
        print(str(now))
        if ConnectionOK:
           directions_result = gmaps.directions(origin=orig,destination = dest[x]['toaddress'], mode = "driving", avoid="tolls", departure_time = now, traffic_model = "best_guess" )
           #directions_result = gmaps.directions(origin=orig,destination = dest[x]['toaddress'], mode = "driving", departure_time = now, traffic_model = "best_guess" )
           TravelDuration[x] = directions_result[0]['legs'][0]['duration']['value']
           TravelDurText[x] = directions_result[0]['legs'][0]['duration']['text']
        else:
           TravelDuration[x] = 1
           TravelDurText[x] = "ERROR"
        #ETA = now + datetime.timedelta(seconds=TravelDuration[x])
        print(dest[x]['toplace'] + " " + " Duration: " + TravelDurText[x])

 
def TimeForBurnIn(BurnInStart, BurnInStop, DigitSec2):
   #global DigitSec
# burnin start and burn in stops are integers that represent 24 hour HOURS
    # MIDNIGHT is represented as zero.   
    # determine if we need to acount for day change:
   TestTime = datetime.datetime.now()
   if BurnInStart < BurnInStop:
      if TestTime.hour >= BurnInStart and TestTime.hour < BurnInStop :
         DigitSec2.BurnIn_On()
         return True
      else:
         DigitSec2.BurnIn_Off()
         return False
   else:
      if (TestTime.hour >= BurnInStart and TestTime.hour < 24) or  (TestTime.hour >= 0 and TestTime.hour < BurnInStop) :
         DigitSec2.BurnIn_On()
         return True
      else:
         DigitSec2.BurnIn_Off()
         return False
   



# Main Loop

# if no parameters are sent with the testdigit.py script, turn on  all nixie's a default
# otherwise, turn them off... this assumes on command line they will be turned on.
GoodArgs = True

if len(sys.argv) < 2:
   print(" Please include google clientkey as parameter")
   GoodArgs = False
else:
   # this key is needed for google maps ETA to work    Need to have a google maps API account.   
   clientkey = sys.argv[1]

#Hard code initial origin and ETA locations
dest = [0,0,0,0]
dest[0] = {'toplace':'trestles','toaddress':'S El Camino Real, San Clemente, CA 92672'}
dest[1] = {'toplace':'huntington','toaddress':'21 Huntington Beach Pier, Huntington Beach, CA 92648'}
dest[2] = {'toplace':'scripts','toaddress':'8564 El Paseo Grande, La Jolla, CA 92037'}
dest[3] = {'toplace':'airport','toaddress':'18601 Airport Way, Santa Ana, CA 92707'}
# clock location address
orig = "25300 Harbor Drive, Dana Point, CA 92629"

locatefile = "/data/locations.txt"

# check to see if the locations.txt file exists.  If it does not then create it.   
# otherwise, read
try:
   with open(locatefile,'r') as f:
      dest,orig = pickle.load(f)
except:
   with open(locatefile,'w') as f:
      pickle.dump((dest,orig),f)

#global parameters for interupt.  Needs to be as larger as dest array below
TravelDuration = [0]*len(dest)
TravelDurText = [0]*len(dest)

# global timer
ind = 0
# timer/ clock update rate in seconds
LoopRate = 1.0

# how long to get actually leave (in minutes)
ETDdelay = 2 
DigitSec = NixieTube.NixieTube('IN-4',6)
DigitSec.Pir_Sensor_On()
pre_time_digits = [0,0,0,0,0,0]
pre_BlankCntrl = [False,False,False,False,False]
      

# start the timer circuit (first parameter is the interval in seconds)
# this circuit will then print the time to the screen and loops through the times 
# 
# this clock will print every second

#rt = RepeatedSyncTimer(LoopRate,PrtCurrentTimeOneNixie,datetime.datetime.now())

rt = RepeatedSyncTimer(LoopRate,PrtCurrentTimeSixNixie, datetime.datetime.now())

#sleep(5)

# start the updateETA routine (in seconds between traffic updates)
updateETATime = 240
# run to initially get ETA
updateETA()
# start time
timerETA = RepeatedSyncTimer(updateETATime,updateETA)
# get the direction results for each destination.  The return is a dict object

print("after timer thread call")

# burnin start time
# burnin stop time


# Burnin Times
BurnInMinutes = 20
BurnInStart = 20
BurnInStop = 23
DigitsToTest = [0,3,4,9,1,2,5,6,7,8]
DigitsTimeTest = [.75,1.5,1.5,.5,.1,.1,.1,.1,.1,.1]
DigIndex = 0
SecIndex = 0
BurnInSec = BurnInMinutes*60
TimerStopped = False
ETATimerStopped = False
TimeForBurnIn(BurnInStart,BurnInStop,DigitSec)


while GoodArgs:

   # HardCode the Burnin
   
      #TestTime = datetime.datetime.now()
   # we  need to set the BurnIn State for DigitSec 
   #if TimeForBurnIn(BurnInStart, BurnInStop):
   #   DigitSec.BurnIn_On()
   #else:
   #   DigitSec.BurnIn_Off()

   print("The Burnin State %s" % DigitSec.BurnIn)

   # if it is time for Burnin then when no movement is detected we want 
   # to turn off the clock timer.   
   # we also want to turn off the timeETA.stop() if no movement is detected
   # so that we can minimize calls to Google Maps.    We will only update
   # traffic when movement is detected.    


   while DigitSec.PIR_SENSE == False:
      # if it is the burnin time
      #if DigitSec.BurnIn: 
         # stop all clocks
      if TimeForBurnIn(BurnInStart,BurnInStop,DigitSec):
         print ("We are stopping all Clocks")
         if TimerStopped == False:
            rt.stop()
            timerETA.stop()
            ind = 0
            TimerStopped = True
         Dig = DigitsToTest[DigIndex]
         DigitSec.Write_Display_No_Off([Dig,Dig,Dig,Dig,Dig,Dig],[True,True,True,True,True,True]) 
         SecIndex += 1
         print("The second Index is: %s" % SecIndex)
         print("The digit Index is:  %s" % DigIndex)
         if SecIndex > BurnInSec*DigitsTimeTest[DigIndex]:
            SecIndex = 0
            DigIndex += 1
            if DigIndex > 9:
               DigIndex = 0  
      else:
         print ("We are stopping only the ETA update clock")
         if ETATimerStopped == False:
            timerETA.stop()
            ETAstoptime = time.time()
            ETATimerStopped = True
      sleep(1)

   if TimerStopped:
      print("Starting All Clocks")
      rt.start()
      timerETA.start()  
      TimerStopped = False
   elif ETATimerStopped:
      print("Starting just the ETA update clock")
      # if the stop time is greater than the update ETA length multiple 
      # then update ETA immediately
      if time.time() - ETAstoptime > updateETATime*.75:
         updateETA()  
      timerETA.start() 
      ETAstarttime = time.time()
      ETATimerStopped = False     
   else:
      print("All timers are on")
   
   # update the trafic every 4 minutes usage to stay under free usage limit 
   sleep(1)
   #break
   

rt.stop()
timerETA.stop()
DigitSec.Power_Off()

# algorithm for the clock

