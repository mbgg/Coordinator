#!/usr/bin/python

from sets import Set

class Conflict:
	def __init__(self):
		self.pidhash = {}
		pass

	def add_to_list(self, list, item):
		if not(list):
			return False
		for i in range(0, len(list)):
			if list[i][0] == item:
				list[i][1] = list[i][1] + 1
				return True
		return False

	def add(self, pid, cpid, cpath):
		#print "conflict add %s %s %s" %(pid, cpid, cpath)
		conflictlist = self.pidhash.setdefault(pid, [])
		if not(conflictlist):
			pathlist = []# [cpath, 1],
			pathlist.append([cpath, 1])
			pidlist = []#[int(cpid), 1],
			pidlist.append([cpid, 1])
			conflictlist.append(pathlist)
			conflictlist.append(pidlist)
		else:
			pidlist = []
			pathlist = []
			pahtlist = conflictlist[0]
			pidlist = conflictlist[1]

			if not(self.add_to_list(pidlist, cpid)):
				pidlist.append([cpid, 1])
			if not(self.add_to_list(pathlist, cpath)):
				pathlist.append([cpath, 1])

	def get_pid_count(self, pid, cpid):
		conflictlist = self.pidhash.get(pid)
		if not(conflictlist):
			return 0
		for element in iter(conflictlist[1]):
			if cpid == element[0]:
				return element[1]
		return 0

	def get_path_count(self, pid, cpath):
		conflictlist = self.pidhash.get(pid)
		if not(conflictlist):
			return 0
		for element in iter(conflictlist[0]):
			if cpath == element[0]:
				return element[1]
		return 0

	def get_pathes(self, path):
		cset = Set()
		pids = self.pidhash.keys()
		for i in range(0, len(pids)):
			conflictlist = slef.pidhash.get(pid[i])
			for pl in iter(conflictlist[0]):
				cset.append(pl[0])
		return cset


	def get_pids(self, pid):
		cset = Set()
		pids = self.pidhash.keys()
		for i in range(0, len(pids)):
			conflictlist = seld.pidhash.get(pid[i])
			for pl in iter(conflictlist[1]):
				cset.append(pl[0])
		return cset


