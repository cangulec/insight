import sys
import json
import string
import re
import time
import htmllib

class ArgumentError(Exception):
    pass
	
def parse_arguments(argv):
	##Validate arguments
	##the script expects 2 arguments- an input file and an output file
	if len(argv) < 3:
		raise ArgumentError("Too few arguments given. Please make sure to specify input and output.")
	if len(argv) > 3:
		print "Too many arguments given. Using '%s' as input and '%s' as output." % (argv[1], argv[2])
	return argv[1],argv[2]

def cleanAndFormatTweet(tweetJSON):
	##Clean and format the tweet and timestamp according to instructions
	##Removing replacing all special characters with their counterparts in the instructions ('\t' -> ' ' etc.)
	##Note: if all characters are non-ascii unicode, the part before the timestamp will be empty
	##This function also replaces encoded HTML ("&amp;" , "&gt;") with its actual characters
	return 	"%s (Timestamp:%s)\n" % (tweetJSON['text'].encode('ascii',errors='ignore').replace('&amp;', '&').replace('&quot;', '"').replace('&apos;', "'").replace('&gt;', '>').replace('&lt;', '<').replace('\n', ' ').replace('\/', '/').replace('\r', '').replace('\\\\', '\\').replace('\t', ' ').replace('\"', '"').replace('\t', ' ').strip() , tweetJSON['created_at'])

def checkForUnicode(tweetJSON):
	##Input: Text field of 
	##Returns 1 if the text contains non-ascii unicode characters
	##Returns 0 if the text is ascii
	##Implemented this way due to legibility
	try:
		tweetJSON['text'].decode('ascii')
		return 0
	except UnicodeEncodeError:
		return 1

def main():
	##Initiate counter for tweets with non-ascii unicode characters
	tweetsWithUnicode = 0;	
	input,output =  parse_arguments(sys.argv)
	
	##Open and read all the lines of the input file. It is assumed that another script/deamon is outputting this file periodically.   
	with open(input) as f:
		content = f.readlines()
	
	#open output files to write. this assumes the user that executes this code has a read/write access in the directory.
	target = open(output, 'w')  
	
	for tweet in content:        
			##parse JSON and remove all escaped single quotes '\' 
			parsed_json = json.loads(tweet.replace(r"\'","'"))
			##try to extract fields 'text' and 'created_at'
			##if the json line does not contain either of these fields will skip the line entirely
			##e.g.  line 108 on the sample file -> '{"limit":{"track":39,"timestamp_ms":"1446218986803"}}'
			try:			
				target.write(cleanAndFormatTweet(parsed_json))
				tweetsWithUnicode = tweetsWithUnicode + checkForUnicode(parsed_json)
			except KeyError:
				pass
		
	target.write("\n%.0f tweets contained unicode\n" % tweetsWithUnicode)
	##close the file handle
	target.close()
	return len(content)
	
if __name__ == "__main__":
	start_time = time.time()
	tweetsProcessed = main()
	print("\n--- tweets_cleaned.py cleaned %s tweets in %s seconds ---" % (tweetsProcessed,(time.time() - start_time)))
