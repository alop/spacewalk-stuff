#!/usr/bin/python
import sys
import xmlrpclib

SATELLITE_URL = "http://spacewalk.usa.tribune.com/rpc/api"
SATELLITE_LOGIN = "abelopez"
SATELLITE_PASSWORD = "Tru$tn01"

client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)
hostIP = sys.argv[1]
tier = int(sys.argv[2])

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
	#print sysID
	chanID, chanLabel, OS = getSystemDetails(sysID)
	gid = calcSystemGroup(tier, chanID)
	groupName = getGroupName(gid)
	print 'system %s will go in group %s' % (hostIP, groupName)
	client.systemgroup.addOrRemoveSystems(key,groupName,sysID,True)
	client.auth.logout(key)

def searchForSystem(IP):
	print 'Looking for %s in spacewalk' % ( IP )
	id = 0
	sysSearch = client.system.search.hostname(key, str(IP) )
	#print len(sysSearch)
	for system in sysSearch:
		if system.get('hostname') == IP:
			#print 'test'
			id = system.get('id')
			#print system.get('name')
	return id

def getSystemDetails(id):
	#sysID = client.system.getId(key, host)
	subscription = client.system.getSubscribedBaseChannel(key, id)
	details = client.system.getDetails(key, id )
	chanID = subscription.get('id')
	chanLabel = subscription.get('label')
	OS = details.get('release')
	#print chanID, chanLabel, OS
	return chanID, chanLabel, OS

#### Group ID cheat section
#group id is 29 name is Solaris 10 Tier 1 & 2
#group id is 30 name is CentOS 4 Dev/Test/QA/Tier 3
#group id is 14 name is Solaris 9 Tier 1 & 2
#group id is 28 name is CentOS 5 Dev/Test/QA/Tier 3
#group id is 31 name is CentOS 4 Tier 1 & 2
#group id is 16 name is Solaris 10 Dev/Test/QA/Tier 3
#group id is 13 name is Solaris 9 Dev/Test/QA/Tier 3
#group id is 27 name is CentOS 5 Tier 1 & 2
#
### Channel ID cheat section
#chan id is 103 name is CentOS 5 i386
#chan id is 106 name is Solaris 9 Sparc
#chan id is 104 name is Solaris 10 Intel
#chan id is 121 name is Solaris 10 Sparc
#chan id is 101 name is CentOS 4 x86_64
#chan id is 102 name is CentOS 5 x86_64
#chan id is 112 name is CentOS 4 i386
def calcSystemGroup(tier, chan):
	#print "tier is %s " % (str(tier))
	if chan == 101:
		if tier == 1:
			group = 31
		elif tier == 2:
			group = 31
		else:
			group = 30
	elif chan == 102:
		if tier == 1:
			group = 27
		elif tier == 2:
			group = 27
		else:
			group = 28
	elif chan == 103:
		if tier == 1:
			group = 27
		elif tier == 2:
			group = 27
		else:
			group = 28
	elif chan == 104:
		if tier == 1:
			group = 29
		elif tier == 2:
			group = 29
		else:
			group = 16
	elif chan == 106:
		if tier == 1:
			group = 14
		elif tier == 2:
			group = 14
		else:
			group = 13
	elif chan == 112:
		if tier == 1:
			group = 31
		elif tier == 2:
			group = 31
		else:
			group = 30
	elif chan == 121:
		if tier == 1:
			group = 29
		elif tier == 2:
			group = 29
		else:
			group = 16
	return group

def getGroupName(id):
	details = client.systemgroup.getDetails(key, id)
	name = details.get('name')
	return name
				
if __name__ == '__main__':
	main()
