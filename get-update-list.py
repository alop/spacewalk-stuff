#!/usr/bin/python
import re
import sys
import xmlrpclib

SATELLITE_URL = "http://spacewalk.usa.tribune.com/rpc/api"
SATELLITE_LOGIN = "abelopez"
SATELLITE_PASSWORD = 

client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)
hostIP = sys.argv[1]
#tier = int(sys.argv[2])

# system ID's will be sorted out before hand
# I'm not _that_ smart of a programmer -yet
# lets make a list for each system group, populated with system id's
# will probably need to know channels too

# Function Definitions 
def main():
	sysID = searchForSystem( hostIP )
	if sysID == 0:
		client.auth.logout(key)
		print '%s is not in spacewalk' % ( hostIP )
		sys.exit(2)
	getPackageList(sysID)
	client.auth.logout(key)

def searchForSystem(IP):
	print 'Looking for %s in spacewalk' % ( IP )
	id = 0
	sysSearch = client.system.search.hostname(key, str(IP) )
	#print len(sysSearch)
	for system in sysSearch:
		if IP in system.get('hostname'):
			print "Found %s" % system.get('hostname')
			id = system.get('id')
			#print 'test'
	return id

def getPackageList(id):
	packlist = client.system.listLatestUpgradablePackages(key,id)
	print 'Package Old New'
	for package in packlist:
		pname = package.get('name')
		parch = package.get('arch')
		pfver = package.get('from_version')
		pfrel = package.get('from_release')
		ptver = package.get('to_version')
		ptrel = package.get('to_release')
		print '%s %s-%s.%s %s-%s.%s' % (pname, pfver, pfrel, parch, ptver, ptrel, parch)
	

if __name__ == '__main__':
	main()
