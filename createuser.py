from urllib import urlencode
from httplib2 import Http
import json
import sys
import base64

engine = create_engine('sqlite:///beautyitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

print("Running Endpoint Tester....\n")
address = raw_input("Please enter the address of the server you want to access, \n If left blank the connection will be set to 'http://localhost:8000':   ")
if address == '':
	address = 'http://localhost:8000'


 #TEST 1 TRY TO MAKE A NEW USER
try:
	
	url = address + '/users'
 	h = Http()
	#h.add_credentials('TinnyTim', 'Udacity')
 	data = dict(username = "TinnyTim", password = "Udacity")
 	data = json.dumps(data)
 	resp, content = h.request(url,'POST', body = data, headers = {"Content-Type": "application/json"})
	if resp['status'] != '201' and resp['status'] != '200':
 		raise Exception('Received an unsuccessful status code of %s' % resp['status'])
except Exception as err:
	print "Test 1 FAILED: Could not make a new user"
	print err.args
	sys.exit()
else:
	print "Test 1 PASS: Succesfully made a new user"

#TEST 2 ADD NEW BAGELS TO THE DATABASE
try:
	h = Http() 
	h.add_credentials('TinnyTim','Udacity')
	url = address + '/product'
	data = dict(username = "TinnyTim", password = "Udacity", name = "plain", picture = "http://bonacbagel.weebly.com/uploads/4/0/5/4/40548977/s318635836612132814_p1_i1_w240.jpeg", description = "Old-Fashioned Plain Bagel", price= "$1.99")
	resp, content = h.request(url,'POST', body = json.dumps(data), headers = {"Content-Type" : "application/json"})
	if resp['status'] != '200':
		raise Exception('Received an unsuccessful status code of %s' % resp['status'])
except Exception as err:
	print "Test 2 FAILED: Could not add new bagels"
	print err.args
	sys.exit()
else:
	print "Test 2 PASS: Succesfully made new bagels"