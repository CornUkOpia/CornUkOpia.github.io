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
    mapOfCanada = str(os.path.dirname(os.path.realpath(__file__))) + "\map.gif"
    mOc = PhotoImage(file=mapOfCanada)
    canvas.pack(expand=YES, fill=BOTH)
    label1 = tkinter.Label(canvas, text="Show Cities with Climate Action Spending greater than: ")
    label1.place(x=10, y=780)
    showCitiesWithCAS = Button(top, text="Submit", command=showCitiesWithCASpending)
    showCitiesWithCAS.place(x=150,y=800)
    resetButton = Button(top, text="Reset", command=reset)
    resetButton.place(x=10,y=850)
    canvas.create_image(583.5,368.5, image=mOc)
    showCitiesWithLROUH = Button(top, text="Show Cities with Decreasing Unaffordable Housing Rate", command=showCitiesWithDecreasingUnaffordableHousing)
    showCitiesWithLROUH.place(x=10,y=740)
    canvas.create_rectangle(1170,10, 1600, 710, outline="#000", fill="#FFF")
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
    canvas.create_oval(x,y,x+10,y+10,fill="black",tag="Montréal")
    canvas.tag_bind("Montréal",'<ButtonPress-1>',displayCityInfo)
    dictionary = buildCityObject(canvas, "Montréal",dictionary,x,y)
    x = 990
    y = 675
    canvas.create_oval(x,y,x+10,y+10,fill="black",tag="Halifax")
    canvas.tag_bind("Halifax",'<ButtonPress-1>',displayCityInfo)
    dictionary = buildCityObject(canvas, "Halifax",dictionary,x,y)
    x = 255
    y = 590
    canvas.create_oval(x,y,x+10,y+10,fill="black",tag="Vancouver")
    canvas.tag_bind("Vancouver",'<ButtonPress-1>',displayCityInfo)
    dictionary = buildCityObject(canvas, "Vancouver",dictionary,x,y)
    x = 350
    y = 490
    canvas.create_oval(x,y,x+10,y+10,fill="black",tag="Edmonton")
    canvas.tag_bind("Edmonton",'<ButtonPress-1>',displayCityInfo)
    dictionary = buildCityObject(canvas, "Edmonton",dictionary,x,y)
    x = 340
    y = 550
    canvas.create_oval(x,y,x+10,y+10,fill="black",tag="Calgary")
    canvas.tag_bind("Calgary",'<ButtonPress-1>',displayCityInfo)
    dictionary = buildCityObject(canvas, "Calgary",dictionary,x,y)
    x = 580
    y = 580
    canvas.create_oval(x,y,x+10,y+10,fill="black",tag="Winnipeg")
    canvas.tag_bind("Winnipeg",'<ButtonPress-1>',displayCityInfo)
    dictionary = buildCityObject(canvas, "Winnipeg",dictionary,x,y)
    canvas.pack()
    top.mainloop()

def reset():
    for x in cityDictionary:
        canvas.itemconfigure(str(x),fill="black")

def showCitiesWithCASpending():
    for x in cityDictionary:
        if "Climate Action Spending" in cityDictionary[x]:
            if int(entryBox.get()) <  int(cityDictionary[x]["Climate Action Spending"]):
                canvas.itemconfigure(str(x),fill="green")

def showCitiesWithDecreasingUnaffordableHousing():
    for x in cityDictionary:
        if "Rate of Unaffordable Housing" in cityDictionary[x]:
            if cityDictionary[x]["Rate of Unaffordable Housing"]["2006"] >  cityDictionary[x]["Rate of Unaffordable Housing"]["2016"]:
                canvas.itemconfigure(str(x),fill="red")


def buildCityObject(canvas,cityName, dictionary, x, y):
    dictionary = AddAttributeTo(dictionary, cityName, "x", x)
    dictionary = AddAttributeTo(dictionary, cityName, "y", y)
    return dictionary

def displayCityInfo(event):
    currentCity = determineCityFromCoordinates(event.x, event.y)
    canvas.create_rectangle(1170,10, 1600, 710, outline="#000", fill="#FFF")
    canvas.create_text(1200,100,text=currentCity)
    ycoor = 120
    for i in cityDictionary[currentCity]:
        line = i + ": " + str(cityDictionary[currentCity][i])
        canvas.create_text(1400,ycoor,text=line)
        ycoor += 20

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

def getUnsuitableHousingData(filename, dictionary):
    pathName = str(os.path.dirname(os.path.realpath(__file__))) + filename
    with open(pathName) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        firstRow = next(reader)
        for row in reader:
            if row[5] in dictionary:
                unsuitableHousingDict = {
                    "2006": row[22],
                    "2011": row[23],
                    "2016": row[24]
                }
                cityDictionary = AddAttributeTo(dictionary,row[5],"Rate of Unaffordable Housing",unsuitableHousingDict)
    return cityDictionary

def getSchoolAndEnvironmentSpending(filename, dictionary):
    pathName = str(os.path.dirname(os.path.realpath(__file__))) + filename
    with open(pathName) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        firstRow = next(reader)
        #print("firstrow: " + str(firstRow[5]) + " : " + str(firstRow[22]) + "  " + str(firstRow[23]) + "  " + str(firstRow[24]))
        for row in reader:
            if row[0] in dictionary:
                cityDictionary = AddAttributeTo(dictionary,row[0],firstRow[1],row[1])
                cityDictionary = AddAttributeTo(dictionary,row[0],firstRow[2],row[2])
    return cityDictionary    

def checkIfInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


def getClimateActionSpending(filename, dictionary):
    pathName = str(os.path.dirname(os.path.realpath(__file__))) + filename
    with open(pathName) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        firstRow = next(reader)
        #print("firstrow: " + str(firstRow[5]) + " : " + str(firstRow[22]) + "  " + str(firstRow[23]) + "  " + str(firstRow[24]))
        for row in reader:
            if row[22] in dictionary:
                value = str(row[14]).replace(" ","")
                value = value.replace("$","").split(".")
                value = value[0].replace(",","")
                if checkIfInt(value) == True:
                    if "Climate Action Spending" in dictionary[row[22]]:
                        totalSpending = dictionary[row[22]]["Climate Action Spending"]
                        dictionary[row[22]]["Climate Action Spending"] = int(totalSpending) + int(value)
                    else:
                        dictionary = AddAttributeTo(dictionary,row[22],"Climate Action Spending",int(value))
    print(dictionary)
    cityDictionary = dictionary
    return cityDictionary

pathNameOfCityData = str(os.path.dirname(os.path.realpath(__file__))) + "\CanadianCityData.csv"
with open(pathNameOfCityData) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    top = tkinter.Tk()
    canvas = Canvas(top, width=1600, height=900)
    entryBox = tkinter.Entry(canvas)
    entryBox.place(x=10, y=805)
    cityDictionary = {}
    for row in reader:
        cityDictionary = buildInitialCityObject(row, cityDictionary)
    cityDictionary = getUnsuitableHousingData("\CMA_CA_RMR_AR.csv",cityDictionary)
    cityDictionary = getSchoolAndEnvironmentSpending("\CANDEVEconAndEducationSpending.csv",cityDictionary)
    cityDictionary = getClimateActionSpending("\climateActionSpending.csv",cityDictionary)
    #print(cityDictionary)
    buildWindow(cityDictionary)   

