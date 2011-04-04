#!/usr/bin/python 

import sys
import csv
from hasht import HashTable

#conn = None #connection to hypervisor
filename = '/tmp/fuse-log-fifo'
global fd
global pidhash 

def log_checker_get_pid(something):
	
	return 0

def log_checker_preface():
	global filename, fd, pidhash

	print "open %s for reading" %(filename)
	#fd = csv.reader(open('/tmp/fuse-log-fifo', 'r'), delimiter=':', quotechar='|')
	fd = csv.reader(open(filename, 'r'), delimiter=':', quotechar='|')
	if fd == None:
		print "not able to open %s" %filename
		return 1

	pidhash = HashTable()
	

def log_checker_postface():
	print "entering postface"
	global conn
	fd.close()
	pass



if __name__ == "__main__":
	global fd
	global pidhash

	print "log-checker started"
	log_checker_preface()

	#for row in fd:
	for [ pid, time, op, path, offset, size ] in fd:
#		if pidhash.get(pid) != None:
#			continue
#		filehash = HashTable()
#		pidhash.set(pid, filehash)
		#print row
		print "%s %s %s %s %s %s" %(pid, time, op, path, offset, size)

	#log_checker_postface()

