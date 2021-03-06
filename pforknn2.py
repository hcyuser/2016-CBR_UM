import csv
import random
import math
import operator

trainingSet=[]
testSet=[]

with open('travel.csv','rb') as csvfile:
	lines=csv.reader(csvfile)
	for row in lines:
		print ','.join(row)


def loadDataset(filename, split):
	global trainingSet
	global testSet
	# type: (object, object, object, object) -> object
	with open(filename,'rb') as csvfile:
		lines=csv.reader(csvfile)
		dataset=list(lines)
		for x in range(len(dataset)-1):
			for y in range(5):
				dataset[x][y]=float(dataset[x][y])
			if random.random() < split:
				trainingSet.append(dataset[x])
			else:
				testSet.append(dataset[x])


def euclideanDistance(instance1,instance2,length):
	distance=0
	for x in range(length):
		distance += pow((instance1[x]-instance2[x]),2)
	return math.sqrt(distance)



def getNeighbors(testInstance, k):
	global trainingSet
	distances = []
	length=len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance,trainingSet[x],length)
		distances.append((trainingSet[x],dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors=[]
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def getResponse(neighbors):
	classVotes={}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response]+=1
		else:
			classVotes[response]=1
	sortedVotes= sorted(classVotes.iteritems(),key=operator.itemgetter(1),reverse=True)
	return sortedVotes[0][0]

def getAccuracy(predictions):
	global testSet
	correct=0
	for x in range(len(testSet)):
		if testSet[x][-1]== predictions[x]:
			correct += 1
	return (correct/float(len(testSet)))*100.0


def main():
	global trainingSet
	global testSet
	split=0.67
	loadDataset('travel.csv',split)
	print'Train Set:' + repr(len(trainingSet))
	print'Test Set:' + repr(len(testSet))

	predictions=[]
	k=3
	for x in range(len(testSet)):
		neighbors = getNeighbors(testSet[x],k)
		result = getResponse(neighbors)
		predictions.append(result)
		print('> predicted='+ repr(result) + ',actual ='+ repr(testSet[x][-1]))
	accuracy = getAccuracy(predictions)
	print('Accuracy:' + repr(accuracy)+'%')



main()