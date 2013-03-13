#!/usr/bin/python
import xmlrpclib

SATELLITE_URL = "http://spacewalk.usa.tribune.com/rpc/api"
SATELLITE_LOGIN = "abelopez"
SATELLITE_PASSWORD = "Tru$tn01"

client = xmlrpclib.Server(SATELLITE_URL, verbose=0)

key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)
list = client.user.list_users(key)
for user in list:
	   print user.get('login')

client.auth.logout(key)
