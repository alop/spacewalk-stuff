#!/usr/bin/python

import sys
import xmlrpclib

SATELLITE_URL = "http://spacewalk.usa.tribune.com/rpc/api"
SATELLITE_LOGIN = "abelopez"
SATELLITE_PASSWORD = "Tru$tn01"

client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)

# group ID's are not listed in spacewalk page, extracting them here for anoither script

groups = client.systemgroup.listAllGroups(key)
for group in groups:
	print 'group id is %s name is %s' % ( group.get('id'), group.get('name') )

