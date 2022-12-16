from cmath import atan
from distutils.log import error
from gettext import find
from http.client import OK
from importlib.resources import path
from logging.config import valid_ident
from platform import node
from queue import PriorityQueue
from re import X
from sre_constants import FAILURE
from this import s
from expand import expand

class Node:
	def __init__(self, name, g, h, order):
		self._name = name
		self._gval = g
		self._hval = h
		self._order = order

class PriorityQ:
	def __init__(self):
		self._data = []
	
	def insert(self, node: Node):
		self._data.append(node)
	
	def pop(self):
		minf = self._data[0] #initialize minf to first item in data
		for item in self._data:
			#calculate f
			f = item._hval + item._gval
			minff = minf._hval + minf._gval

			if f < minff:
				minf = item
			elif f == minff:
				if item._hval < minf._hval:
					minf = item
				elif item._order < minf._order:
					minf = item

		self._data.remove(minf) #remove min from data
		return minf

	def findg(self, name):
		for item in self._data:
			if item._name == name:
				return item._gval
		return None
	
	def updateg(self, name, g):
		for item in self._data:
			if item._name == name:
				item._gval = g


def a_star_search (dis_map, time_map, start, end):
	open = PriorityQ()
	order = 0
	startnode = Node(start, 0, dis_map[start][end], order)
	open.insert(startnode)
	parents = {start: None}
	closed = []

	while len(open._data) != 0:
		currnode = open.pop() 
		curr = currnode._name
		closed.append(curr)

		if curr == end:
			path = [end]
			i = end
			while(parents[i] != None):
				path.append(parents[i])
				i = parents[i] #retraces path from end to start
			return path[::-1]
		
		list = expand(curr, time_map) #obtain list of adjacent nodes
		for node in list:
			if node not in closed:
				g = currnode._gval + time_map[curr][node]
				h = dis_map[node][end]
				if (open.findg(node) == None): #if node is not in open, insert node and add parent
					order += 1
					realnode = Node(node, g, h, order)
					open.insert(realnode)
					parents[node] = curr
				elif g < open.findg(node): #if new g value is smaller than old g value, update g and parent
					open.updateg(node, g)
					parents[node] = curr
	print("No solution found")
	return

def depth_first_search(time_map, start, end):
	fringe = [start]
	path = [end]
	parents = {start: None}

	while fringe:
		curr = fringe.pop()
		if curr == end:
			i = end
			while(parents[i] != None):
				path.append(parents[i])
				i = parents[i] #retraces path from end to start
			return path[::-1]
		else:
			expandlist = expand(curr, time_map)
			for item in expandlist:
				parents[item] = curr
			fringe = fringe + expandlist[::-1]
	print("No solution found")
	return

def breadth_first_search(time_map, start, end):
	fringe = [start]
	parents = {start: None} #dictionary: key is node, value is its parent
	path = [end]
	seen = []

	while fringe: #while fringe is not empty
		curr = fringe.pop(0) #set curr to top of fringe
		if curr == end:
			i = end
			while(parents[i] != None):
				path.append(parents[i])
				i = parents[i] #retraces path from end to start
			return path[::-1] #reverses path ... .reverse() lets you print reversed but returns NONE!
		else:
			uncutexpand = expand(curr, time_map) #this is all the nodes connected to curr
			cutexpand = [] #this is all NEW nodes connected to curr
			for item in uncutexpand:
				if (item not in seen) and (item not in fringe):
					cutexpand.append(item)
					parents[item] = curr #add any new parent-child relations to dictionary
			fringe = fringe + cutexpand #add all the NEW nodes connected to curr to fringe
			seen.append(curr) #mark curr as seen
	print("No solution found")
	return #if this gets called, that means fringe was empty before solution was found