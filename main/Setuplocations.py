#!/usr/bin/python

import pickle
import sys

# load the destinations and origins

locatefile = "/data/locations.txt"

# main loop
# the datafile can be at another location .. for debug

if len(sys.argv) < 2:
#blank digits
   locatefile = "/data/locations.txt"
else:
   locatefile = sys.argv[1]

# check to see if the locations.txt file exists.  If it does not then create it.   
# otherwise, read
try:
   with open(locatefile,'r') as f:
      dest,orig = pickle.load(f)
except:
   dest = []
   orig = "NEED ORIGIN"


while True:

   print("SET THE ETA LOCATIONS FOR CLOCK \n")
   print("The clock original address is: %s \n" % orig)
   print("The ETA locations:")
   #
   for index,x in enumerate(dest):
      output = str(index+1) + ": "
      output = output + x['toplace'] + ": " + x['toaddress']
      print(output)

   print("\n[A]: Add a location:")
   print("[R]: Remove a location:")
   print("[M]: Move a location up:")
   print("[O]: Set the Origin:")
   print("[W]: Write the locations file")
   print("[x]: Write and exit")
   
   raw_option = raw_input("")
   if raw_option == "A":
      if len(dest) > 8:
         print("You are at the maximum ETA: Remove on first and try again")
      else: 
         while True:
            raw_option3 = raw_input("What is the name (i.e. work, airport)?: ")
            raw_option2 = raw_input("Enter Google Address: ")
            try:
               # add a google address check
               dest.append({'toplace':str(raw_option3),'toaddress':str(raw_option2)})
               break
            except ValueError:
               print ("This is not a valid address.  Please try again")
   elif raw_option == "R":
      while True:
         raw_option2 = raw_input("Enter the Address to remove [1-%s]: " % len(dest))
         try:
            c = int(raw_option2)
            if c < 1 or c > len(dest):
               print("Enter the number of the address: between 1 and %s" % len(dest))
            else:
               # remove from list
               dest.pop(c-1)
               break
         except ValueError:
            print ("the input is not a number between 1 and %s" % len(dest))
   elif raw_option == "M":
      while True:
         raw_option2 = raw_input("Enter the Address to move [1-%s]: " % len(dest))
         try:
            c = int(raw_option2)
            if c < 1 or c > len(dest):
               print("Enter the number of the address: between 1 and %s" % len(dest))
            else:
               # remove from list
               movaddress = dest.pop(c-1)
               if c-2 < 0:
                  dest.append(movaddress)
               else:
                  dest.insert(c-2,movaddress)
               break
         except ValueError:
            print ("the input is not a number between 1 and %s" % len(dest))
   elif raw_option == "O":
      while True:
         raw_option2 = raw_input("Enter Google Address: ")
         try:
            # add a google address check
            orig = str(raw_option2)
            break
         except ValueError:
            print ("This is not a valid address.  Please try again")
   elif raw_option == "W":
      with open(locatefile,'w') as f:
         pickle.dump((dest,orig),f)
   elif raw_option == "x":
      with open(locatefile,'w') as f:
         pickle.dump((dest,orig),f)
      break
   else:
      print("The choice was not valid, please try again")

