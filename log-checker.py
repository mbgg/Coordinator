#!/usr/bin/python 
import sys
import csv
import getopt
from logdata import LogData
from conflict import Conflict

filename = '/home/matthias/fuse/fuse-test/text.txt'
global text_to_load
global text_to_load2

global fd, fd2
global logdata
global pid_ignore_list, pid_check_list
global conflicts

def log_checker_preface():
	global filename, fd, logdata, fd2

	if text_to_load != None:
		filename = text_to_load

	print "open %s for reading" %(filename)
	#fd = csv.reader(open('/tmp/fuse-log-fifo', 'r'), delimiter=':', quotechar='|')
	fd = csv.reader(open(filename, 'r'), delimiter=':', quotechar='|')
	if fd == None:
		print "not able to open %s" %filename
		return 1

	if text_to_load2 != None:
		filename = text_to_load2
		print "open %s for reading" %(filename)
		fd2 = csv.reader(open(filename, 'r'), delimiter=':', quotechar='|')
		if fd2 == None:
			print "not able to open %s" %filename
			return 1
	

def log_checker_postface():
	global logdata

	pidlist = logdata.get_pids_all()
	print "pidlist: %s" %pidlist
	#path = logdata.get_pathes(pidlist[0])
	#print "all ragnes from pid %s on file %s: %s" %(pidlist[0], path[0], logdata.get_ranges(pidlist[0], path[0]))
#	for i in iter(pidlist):
#		print "pid %s accessed: %s" %(i, logdata.get_pathes(i))
#	pass

	#print "all pathes are %s" %logdata.get_pathes_all()
	#pidpath = logdata.get_pid_path()
	#print "all [pid, path] tuples: %s" %pidpath


def log_build_access_map(fd, operation):
	global logdata
	print "log build access map with %s and %s" %(fd, operation)
	pid_string = None
	id_list = pid_check_list 
	for [ pid, time, op, path, offset, size ] in fd:
		if pid_string != None:
			if path in id_list and op == "close":
					pid_string = None
					continue

		if pid_string == None:
			if path in id_list and op == "open":
					if operation != 0:
						pid_string = operation
					else:
						pid_string = path
					continue

		if op != "write" and op != "read":
			continue

		offset = int(offset)
		size = int(size)
#		logdata.add(pid, path, op, offset, size)
		
		if pid_string == None:
			if operation == 0:
				#logdata.add(pid, path, op, offset, size)
				logdata.oldadd(pid, path, op, offset, size, time)
			elif operation != 0:
				logdata.oldadd(operation, path, op, offset, size, time)
		else:
			#logdata.add(pid_string, path, op, offset, size)
			logdata.oldadd(pid_string, path, op, offset, size, time)


#NYAP NYAP NYAP
def find_conflicts():
	global pid_ignore_list, conflicts
	conflicts = Conflict()
	ret = None
	pid_path_list = logdata.get_pid_path()
	if pid_check_list:
		for i in range(0, len(pid_path_list)-1):
			if pid_path_list[i][0] not in pid_check_list:
				#print "pid %s ignored" %pid_path_list[i][0]
				continue
			for j in range(i+1, len(pid_path_list)):
				if pid_path_list[j][0] not in pid_check_list:
					#print "pid %s ignored" %pid_path_list[j][0]
					continue
				range_i = logdata.get_ranges(pid_path_list[i][0], pid_path_list[i][1])  #pid_path_list looks like [[pid, path](,[pid, path])*]
				if pid_path_list[i][0] != pid_path_list[j][0] and pid_path_list[i][1] == pid_path_list[j][1]: #access same file
					range_j = logdata.get_ranges(pid_path_list[j][0], pid_path_list[j][1])
					ret = find_conflicts_range(range_i, range_j, pid_path_list[i][1], pid_path_list[i][0], pid_path_list[j][0])

	else:
		for i in range(0, len(pid_path_list)-1):
			if pid_path_list[i][0] in pid_ignore_list:
				print "pid %s ignored" %pid_path_list[i][0]
				continue
			for j in range(i+1, len(pid_path_list)):
				if pid_path_list[j][0] in pid_ignore_list:
					print "pid %s ignored" %pid_path_list[j][0]
					continue
				range_i = logdata.get_ranges(pid_path_list[i][0], pid_path_list[i][1])  #pid_path_list looks like [[pid, path](,[pid, path])*]
				if pid_path_list[i][0] != pid_path_list[j][0] and pid_path_list[i][1] == pid_path_list[j][1]: #access same file
					print "%s and %s access same file %s" %(pid_path_list[i][0], pid_path_list[j][0], pid_path_list[j][1])
					range_j = logdata.get_ranges(pid_path_list[j][0], pid_path_list[j][1])
					ret = find_conflicts_range(range_i, range_j, pid_path_list[i][1], pid_path_list[i][0], pid_path_list[j][0])

	if ret != None:
		print "we found at least one conflict"
		pass
	return ret


def get_time(t1, t2):
	if t1 < t2:
		return t2 - t1
	else:
		return t1 - t2

# nyap
def find_conflicts_range(range_i, range_j, filename, pid, cpid):	
	ret = False
	for ri in iter(range_i):
		for rj in iter(range_j):
			rimin = ri[1]
			rimax = rimin + ri[2] - 1
			ritime = float(ri[3])
			rjmin = rj[1]
			rjmax = rjmin + rj[2] - 1
			rjtime = float(rj[3])
			if rimin > rjmax or rimax < rjmin: #case A
				continue
			else: # rimin >= rjmin and rimax >= rjmax: #case B
				if ri[0] == "write" or rj[0] == "write": # r-w or w-r accesses only NYAP!
					deltatime = get_time(ritime, rjtime)
					#print "conflict on file %s in i[%d,%d] and j[%d,%d] - %s %s - time %f %f - %f" %(filename, rimin, rimax, rjmin, rjmax, ri[0], rj[0], ritime, rjtime, deltatime)
					conflicts.add(pid, cpid, filename, deltatime) # pid, cpid, cpath
					ret = True

	return ret
	pass

def usage():
	print "-h       --help \t print this help"
	print "-t [path] --text=[path] \t load data from text file"
	print "-l [path] --load=[path] \t load data structure from file path"
	print "-s [path] --save=[path] \t save data structure to file path"
	print "-i [pid] --ignore=[pid] \t pid that will be ignored"
	print "-c [pid] --check=[pid] \t pid that will be checked"

if __name__ == "__main__":
	global conflicts
	global fd, fd2
	file_to_load = None
	save_to_file = None

	global pid_ignore_list, pid_check_list
	pid_ignore_list = []
	pid_check_list = []

	global text_to_load
	global text_to_load2
	text_to_load = None
	text_to_load2 = None

	try:
		opts, args = getopt.getopt(sys.argv[1:], "l:s:ht:i:c:", ["load=", "save=", "help", "text=", "ignore=", "check="])
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
			if text_to_load != None:
				text_to_load2 = a
			else:
				text_to_load = a
		elif o in ("-i", "--ignore"):
			pid_ignore_list.append(a)
		elif o in ("-c", "--check"):
			pid_check_list.append(a)
		else:
			assert False, "unhandled option"

	if pid_ignore_list:
		print "pid ignore list is: %s" %pid_ignore_list
	if pid_check_list:
		print "pid check list is: %s" %pid_check_list

	logdata = LogData()

	print "log-checker started"
	print "we load %s and %s" %(text_to_load, text_to_load2)

	if file_to_load != None:
		print "access map load from %s" %file_to_load
		if logdata.load_data(file_to_load) == False:
			print "not able to load file %s" %(file_to_load)
			sys.exit(1)
	else:
		log_checker_preface()
		if not(text_to_load2):
			log_build_access_map(fd, 0)
		else:
			log_build_access_map(fd, "run1")
			log_build_access_map(fd2, "run2")

	if save_to_file != None:
		print "save raw data to %s" %save_to_file
		logdata.save_data(save_to_file)

#	log_minimize_map()

	log_checker_postface()

	find_conflicts()
	
	# analyze conflicts

	pids = logdata.get_pids_all()	
	totalconflicts = 0
	for p1 in range(0, len(pids)-1):
		for p2 in range(1, len(pids)):
			timelist = conflicts.get_time_list(pids[p1], pids[p2])
			numc = conflicts.get_pid_count(pids[p1], pids[p2])
			if numc:
				print "number of conflicts between %s and %s: %d" %(pids[p1], pids[p2], numc)
				totalconflicts = totalconflicts + numc
				if timelist:
					t = conflicts.calc_time(timelist)
					print "time of conflicts between %s and %s: \t min %f \t max %f \t avg %f" %(pids[p1], pids[p2], t[0], t[1], t[2])

	print "total number of logged filesystem operations %d - number of overall conflicts %d" %(logdata.get_number_logged_fs_ops(), totalconflicts)

	#pathes = []
	#for pid in iter(pid_check_list):
	#	pathes.append(logdata.get_pathes(pid))

	#for p in iter(pathes):
	#	pass
	#	for pp in iter(p):
	#		print	"path %s has conflcits with %s" %(pp, conflicts.get_pathes(pp))
	
	#log_checker_postface()
