import re
import sys
import json
from time import mktime,strptime
from datetime import datetime 


def construct_tree(tree,nodes_list):
	"""
	This function constructs a dictionary representing the tree.
	Each Key is in turn a dictionary and has value representing a node with which it is linked to.
	"""

	for node_list in nodes_list:

		if len(node_list) > 1:

			for index,node in enumerate(node_list):
				if not node in tree:
					tree[node] = {}

				next_link_node = node_list[(index+1) % len(node_list)]
				tree[node][next_link_node] = 1
				
				prev_link_node = node_list[index-1]
				tree[node][prev_link_node] = 1
				

def delete_nodes(tree,nodes_list):
	"""
	This function deletes all links which are the past the 60 seconds gap.
	"""

	for node_list in nodes_list:

		if len(node_list) > 1:

			for index,node in enumerate(node_list):
				if not node in tree:
					tree[node] = {}
				next_link_node = node_list[(index+1) % len(node_list)]
				if next_link_node in tree[node]:
					del tree[node][next_link_node]
				
				prev_link_node = node_list[index-1]
				if prev_link_node in tree[node]:
					del tree[node][prev_link_node]

				if not tree[node]:
					del tree[node]


def check_to_delete(time_tree):
	"""
	This function sees which all links are to be deleted based on timestamp.
	"""

	current_epoch_time = time_tree[-1][0]
	starting_point = 0
	for index in xrange(len(time_tree)-1,-1,-1):
		if current_epoch_time - time_tree[index][0] > 60:
			starting_point = index+1

	remove_list = []

	for index2 in xrange(starting_point):
		nodes_to_remove = time_tree[index2][1]
		del time_tree[index2]
		remove_list.append(nodes_to_remove)

	return remove_list


if __name__ == "__main__":

	try:
		input_file = sys.argv[1]
		output_file = sys.argv[2]
	except:
		print "Please specify the input and output file"
		sys.exit()

	f1 = open(input_file)
	lines = f1.readlines()

	f2 = open(output_file,'w')

	time_tree = []
	node_tree = {}
	latest_degree = '0.00'

	for line in lines:

		line = line.strip()
		if not line:
                	continue

		hashtags = re.findall(r'#[a-zA-Z0-9]+',line)
		if not hashtags and not node_tree:
			f2.write(latest_degree+'\n')
			continue

		hashtags = [hashtag.lower() for hashtag in hashtags]

		try:
			ts = re.findall(r'timestamp:(.*)\)',line)[0].strip()
		except:
			continue

		temp_time = strptime(ts, "%a %b %d %H:%M:%S +0000 %Y")

		dt = datetime.fromtimestamp(mktime(temp_time))

		epoch_str = dt.strftime('%s')

		epochtime = int(epoch_str)

		time_tree.append((epochtime,hashtags))

		#print "*******************************************"

		#print "========== HASHTAGS ======================="
		print hashtags

		construct_tree(node_tree,[hashtags])

		#print "========== AFTER CONSTRUCT ================"
		print node_tree

		remove_list = check_to_delete(time_tree)

		#print "========== REMOVE LIST ===================="
		#print remove_list

		if remove_list:
			delete_nodes(node_tree,remove_list)
			#print "=========== AFTER DELETE =============="
			#print node_tree

		#print "==== FINAL TREE ====",node_tree
		total_degree = len(node_tree.values())

		if total_degree:
			avg = 0
			for value in node_tree.values():
				avg += len(value.values())
			calculation =  "%.2f" % (float(avg)/float(total_degree))
		else:
			calculation = '0.00'

		latest_degree = calculation
		
		#print("%d/%d"%(avg,total_degree))

		#print "*******************************************\n"
		f2.write(calculation+"\n")

	f2.close()




