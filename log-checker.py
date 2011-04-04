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

	for [ pid, time, op, path, offset, size ] in fd:
		if op != "write" and op != "read":
			print "op %s ignored" %op
			continue

		filehash = pidhash.get(pid)
		if filehash == None:
			# we have a new process
			rangelist = [[op, int(offset), int(offset)+int(size)]] 
			filehash = HashTable()
			filehash.set(path, rangelist)
			pidhash.set(pid, filehash)
			print "added pid %s [%d,%d]" %(pid, int(offset), int(offset)+int(size))

		else:
			# get filehash from pid
			filehash = pidhash.get(pid);
			# we have the file already?
			expath = filehash.get(path)
			if expath == None:
#				print "filepaht %s didn't exist %s %s" %(path, pid, op)
				rangelist = [[op, int(offset), int(offset)+int(size)]] 
				filehash = HashTable()
				filehash.set(path, rangelist)
				#print "op %s [%d,%d] added" %(op, int(offset), int(offset)+int(size))
			else:
#				print "filepaht %s exists %s %s" %(path, pid, op)
			#we have the range already?
				found = None
				for i in range(0, len(expath)):
					if int(offset) >= int(expath[i][1]) and int(offset)+int(size) <= int(expath[i][2]) and op == expath[i][0]:
						print "%s op %s [%d,%d] already in filehash" %(pid, op, int(offset), int(offset)+int(size))
						found = expath
						break

				if found == None:
					print "%s op %s [%d,%d] not in filehash" %(pid, op, int(offset), int(offset)+int(size))
					expath.append([op, int(offset), int(offset)+int(size)])

#		print "%s %s %s %s %s %s" %(pid, time, op, path, offset, size)

	#log_checker_postface()

