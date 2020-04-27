import ROOT
import os
import numpy
import subprocess
import root_numpy
import math
import copy


def loopOver(path,pathList):
        for filename in os.listdir(path):
                pathNew=path+"/"+filename
                if os.path.isfile(pathNew) and pathNew.endswith(".root"):
                        pathList.append(pathNew)
                elif os.path.isdir(pathNew):
                        loopOver(pathNew,pathList)
        #return pathList

def getBkg(path,name):
        pathList=[]
        for filename in os.listdir(path):
                pathNew=path+"/"+filename
                if os.path.isdir(pathNew) and filename.startswith(name):
                        loopOver(pathNew,pathList)
        return pathList

