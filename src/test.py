import unittest
import json
import time
import datetime
from tweets_cleaned import cleanAndFormatTweet
from tweets_cleaned import checkForUnicode
from average_degree import getUniqueEdges
from average_degree import cleanTweet
from average_degree import removeVertices
from average_degree import getNodeCount

import itertools

class scriptTests(unittest.TestCase):

	def testUnicodeCount(self):
		with open('./tweet_input/test.txt') as f:
			content = f.readlines()
		parsed_json = json.loads(content[2])
		self.assertEqual(checkForUnicode(parsed_json),0)
		
	def testParsing(self):
		with open('./tweet_input/test.txt') as f:
			content = f.readlines()
		#print content[0]
		parsed_json = json.loads(content[2])
		self.assertEqual(cleanAndFormatTweet(parsed_json), '@el_swizzlee https://t.co/IsFytngnyD (Timestamp:Fri Oct 30 15:32:16 +0000 2015)\n', "These are not the same")
		
	def testRemoveVertices(self):
		tree = [] 
		tree.append([datetime.datetime.now(), ['fun','selfie']])
		self.assertEqual(len(tree),1)
		time.sleep(2)
		tree = removeVertices(tree,datetime.datetime.now(),1)
		self.assertEqual(len(tree),0)
		
	def testUniqueEdgesUniqueNodes(self):
		tree = [] 
		tree.append([datetime.datetime.now(), ('fun','selfie')])
		tree.append([datetime.datetime.now(), ('fun','selfie')])
		tree.append([datetime.datetime.now(), ('fun','healthy')])
		uniqueEdges = getUniqueEdges(tree)
		numberOfNodes = getNodeCount(uniqueEdges)
		self.assertEqual(len(uniqueEdges),2)
		self.assertEqual(numberOfNodes,3)

def main():
    unittest.main()

if __name__ == '__main__':
    main()