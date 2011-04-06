#!/usr/bin/python 

class LogData:
	
	def __init__(self):#,pid,path,op,offset,size):
		self.pidhash = {}

	def add(self, pid, path, op, offset, size): # add data to the data structure...
		filehash = self.pidhash.setdefault(pid, {})
		rangelist = filehash.setdefault(path, [])
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
		

	

