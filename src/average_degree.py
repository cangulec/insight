from __future__ import division
import sys
import json
import string
from datetime import datetime,timedelta
import itertools
import re
import time

class ArgumentError(Exception):
    pass
def parse_arguments(argv):
	if len(argv) < 3:
		raise ArgumentError("Too few arguments given. Please make sure to specify input and output.")
	if len(argv) > 3:
		print "Too many arguments given. Using '%s' as input and '%s' as output." % (argv[1], argv[2])
	return argv[1],argv[2]

def cleanTweet(tweetText):
	##Clean hashtags according to instructions
	##Removing replacing all special characters with their counterparts in the instructions ('\t' -> ' ' etc.)
	##Note: if all characters are non-ascii unicode, will return blank
	return 	"%s" % (tweetText.encode('ascii',errors='ignore').replace('\n', ' ').replace('\/', '/').replace('\r', '').replace('\\\\', '\\').replace('\t', ' ').replace('\"', '"').replace('\t', ' ').strip().lower() )
	
def generate_graphviz_output(set):
	graphviz = open("tweet_output/graphviz.txt", 'w')
	graphviz.write("graph G {")
	for eachpair in set:
		for i,eachvalue in enumerate(eachpair):
			graphviz.write("\"")
			graphviz.write(eachvalue.replace('#',''))
			graphviz.write("\"")
			if i < len(eachpair)-1:
					graphviz.write(" -- ")
		graphviz.write(";\n")
	graphviz.write("}")
	
def getTimeStampFromJson(json):
	#convert 'created_at' string from JSON to datetime object
	ts = datetime.strptime(json['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
	return ts

def removeVertices(old_list,mostRecentTweetTimeStamp,timeframe):
	##check each Vertices in 'tree'
	##if timestamps is more than 'timeframe' seconds away, remove from the graph
	updatedVertices = []
	for item in old_list:
		#[0]th element contains the timestamp
		if (mostRecentTweetTimeStamp - item[0]) <= timedelta(seconds = timeframe):
			updatedVertices.append(item)
	return updatedVertices

def getUniqueEdges(tree):
	##receives the graph (each edge) as input
	##returns values of the unique edges
	##this necessary because the tree can contain multiple edges of the same pair
	##e.g if two tweets that contain the same 2 hash-tags come at different times, there will be two entries in tree to account for both tweets
	## tweet1-> (time1, hashtag1,hashtag2)
	## tweet2-> (time2, hashtag1,hashtag2)
	##this function removes duplicate pairs
	return set([x[1] for x in tree])
	
def getNodeCount(tree):
	##given every pair of vertices
	##count the number of unique nodes
	my_set = set()
	for pair in tree:
		for item in pair:
			my_set.update([item])
	return len(my_set)

def main():
	#Look back period (in number of seconds) while processing current tweet
	LOOKBACK_PERIOD_IN_SECONDS = 60
	input,output =  parse_arguments(sys.argv)
	##Open and read all the lines of the input file. It is assumed that another script/deamon is outputting this file periodically.
	##This line would need to be modified if we were dealing with data sets larger than computers dynamic memory.    
	with open(input) as f:
		content = f.readlines()	
		
	#open output files to write. this assumes the user that executes this code has a read/write access in the directory.
	target = open(output, 'w')
	
	## add all of them to list - there will be duplicate nodes
	##remove them while you are calculating
			
	##Initiate the graph
	##tree will contain each edge along with the timestamp of that edge
	##e.g. (timestamp, node1, node2)
	tree = []
	
	for tweet in content:        
			##parse JSON and remove all escaped single quotes '\' 
			parsed_json = json.loads(tweet.replace(r"\'","'"))
			##try to extract fields 'text' and 'created_at'
			##if the json line does not contain either of these fields will skip the line entirely
			##e.g.  line 108 on the sample file -> '{"limit":{"track":39,"timestamp_ms":"1446218986803"}}'
			try:	
				currentTweetTimeStamp = getTimeStampFromJson(parsed_json)
				##Extract and clean unique hashtags from json
				hashtags = []
				for hashtag in parsed_json['entities']['hashtags']:
					cleanHashtag = cleanTweet(hashtag['text'])
					if cleanHashtag <> '':
						hashtags.append(cleanHashtag)
				##remove duplicate hashtags on the same tweet
				hashtags =list(set(hashtags))	
				##if there is more than 1 hash-tag in the tweet, add every combination to the tree (e.g. 3 hash-tags will give 6 unique combinations/edges)
				if len(hashtags) > 1:
					for pair in itertools.combinations(hashtags, 2):
						tree.append([currentTweetTimeStamp,pair])
					
				##Delete all vertices that are older than the lookback period
				tree = removeVertices(tree,currentTweetTimeStamp,LOOKBACK_PERIOD_IN_SECONDS)
				##tree may contain duplicate edges, since the edges in the tree also contain timestamp information
				uniqueEdges = getUniqueEdges(tree)
				##figure out how many nodes there are in the graph
				numberOfNodes = getNodeCount(uniqueEdges)
				##total connections in the graph is number of edges * 2
				##if a is connected to b, this is counted as two connections
				totalEdges = len(uniqueEdges)*2
				##if there are no edges, the rolling average will default to 0.00
				rollingAverage = 0.00
				if len(uniqueEdges)>0:
					rollingAverage = round(totalEdges/numberOfNodes,5)
				target.write(" %.2f\n" % rollingAverage ) 
			except KeyError:
				pass

	##will generate actual visuals for the last tweet in the input file
	generate_graphviz_output(uniqueEdges)
	#print tree
	target.close()
	return len(content)
	
if __name__ == "__main__":
	start_time = time.time()
	tweetsProcessed = main()
	print("\n--- average_degree.py processed %s tweets in %s seconds ---" % (tweetsProcessed,(time.time() - start_time)))




