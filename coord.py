#!/usr/bin/python 
# coordinator which sends 
#
#

import socket
import libvirt
import sys

conn = None #connection to hypervisor

def examine_vm_by_id(id):
	global conn
	try:
		dom = conn.lookupByID(id)
	except:
		print 'Failed to find the main domain by ID'
		sys.exit(1)

	print "Domain %s: id %d running %s" % (dom.name(), dom.ID(), dom.OSType())
	print dom.info()
#	print conn.getCapabilities()
#	nodeinfo = conn.virGetNodeInfo()
#	print nodeinfo.model
#	print nodeinfo.memory



def examine_vm(name):
	global conn
	try:
		dom = conn.lookupByName(name)
	except:
		print 'Failed to find the main domain by name'
		sys.exit(1)

	print "Domain %s: id %d running %s - %s" % (dom.name(), dom.ID(), dom.OSType(), dom.info())



def shutdown_all():
	global conn
	for vmid in conn.listDomainsID():
		dom = conn.lookupByID(vmid)
		print "shutting down %s..." %(dom.name())
		dom.destroy()
		print "... done!"
	pass



def preface():
	global conn
	#conn = libvirt.openReadOnly("qemu:///system")
	conn = libvirt.open("qemu:///system")
	if conn == None:
		print 'Failed to open connection to the hypervisor'
		sys.exit(1)

	print conn.listDefinedDomains()
	print "numOfDomains: %d" %(conn.numOfDomains())
	print "numOfDefinedDomains: %d" %(conn.numOfDefinedDomains())

	shutdown_all()

	for id in conn.listDefinedDomains():	
		dom = conn.lookupByName(id)
		examine_vm(id)


	dom = conn.lookupByName("demo3")
	dom.create()
	print "domain %s with ID %d created" %(dom.name(), dom.ID())
#	conn.createXML(dom.XMLDesc(1), 0)

	print conn.listDefinedDomains()
	print "numOfDomains: %d" %(conn.numOfDomains())
	print "numOfDefinedDomains: %d" %(conn.numOfDefinedDomains())
	for id in conn.listDomainsID():	
		dom = conn.lookupByID(id) 
		examine_vm(dom.name())



def postface():
	print "entering postface"
	global conn
	conn.close()
	pass



def nwcom():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.bind(("", 51000)) 
	s.listen(1)

	try: 
		while True: 
			komm, addr = s.accept() 
			print "connection from %s" % addr[0]

			while True: 
				data = komm.recv(1024)

				if not data: 
					komm.close() 
					break

				#print "[%s] %s" % (addr[0], data) 	
				if data == "start":
					print "start recv"
					komm.send("check") 

				elif data == "rewind":
					print "rewind recv"
					komm.send("dorewind") 
				
				elif data == "exit":
					komm.close()
					s.close()
					return

	finally: 
		s.close()
		postface()

if __name__ == "__main__":
	print "coord started"
	preface()

	#nwcom()

	postface()

