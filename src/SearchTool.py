'''
Created on 10/10/2017

@author: Connor Hewett 15903849 & Craig Fraser 15889604 
'''

import Spider
import SpiderLeg
import codecs
from operator import itemgetter
import urllib.parse

# if keyword in meta keywords, add to list, write to txt & display to screen
maxDepth = 3 # the max depth the crawl will travel
RESULT_URL = 0 # Index position for URL
RESULT_RANK = 1 # Index position for Page Rank
changing = True # True if the PageRank Vector is changing notably, False once the change is less than DELTA
DELTA = 0.0001 # Once the change between page rank values after an interation is less than this, stop calculating
RESULTS_FILE_NAME = "results.txt"

seeds = []

# list for seed URLs that user inputs
usrInput = input("Enter seed URL or press ENTER to continue: ")

while (usrInput != "" and usrInput != " "):
	check = urllib.parse.urlparse(usrInput)
	if check.netloc != '' and check.scheme != '':
		seed = [0, usrInput]
		seeds.append(seed)
	else:
		print('Invalid URL')
	usrInput = input("Enter seed URL or press ENTER to continue: ")
		
keyword = input("Enter keyword to search for: ").lower() 

spider = Spider.Spider(seeds, maxDepth, keyword) # Create spider object initialised with the users seed urls and keyword
spider.crawl() # Start crawling process

results = spider.results # Get list of URL results from the Spider
adjList = spider.adjacencyList
c = 0.15 # This is the damping factor
pArray = [[0 for col in range(len(adjList))] for row in range(len(adjList))] # Stores the page ranks matrix
vArray = [1/len(adjList) for col in range(len(adjList))] # PageRank Vector
temp = [0 for col in range(len(adjList))]
rankRes = [] # Store the results hyperlinks and corresponding page rank centrality

# Calculate PageRank Matrix
for i in range(len(adjList)):
	if len(adjList[i]) == 0:
		for j in range(len(adjList)):
			pArray[i][j] = 1.0 / len(adjList) # If node is a sink
	else:
		for k in range(len(adjList)):
			if k in adjList[i]:
				pArray[i][k] = (1.0 - c) / len(adjList) + c/len(adjList[i]) # if k is connected to node i's
			else:
				pArray[i][k] = (1.0 - c) / len(adjList) # otherwise

				
# Transform the PageRank Matrix (flip along main diagonal)
for i in range(0, len(adjList)):
	for j in range(i+1, len(adjList)):
		pArray[i][j],pArray[j][i] = pArray[j][i],pArray[i][j]
		

# Calculate the PageRank Vector
while changing: #for i in range(len(adjList)): # instead of this, while change isnt much
	for j in range(len(adjList)):
		for k in range(len(adjList)):
			temp[j] += (pArray[j][k] * vArray[k])
		if (abs(vArray[j] - temp[j]) < DELTA):
			changing = False
		else:
			changing = True
	
	vArray = temp
	temp = [0 for col in range(len(adjList))]

# Create list of URL results with their corresponding Page Rank values
for i in range(len(spider.results)):
	rankRes.append([spider.visited.index(spider.results[i]), vArray[spider.visited.index(spider.results[i])]])

rankRes.sort(key=lambda tup: tup[1], reverse=True) # Sort the results from highest PageRank to lowest

# Print the Results in order of highest to lowest PageRanks and write to a text file
file = open(RESULTS_FILE_NAME, "w")
i = 1
print("\n===KEYWORD MATCHES===")
for y in range(len(rankRes)):
	print(i, ": ", spider.visited[rankRes[y][RESULT_URL]].encode('850', 'ignore').decode('850')) 
	file.write(spider.visited[rankRes[y][RESULT_URL]].encode('850', 'ignore').decode('850')+'\r\n') # Write the results to a text file
	print("  ", SpiderLeg.getTitle(spider.visited[rankRes[y][RESULT_URL]]).encode('850', 'ignore').decode('850'))
	print("  (Rank: ", rankRes[y][RESULT_RANK], ")\n")
	i+=1
print("")
file.close()