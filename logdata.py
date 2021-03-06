#!/usr/bin/python 

import pickle
import os.path

class LogData:
	
	def __init__(self):
		self.pidhash = {}
		self.number_of_logged_fs_ops = 0

	def op_logged(self):
		self.number_of_logged_fs_ops += 1

	def get_number_logged_fs_ops(self):
		return self.number_of_logged_fs_ops

	def append(self, op, offset, size, rangelist):
		if rangelist != []:
			for range in iter(rangelist):
				old_op = range[0]
				old_offset = range[1]
				old_size = range[2] + old_offset
				new_size = offset + size
				new_offset = offset
				if old_op != op:
					continue
				if new_offset < old_offset and (new_size <= old_size and new_size > old_offset):
					#print "append new %s[%d:%d]" %(op, offset, size)
					range[1] = new_offset
					return True
				if (new_offset >= old_offset and new_offset <= old_size) and new_size > old_size:
					#print "append new %s[%d:%d]" %(op, offset, size)
					range[2] = new_size - new_offset + old_size - old_offset
					return True
				if new_offset <= old_offset and new_size >= old_size:
					#print "append new %s[%d:%d]" %(op, offset, size)
					range[1] = new_offset
					range[2] = new_size - new_offset + old_size - old_offset
					return True
				#print "new[%d:%d] - old[%d:%d]" %(new_offset, new_size, old_offset, old_size)
			#print "rangelist has no fitting part"
			return False
		else:
			#print "rangelist is empty"
			return False

	def oldadd(self, pid, path, op, offset, size, time): # add data to the data structure...
		self.op_logged()
		filehash = self.pidhash.setdefault(pid, {})
		rangelist = filehash.setdefault(path, [])
		rangelist.append([op, offset, size, time])

	def add(self, pid, path, op, offset, size): # add data to the data structure...
		self.op_logged()
		filehash = self.pidhash.setdefault(pid, {})
		rangelist = filehash.setdefault(path, [])
		if self.append(op, offset, size, rangelist) == False:
			#print "add new %s[%d:%d]" %(op, offset, size+offset)
			rangelist.append([op, offset, size])

	def get_ranges(self, pid, path): # returns list of all file ranges from pid path tupel
		filehash = self.pidhash.get(pid)
		return filehash.get(path)
		pass

	def get_pids_all(self): # returns all pids
	  return self.pidhash.keys()

	def get_pathes(self, pid): # returns a list with all passes from given pid
		fh = self.pidhash.get(pid)
		return fh.keys()
		pass

	def get_pathes_all(self): # returns a list with all pathes
		pathlist = []
		for p in self.pidhash.itervalues():
			for path in p.iterkeys():
				if pathlist.count(path) == 0:
					pathlist.append(path)
		return pathlist

	def get_pid_path(self): # returns a list with all ['pid', 'path'] values
		pidpathlist = []
		for p in self.pidhash.iterkeys():
			f = self.pidhash.get(p)
			for path in f.keys():
				pidpathlist.append([p, path])
		return pidpathlist

	def get_pids(self, path): # returns a list of all pids by given path
		pidlist = []
		pids = self_pids_all()
		for p in iter(pids):
			filehash = self.pidhash.get(p)
			if filehash.get(path) != None:
				pidlist.append(pid)
		return pidlist
		
	def save_data(self, path):
		fd = open(path, 'w')
		fd.seek(0)
		pickle.dump(self.pidhash, fd)
		fd.close()

	def load_data(self, path):
		if os.path.isfile(path):
			self.pidhash = {}
			fd = open(path, 'r')
			self.pidhash = pickle.load(fd)
			fd.close()
			return True
		else:
			return False
		
	

if __name__ == "__main__":
	print "executing data structure usecase..."
	logdata = LogData()
	#logdata.add(pid, path, op, offset, size)
	logdata.add(1, 'test', 'read', 10, 2)
	logdata.add(1, 'test', 'read', 8, 2)
	logdata.add(1, 'test', 'read', 11, 100)
	logdata.add(1, 'test', 'read', 15, 10)

	logdata.add(1, 'test', 'write', 10, 200)
	logdata.add(1, 'test', 'write', 11, 2)

	print logdata.get_ranges(1, 'test')
