# Heejung Chung
# Implementation of a HashMap class without use of dictionaries
# TO RUN:
# 	1. open terminal
# 	2. type... $ python3 hashmap.py

import sys
import re
import pdb
from collections import namedtuple


######################### CONSTANTS #########################

SET_CMD = "set"
GET_CMD = "get"
DELETE_CMD = "delete"
LOAD_CMD = "load"
EXIT_CMD = "exit"


######################### HASHMAP CLASS IMPLEMENTATION ######

class HashMap(object):
	# hashmap singleton
	current = None

	# constructor
	def __new__(cls, size):
		if size <= 0:
			print("cannot create hashmap of size less than 1")
			return
		return object.__new__(cls)

	def __init__(self, size):
		self._size = size
		# create null arrays for keys and values with size `size`
		# arrays are 2d to help with chaining
		self._keys = [[None] for i in range(size)]
		self._values = [[None] for i in range(size)]
		self._valuesCount = 0
		HashMap.current = self

	# private helper function
	def _getIndexFromKey(self, key):
		keyHash = hash(key)
		TwoDIndex = namedtuple('TwoDIndex', 'idx chainIdx keyExists')
		idx = keyHash % self._size
		# if no collision...
		if self._keys[idx][0] == None:
			return TwoDIndex(idx, 0, False)
		else: # if there is a collision...
			try: # if existing key
				chainIdx = self._keys[idx].index(key)
				return TwoDIndex(idx, chainIdx, True)
			except: # if non-existent key
				return TwoDIndex(idx, -1, False)

	# functions required by coding challenge
	def set(self, key, value):
		if self._valuesCount >= self._size:
			return False
		else:
			idxs = self._getIndexFromKey(key)

			if idxs.chainIdx == -1: # if there is a collision & new key
				self._keys[idxs.idx].append(key)
				self._values[idxs.idx].append(value)
			else: # if existing key and/or no collisions
				self._keys[idxs.idx][idxs.chainIdx] = key
				self._values[idxs.idx][idxs.chainIdx] = value

			self._valuesCount += 1
			return True

	def get(self, key):
		idxs = self._getIndexFromKey(key)
		if idxs.keyExists == False:
			return
		value = self._values[idxs.idx][idxs.chainIdx]
		return value

	def delete(self, key):
		idxs = self._getIndexFromKey(key)
		value = self._values[idxs.idx][idxs.chainIdx]
		self._values[idxs.idx][idxs.chainIdx] = None
		self._valuesCount -= 1
		return value

	def load(self):
		return self._valuesCount / self._size


######################### COMMAND LINE HELPER FUNCTIONS #####

def askForSize():
	while True:
		sizeStr = input("Enter hashmap size: ")
		if sizeStr.isdecimal():
			size = int(sizeStr)
			return size
		else:
			print("Size must be int greater than 0")
	return

def printHelp():
	print("\nHELP:")
	print("Type....")
	print("  %s([key], [value])" % SET_CMD)
	print("  %s([key])" 				 % GET_CMD)
	print("  %s([key])" 				 % DELETE_CMD)
	print("  %s() or..." 				 % LOAD_CMD)
	print("  %s \n" 						 % EXIT_CMD)
	return

def isFloat(string):
	try:
		floatOfStr = float(string)
		return True
	except:
		return False

def getParamsFromStringCmd(cmd):
	params = []

	commandSections = re.split("\(|\)", cmd.strip())
	if len(commandSections) <= 1:
		return
	# paramsStr will be comma-separated list of params (eg ""hi", 3")
	paramsStr = commandSections[1]
	paramsSepByQuotes = re.split("\"|\'", paramsStr)

	for idx, section in enumerate(paramsSepByQuotes):
		# if section was inside quotes, i.e. string parameter
		if idx % 2 == 1:
			params.append(section)
		else:
			paramsInThisSection = [x for x in section.replace(" ", "").split(",") if x != ""]
			if len([x for x in paramsInThisSection if not isFloat(x)]) > 0:
				print("Parameters must be string literals or numeric types.")
				return None

			params.extend(paramsInThisSection)

	return params

def executeCommand(cmd):
	# try executing corresponding command, but may fail depending on params
	if cmd == EXIT_CMD:
		sys.exit()

	# try:
	params = getParamsFromStringCmd(cmd)
	if SET_CMD in cmd:
		if len(params) != 2:
			print("`set` takes two parameters")
			return
		print(HashMap.current.set(params[0], params[1]))

	elif GET_CMD in cmd:
		if len(params) != 1:
			print("`get` takes one parameter")
			return
		print(HashMap.current.get(params[0]))

	elif DELETE_CMD in cmd:
		if len(params) != 1:
			print("`delete` takes one parameter")
			return
		print(HashMap.current.delete(params[0]))

	elif LOAD_CMD in cmd:
		if len(params) != 0:
			print("`load` takes no parameters")
			return
		print(HashMap.current.load())

	else:
		print("Not a valid function.")

	# if executing command fails, then print message and return
	# except:
	# 	print("Invalid function or parameters.")

	return


######################### MAIN ##############################

def main():
	size = askForSize()

	# initialize new hashmap & populate singleton
	current = HashMap(size)

	# let user know what functions are available
	printHelp()

	# repeatedly ask user for next fxn until they type "exit"
	while True:
		command = input("command: ")
		executeCommand(command)

	return

if __name__ == "__main__":
	main()
