#!/usr/bin/python

import json
import subprocess

turnkey_box = False

def is_number(s):
	try:
		float(s)
		return True
	except:
		return False

try:
	rc = subprocess.check_output(["turnkey-version"])
	turnkey_box = True
except:
	#could uncomment this line for testing if needed.
	#rc = "turnkey-jenkins-13.0-wheezy-amd64"
	turnkey_box = False

if turnkey_box:
	facts = rc.split("-")

	#Get the version number. should be the only number in the facts list
	ver_list = filter(is_number, facts)
	if len(ver_list) == 1:
		ver_index = facts.index(ver_list[0])
	fact_version = ""
	#could be longer than the one number i.e. 14.0 RC2
	for i in facts[ver_index:len(facts)-2]:
		fact_version += i

	#application name should be from index 1 to version number index
	fact_app = ""
	for j in facts[1:ver_index]:
		fact_app += j+' '

	fact_arch = facts[-1]
	fact_deb = facts[-2]

	print(json.dumps({
		"ansible_facts" : {
			"turnkey" : True, 
			"turnkey_version" : rc,
			"turnkey_app" : fact_app,
			"turnkey_ver" : fact_version,
			"turnkey_arch" : fact_arch,
			"turnkey_deb" : fact_deb
		}
	}))
else:
	print(json.dumps({
		"ansible_facts" : {
			"turnkey" : False
		}
	}))

