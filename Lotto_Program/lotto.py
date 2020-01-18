import csv
import operator
import random
from math import factorial
from itertools import combinations

def updateNumOfNum(valueToUpdate):
    oldVal = dicts[valueToUpdate]
    newVal = oldVal + 1
    dicts[valueToUpdate] = newVal

def findBestReturn():
    val = range(1,50)
    arr = []
    for i in val:
        arr.append(i)
    print(arr)
    allPosComb = combinations(arr,6)
    num = 0
    for i in list(allPosComb):
        num += 1
        print(num)

def calculateProbability(value):
    prob = (float(dicts[value])/num) * 100
    print(str(value) + ": " + str(prob) + "%")

def findNumberOf(numbersarr):
    with open('/home/galliumos/Documents/Lotto649results.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        quantity = {} 
        qKey = range(0,7)
        for val in qKey:
            quantity[int(val)] = 0
        for row2 in reader:
            matchesInRow = 0
            for i in range(1,7):
                if int(row2[i]) in numbersarr:
                    matchesInRow += 1
            oldVal = quantity[matchesInRow]
            newVal = oldVal + 1
            quantity[matchesInRow] = newVal
        return quantity

def expectedValue(dictionary,numOfPlays):
    valuePerNOM = [0,0,3,10,78,2836,25127625]
    expectedVal = 0.00
    for value in range(0,7):
        probability = float(dictionary[value])/float(numOfPlays)
        v1 = (probability*valuePerNOM[value])
        expectedVal += v1 
    expectedVal -= 3.00
    expectedVal = round(expectedVal,2)
    return expectedVal; 

def nCr(n,r):
    choose = (factorial(n)/(factorial(r)*(factorial(n-r))))
    return choose

def getNumbersToCheck():
    numbersToCheck = []
    while(len(numbersToCheck)<6):
        newNumber = raw_input("Add a number > 0 and < 50 that is not already in the set: ")
        if 1 <= int(newNumber) <= 49:
            if int(newNumber) in numbersToCheck:
                print("Number is currently in list")
            else:
                numbersToCheck.append(int(newNumber))
                print(numbersToCheck)
    numbersToCheck.sort()
    print("Your 6 numbers: " + str(numbersToCheck))
    return numbersToCheck

def getNumberOfRows():
    with open('/home/galliumos/Documents/Lotto649results.csv') as csvfile:
        reader1 = csv.reader(csvfile, delimiter=',')
        numberOfPlays = 0
        for row1 in reader1:
            numberOfPlays += 1
        return numberOfPlays

def generateRandomInput():
    generatedRandomNumbers = []
    while(len(generatedRandomNumbers)<6):
        newNumber = random.randrange(1,50,1)
        if int(newNumber) in generatedRandomNumbers:
            e = 1
        else:
            generatedRandomNumbers.append(int(newNumber))
    generatedRandomNumbers.sort()
    return generatedRandomNumbers


def findFrequency(freqValue, reader):
    dicts ={}
    key = range(1,50)
    for j in key:
        dicts[str(j)] = 0
    for row in reader:
        for i in range(1,7):
            currVal = row[i]
            updateNumOfNum(currVal)
    sorted_dictionary = sorted(dicts.items(), key=lambda kv: kv[1], reverse=True)
    print(sorted_dictionary)

def makeSetOfXSets(x):
    setOfSets = []
    while(len(setOfSets)<x):
        setOfSets.append(generateRandomInput())
    return setOfSets

def estimatedReturnForXTickets(x):
    numberOfPlays = getNumberOfRows()
    setOfSets = makeSetOfXSets(x)
    total = 0.00
    for i in setOfSets:
        quantityOfNums = findNumberOf(i)
        toAdd = float(expectedValue(quantityOfNums,numberOfPlays))
        total += toAdd
        print("subtotal: " + str(total) + " $" + str(toAdd))
    print("total: " + str(total))

with open('/home/galliumos/Documents/Lotto649results.csv') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    estimatedReturnForXTickets(1000)
    
 
  