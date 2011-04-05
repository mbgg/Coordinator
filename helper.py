#!/usr/bin/python 

class LogData:
	
	def __init__(self):#,pid,path,op,offset,size):
		self.pidhash = {}
#		filehash = {}
#		rangelist = []
#		rangelist.append([op, offset, size])
#		filehash[path] = rangelist
#		self.pidhash[pid] = filehash

	def add(self, pid, path, op, offset, size):
		filehash = self.pidhash.setdefault(pid, {})
		rangelist = filehash.setdefault(path, [])
		rangelist.append([op, offset, size])
		#print "%s added %s to %s [%d,%d]" %(pid, rangelist[len(rangelist)-1][0], filehash.keys(), offset, offset+size)

	def get_ranges(self, pid, path):
		filehash = self.pidhash.get(pid)
		return filehash.get(path)
		pass

	def get_pids_all(self):
	  return self.pidhash.keys()

	def get_pathes(self, pid):
		fh = self.pidhash.get(pid)
		return fh.keys()
		pass

	def get_pid_path(self):
		pass

	def get_pids(self, path):
		pass

	

