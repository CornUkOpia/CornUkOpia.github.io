import tkinter
from tkinter import *
import os
import math
import csv


def buildInitialCityObject(row, dictionary):
    city = {
        "latitude" : row[1],
        "longitude": row[2],
        "population": row[7],
        "x": 0,
        "y": 0
    }
    if("city" not in row[0]):
        dictionary[row[0]] = city
    return dictionary

def buildWindow(dictionary):
    top = tkinter.Tk()
    mapOfCanada = str(os.path.dirname(os.path.realpath(__file__))) + "\map.gif"
    mOc = PhotoImage(file=mapOfCanada)
    canvas = Canvas(top, width=1200, height=900)
    canvas.pack(expand=YES, fill=BOTH)
    canvas.create_image(583.5,368.5, image=mOc)
    x = 845
    y = 660
    canvas.create_oval(x,y,x+10,y+10,fill="black",tag="Ottawa")
    canvas.tag_bind("Ottawa",'<ButtonPress-1>',displayCityInfo)
    dictionary = buildCityObject(canvas, "Ottawa",dictionary,x,y)
    x = 800
    y = 695
    canvas.create_oval(x,y,x+10,y+10,fill="black",tag="Toronto")
    canvas.tag_bind("Toronto",'<ButtonPress-1>',displayCityInfo)
    dictionary = buildCityObject(canvas, "Toronto",dictionary,x,y)
    x = 875
    y = 660
    canvas.create_oval(x,y,x+10,y+10,fill="black",tag="Montreal")
    canvas.tag_bind("Montreal",'<ButtonPress-1>',displayCityInfo)
    cityDictionary = buildCityObject(canvas, "Montreal",dictionary,x,y)
    print("citydictionary")
    print(cityDictionary)
    canvas.pack()
    top.mainloop()

def buildCityObject(canvas,cityName, dictionary, x, y):
    dictionary = AddAttributeTo(dictionary, cityName, "x", x)
    dictionary = AddAttributeTo(dictionary, cityName, "y", y)
    print(cityName)
    print(dictionary[cityName])
    return dictionary

def displayCityInfo(event):
    print("event")
    print(event)
    currentCity = determineCityFromCoordinates(event.x, event.y)
    print("Current City:")
    print(currentCity)
    print(cityDictionary[currentCity])

def determineCityFromCoordinates(x,y):
    for key in cityDictionary:
        if cityDictionary[key]["x"] < x+10 and cityDictionary[key]["x"] >= x - 10:
            return key

def AddAttributeTo(dictionary, dictionaryKey,attributeToAddName, attributeToAddValue):
    dictionary[dictionaryKey][attributeToAddName] = attributeToAddValue
    return dictionary
    
def longAndLatToXY(cityObj):
    mapHeight = 737.00
    mapWidth = 1167.00
    x = float((mapWidth/360.00) * (180 + cityObj.latitude))
    print(x)
    y = float((mapHeight/180.00) * (90 + cityObj.longitude))
    print(y)

def getUnsuitableHousingData(filename):
    pathName = str(os.path.dirname(os.path.realpath(__file__))) + filename
    with open(pathName) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        firstRow = next(reader)
        print("firstrow: " + str(firstRow[5]) + " : " + str(firstRow[22]) + "  " + str(firstRow[23]) + "  " + str(firstRow[24]))
        for row in reader:
            
            # row[5]
            print(str(row[5]) + " : " + str(row[22]) + "  " + str(row[23]) + "  " + str(row[24]))


pathNameOfCityData = str(os.path.dirname(os.path.realpath(__file__))) + "\CanadianCityData.csv"
with open(pathNameOfCityData) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    cityDictionary = {}
    for row in reader:
        cityDictionary = buildInitialCityObject(row, cityDictionary)
    getUnsuitableHousingData("\CMA_CA_RMR_AR.csv")
    #buildWindow(cityDictionary)   

