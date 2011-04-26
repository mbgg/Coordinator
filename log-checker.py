#!/usr/bin/python 
#	The data structure:
#
#

import sys
import csv
import getopt
from logdata import LogData

#filename = './fuse-madbench-test'
#filename = '/home/matthias/fuse-log-fifo'
filename = '/home/matthias/fuse/fuse-test/text.txt'
saved_status = './status.saved'
global text_to_load

global fd
global logdata

def log_checker_get_pid(something):
	
	return 0

def log_checker_preface():
	global filename, fd, logdata

	if text_to_load != None:
		filename = text_to_load

	print "open %s for reading" %(filename)
	#fd = csv.reader(open('/tmp/fuse-log-fifo', 'r'), delimiter=':', quotechar='|')
	fd = csv.reader(open(filename, 'r'), delimiter=':', quotechar='|')
	if fd == None:
		print "not able to open %s" %filename
		return 1

	

def log_checker_postface():
	global logdata

	pidlist = logdata.get_pids_all()
	print "pidlist: %s" %pidlist
	#path = logdata.get_pathes(pidlist[0])
	#print "all ragnes from pid %s on file %s: %s" %(pidlist[0], path[0], logdata.get_ranges(pidlist[0], path[0]))
	for i in iter(pidlist):
		print "pid %s accessed: %s" %(i, logdata.get_pathes(i))
	pass

	#print "all pathes are %s" %logdata.get_pathes_all()
	#pidpath = logdata.get_pid_path()
	#print "all [pid, path] tuples: %s" %pidpath


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

#NYAP NYAP NYAP
def find_conflicts():
	ret = None
	pid_path_list = logdata.get_pid_path()
	for i in range(0, len(pid_path_list)-1):
		for j in range(i+1, len(pid_path_list)):
			range_i = logdata.get_ranges(pid_path_list[i][0], pid_path_list[i][1])  #pid_path_list looks like [[pid, path](,[pid, path])*]
			if pid_path_list[i][0] != pid_path_list[j][0] and pid_path_list[i][1] == pid_path_list[j][1]:
				print "pid %s and %s access same file %s" %(pid_path_list[i][0], pid_path_list[j][0], pid_path_list[i][1])
				range_j = logdata.get_ranges(pid_path_list[j][0], pid_path_list[j][1])
				ret = find_conflicts_range(range_i, range_j, pid_path_list[i][1])
	if ret != None:
		print "we found at least one conflict in"
	return ret

# nyap
def find_conflicts_range(range_i, range_j, filename):	
	ret = False
	for ri in iter(range_i):
		for rj in iter(range_j):
			rimin = ri[1]
			rimax = rimin + ri[2]
			rjmin = rj[1]
			rjmax = rjmin + rj[2]
			if rimin > rjmax or rimax < rjmin: #case A
				continue
			else: #f rimin >= rjmin and rimax >= rjmax: #case B
				print "conflict on file %s in i[%d,%d] and j[%d,%d]" %(filename, rimin, rimax, rjmin, rjmax)
				ret = True

	return ret
	pass

def usage():
	print "-h       --help \t print this help"
	print "-t[path] --text=[path] \t load data from text file"
	print "-l[path] --load=[path] \t load raw data from file path"
	print "-s[path] --save=[path] \t save raw data to file path"

if __name__ == "__main__":
	global fd		
	file_to_load = None
	save_to_file = None

	global text_to_load
	text_to_load = None

	try:
		opts, args = getopt.getopt(sys.argv[1:], "l:s:ht:", ["load=", "save=", "help", "text="])
	except getopt.GetoptError, err:
			print str(err) # will print something like "option -a not recognized"
			usage()
			sys.exit(2)
	for o, a in opts:
		if o in ("-l", "--load"):
			file_to_load = a
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-s", "--save"):
			save_to_file = a
		elif o in ("-t", "--text"):
			text_to_load = a
		else:
			assert False, "unhandled option"

	logdata = LogData()

	print "log-checker started"

	if file_to_load != None:
		print "access map load from %s" %file_to_load
		if logdata.load_data(file_to_load) == False:
			print "not able to load file %s" %(file_to_load)
			sys.exit(1)
	else:
		log_checker_preface()
		log_build_access_map(fd)

		if save_to_file != None: #save == True:
			print "save raw data to %s" %save_to_file
			logdata.save_data(save_to_file)#"./status.saved")

#	log_minimize_map()

	log_checker_postface()

	find_conflicts()
