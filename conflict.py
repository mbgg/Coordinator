#!/usr/bin/python

from sets import Set

class Conflict:
	def __init__(self):
		self.pidhash = {}
		pass

	def add_to_list(self, list, item, time):
		if not(list):
			return False
		for i in range(0, len(list)):
			if list[i][0] == item:
				list[i][1] = list[i][1] + 1
				list[i][2].append(time)
				return True
		return False

	def add(self, pid, cpid, cpath, time):
		#print "conflict add %s %s %s" %(pid, cpid, cpath)
		conflictlist = self.pidhash.setdefault(pid, [])
		if not(conflictlist):
			pathlist = []# [cpath, 1],
			pathlist.append([cpath, 1, [time]])
			pidlist = []#[int(cpid), 1],
			pidlist.append([cpid, 1, [time]])

			conflictlist.append(pathlist)
			conflictlist.append(pidlist)
		else:
			pidlist = []
			pathlist = []
			pahtlist = conflictlist[0]
			pidlist = conflictlist[1]

			if not(self.add_to_list(pidlist, cpid, time)):
				pidlist.append([cpid, 1, [time]])
			if not(self.add_to_list(pathlist, cpath, time)):
				pathlist.append([cpath, 1, [time]])

	def get_pid_count(self, pid, cpid):
		conflictlist = self.pidhash.get(pid)
		if not(conflictlist):
			return 0
		for element in iter(conflictlist[1]):
			if cpid == element[0]:
				return element[1]
		return 0

	def get_time_list(self, pid, cpid):
		conflictlist = self.pidhash.get(pid)
		if not(conflictlist):
			return None
		for element in iter(conflictlist[1]):
			if cpid == element[0]:
				return element[2]
		return None

	def calc_time(slef, list):
		if not(list):
			return None
		min = list[0]
		max = list[0]
		avg = list[0]
		count = 1
		for i in range(1, len(list)):
			if list[i] < min:
				min = list[i]
			if list[i] > max:
				max = list[i]
			avg += list[i]
			count += 1
		avg = avg/count
		return [min, max, avg]

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
			conflictlist = self.pidhash.get(pids[i])
			for pl in iter(conflictlist[0]):
				cset.add(pl[0])
		return cset


	def get_pids(self, pid):
		cset = Set()
		pids = self.pidhash.keys()
		for i in range(0, len(pids)):
			conflictlist = self.pidhash.get(pid[i])
			for pl in iter(conflictlist[1]):
				cset.add(pl[0])
		return cset


