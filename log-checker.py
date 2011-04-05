#!/usr/bin/python 
#	The data structure:
#
#	hashmap pidhash(pid,filehash) -> all files used by pid
# hashmap filehash(path,range) -> all byte ranges used for this file by pid
# set     range([operation, offset, offset+size]+) -> ranges used by pid for specific file including operation
#

import sys
import csv
from hasht import HashTable
from helper import LogData

#conn = None #connection to hypervisor
filename = '/tmp/fuse-log-fifo'
global fd
global pidhash 
global logdata

def log_checker_get_pid(something):
	
	return 0

def log_checker_preface():
	global filename, fd, pidhash, logdata

	print "open %s for reading" %(filename)
	#fd = csv.reader(open('/tmp/fuse-log-fifo', 'r'), delimiter=':', quotechar='|')
	fd = csv.reader(open(filename, 'r'), delimiter=':', quotechar='|')
	if fd == None:
		print "not able to open %s" %filename
		return 1

	pidhash = HashTable()
	logdata = LogData()
	

def log_checker_postface():
	print "entering postface"
	global logdata
	pidlist = logdata.get_pids_all()

	path = logdata.get_pathes(pidlist[0])
	print logdata.get_ranges(pidlist[0], path[0])
	print pidlist
	for i in range(0, len(pidlist)):
		print "pid %s accessed: %s" %(pidlist[i], logdata.get_pathes(pidlist[i]))
	pass

def log_build_access_map(fd):
	global logdata
	for [ pid, time, op, path, offset, size ] in fd:
		if op != "write" and op != "read":
			continue
		offset = int(offset)
		size = int(size)
		logdata.add(pid, path, op, offset, size)

def log_minimize_map():
	global pidhash

	found = pidhash
	#pidlist = []
	#pidlist = pidhash.get_keys()

	for pid in pidhash.get_keys(): #pidlist:
		rangelist = []
		filehash = pidhash.get(pid)
		#filelist = []
		#filelist = filehash.get_keys()

		for f in filehash.get_keys(): #filelist:
			rangelist = filehash.get(f)

			while found != None:
				found = None
				for r in rangelist:
					if offset >= r[1] and offset+size <= r[2] and op == r[0]:
						print "%s op %s [%d,%d] already in filehash" %(pid, op, offset, offset+size)
						found = r
						break
					# C + E
					elif offset-1 >= r[1] and (offset-1 <= r[2])  and op == r[0]:
						r[2] = offset+size
						found = r
						break 
					# D + F


def find_conflicts():
	pass

if __name__ == "__main__":
	global fd
	global pidhash

	print "log-checker started"
	log_checker_preface()

	log_build_access_map(fd)

#	log_minimize_map()

	log_checker_postface()

