#!/usr/bin/python 
#	The data structure:
#
#

import sys
import csv
from helper import LogData

#conn = None #connection to hypervisor
filename = './fuse-log-fifo'
global fd
global logdata

def log_checker_get_pid(something):
	
	return 0

def log_checker_preface():
	global filename, fd, logdata

	print "open %s for reading" %(filename)
	#fd = csv.reader(open('/tmp/fuse-log-fifo', 'r'), delimiter=':', quotechar='|')
	fd = csv.reader(open(filename, 'r'), delimiter=':', quotechar='|')
	if fd == None:
		print "not able to open %s" %filename
		return 1

	logdata = LogData()
	

def log_checker_postface():
	print "entering postface"
	global logdata

	pidlist = logdata.get_pids_all()
	print "pidlist: %s" %pidlist
	path = logdata.get_pathes(pidlist[0])
	print "all ragnes from pid %s on file %s: %s" %(pidlist[0], path[0], logdata.get_ranges(pidlist[0], path[0]))
	for i in iter(pidlist):
		print "pid %s accessed: %s" %(i, logdata.get_pathes(i))
	pass

	print "all pathes are %s" %logdata.get_pathes_all()
	pidpath = logdata.get_pid_path()
	print "all [pid, path] tuples: %s" %pidpath

def log_build_access_map(fd):
	global logdata
	for [ pid, time, op, path, offset, size ] in fd:
		if op != "write" and op != "read":
			continue
		offset = int(offset)
		size = int(size)
		logdata.add(pid, path, op, offset, size)

def log_minimize_map():
	pass

def find_conflicts():
	pass

if __name__ == "__main__":
	global fd

	print "log-checker started"
	log_checker_preface()

	log_build_access_map(fd)

#	log_minimize_map()

	log_checker_postface()

