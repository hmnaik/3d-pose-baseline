
# The file is used to prepare the dataset required for the 3D from 2D algorithm

import glob
import os
import pandas as pd

def getData(path, dims = 3):
    dir = path
    print("File exists", os.path.exists(dir))
    files = glob.glob(dir)
    files = [x for x in files if x.endswith(".csv")]

    trainDict = {}
    testDict = {}
    dataDict = {}
    for i in range(len(files)):
        file = files[i]
        fileName = file.split(".csv")[0]
        frame = pd.read_hdf(fileName + ".h5", "{0}DPositions".format(dims))
        frame = changeOrder(frame, dims)
        dataDict[fileName] = frame.as_matrix()

        print("{0}D position {1}: \n {2}".format(dims, frame.columns.tolist(), dataDict[fileName].shape))

    # if dims == 3:
    #     process3DData(dataDict)

    for fileName,i in zip(dataDict,range(len(dataDict))):
        if i != len(dataDict)-1:
            trainDict[("1","Directions",fileName+ ".h5" )] = dataDict[fileName]
        else:
            testDict[("9","Directions",fileName+ ".h5" )] = dataDict[fileName]

    return trainDict, testDict

def switch(headIndex, shoulderIndex, list):
    newList = list[:]
    for hIndex,sIndex in zip(headIndex,shoulderIndex):
        newList[hIndex] = list[sIndex]
        newList[sIndex] = list[hIndex]
    print(newList)
    return newList

def changeOrder(frame, dims):
    print("Changing order of joint")
    columnsList = frame.columns.tolist()
    hbx = columnsList.index("head_beak_{0}d_x".format(dims))
    lsx = columnsList.index("body_leftShoulder_{0}d_x".format(dims))
    if dims == 3:
        headIndex = [hbx, hbx + 1, hbx + 2]
        shoulderIndex = [lsx, lsx + 1, lsx + 2]
    else:
        headIndex = [hbx, hbx + 1]
        shoulderIndex = [lsx, lsx + 1]

    newList = switch(headIndex, shoulderIndex, columnsList)
    print("New List : ", frame.iloc[0])
    retFrame = frame[newList]
    print("New List : ", retFrame.iloc[0])
    return retFrame


def process3DData(dataDict, originCamID ="2118670", replaceCamID = "2119571"):

    # change the database
    for data in dataDict :
        if replaceCamID in data:
            fileName = data
            print(" Original File Name : ", fileName)
            replacedFileName = fileName.replace(replaceCamID,originCamID)
            print(" Replaced File Name : ", replacedFileName)
            dataDict[data] = dataDict[replacedFileName]



if __name__ == "__main__":
    path = "./testDatasetBirdTracking/*"
    train2D, test2D = getData(path, dims  = 2)
    train3D, test3D = getData(path, dims = 3)


    print(os.path.exists(path))
