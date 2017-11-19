# Heejung Chung, KPCB 2018 Application, Stanford Class of '21
# TO RUN:
# 	1. open terminal
# 	2. type... $ python3 test.py

import sys
import unittest
import string
import random
import pdb
from collections import namedtuple
# my file...
import hashmap

KEY_STRING_LEN = 6
MIN_HASHMAP_SIZE = 1
MAX_HASHMAP_SIZE = 100

class HashmapTestSuper(unittest.TestCase):

	def generateUniqueString(self): # actually not entirely unique, only unique among hashmap keys
		while True: # safeguard against generating key that happens to already exist
			randomString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(KEY_STRING_LEN))
			if hashmap.HashMap.current.get(randomString) == None:
				return randomString
		return

	def setRandomKeyValuePair(self):
		randomKey = self.generateUniqueString()
		randomVal = self.generateUniqueString()
		success = hashmap.HashMap.current.set(randomKey, randomVal)
		KeyValuePair = namedtuple("KeyValuePair", "key value success")
		return KeyValuePair(randomKey, randomVal, success)

	def setUp(self):
		# will remain constant throughout test case
		self.HASHMAP_SIZE = random.randint(MIN_HASHMAP_SIZE, MAX_HASHMAP_SIZE)
		hashmap.HashMap(self.HASHMAP_SIZE)
		return

	def tearDown(self):
		# reset singleton
		hashmap.HashMap.current = None
		return


class SetTestCase(HashmapTestSuper):

	def test_set_pass(self):
		keyValPair = self.setRandomKeyValuePair()
		self.assertTrue(keyValPair.success)
		self.assertEqual(keyValPair.value, hashmap.HashMap.current.get(keyValPair.key))
		return

	def test_set_fail(self):
		for i in range(self.HASHMAP_SIZE):
			self.setRandomKeyValuePair()
		success = self.setRandomKeyValuePair().success
		self.assertFalse(success)
		return


class GetTestCase(HashmapTestSuper):

	def test_get_fail(self): # no test_get_passed, bc indirectly tested in SetTest
		self.assertEqual(None, hashmap.HashMap.current.get(self.generateUniqueString()))
		return


class DeleteTestCase(HashmapTestSuper):

	def test_delete_pass(self):
		keyValPair = self.setRandomKeyValuePair()
		deletedVal = hashmap.HashMap.current.delete(keyValPair.key)
		self.assertEqual(keyValPair.value, deletedVal)
		return

	def test_delete_fail(self):
		deletedVal = hashmap.HashMap.current.delete(self.generateUniqueString())
		self.assertEqual(None, deletedVal)
		return

class LoadTestCase(HashmapTestSuper):
	randomKeys = []

	def setUp(self):
		super().setUp()
		self.NUM_VALUES_TO_LOAD = random.randint(MIN_HASHMAP_SIZE, self.HASHMAP_SIZE)
		while len(self.randomKeys) < self.NUM_VALUES_TO_LOAD:
			pair = self.setRandomKeyValuePair()
			if pair.success:
				self.randomKeys.append(pair.key)
		return

	def test_load_pass(self):
		loadVal = self.NUM_VALUES_TO_LOAD / self.HASHMAP_SIZE
		self.assertEqual(hashmap.HashMap.current.load(), loadVal)
		return


def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(SetTestCase))
	suite.addTest(unittest.makeSuite(GetTestCase))
	suite.addTest(unittest.makeSuite(DeleteTestCase))
	suite.addTest(unittest.makeSuite(LoadTestCase))
	return suite

def main():
	testRunner = unittest.TextTestRunner(verbosity=2)
	testSuite = suite()
	testRunner.run(testSuite)
	print("finished")
	return

if __name__ == "__main__":
	main()
