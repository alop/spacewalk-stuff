#!/usr/bin/python

import sys
import xmlrpclib

SATELLITE_URL = "http://spacewalk.usa.tribune.com/rpc/api"
SATELLITE_LOGIN = "abelopez"
SATELLITE_PASSWORD = 

client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)

# group ID's are not listed in spacewalk page, extracting them here for anoither script

chans = client.channel.listAllChannels(key)
for chan in chans:
	print 'chan id is %s name is %s' % ( chan.get('id'), chan.get('name') )

