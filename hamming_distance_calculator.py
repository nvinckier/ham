#!/usr/bin/python3

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Sample sheet opening and parsing function

def open_SS(file):
    df=""
    num=""
    indexes=""
    df=pd.read_csv(file,sep=',')

    if '[Data]' in str(df.columns):
        num=0
    else:
        for line in range(0,len(df)-1):
            if '[Data]' in str(df.loc[line]):
                num=line
    if num=="":
        print("No [Data] section found! Please check sample sheet for errors.")

    dataSection=df.iloc[num+2:len(df)]
    dataSection.columns=df.iloc[num+1].values

    if 'index2' in dataSection.columns:
        if 'index' in dataSection.columns:
            indexes=pd.DataFrame()
            indexes['index']=dataSection['index']
            indexes['index2']=dataSection['index2']
            indexSeries=indexes['index']+"+"+indexes['index2']
        elif 'Index' in dataSection.columns:
            indexes=pd.DataFrame()
            indexes['index']=dataSection['Index']
            indexes['index2']=dataSection['index2']
            indexSeries=indexes['index']+"+"+indexes['index2']
        else:
            print("No index column found! Please check sample sheet for errors.")
    elif 'Index2' in dataSection.columns:
        if 'index' in dataSection.columns:
            indexes=pd.DataFrame()
            indexes['index']=dataSection['index']
            indexes['index2']=dataSection['Index2']
            indexSeries=indexes['index']+"+"+indexes['index2']
        elif 'Index' in dataSection.columns:
            indexes=pd.DataFrame()
            indexes['index']=dataSection['Index']
            indexes['index2']=dataSection['Index2']
            indexSeries=indexes['index']+"+"+indexes['index2']
        else:
            print("No index column found! Please check sample sheet for errors.")
    elif 'index' in dataSection.columns:
            indexes=pd.DataFrame()
            indexes['index']=dataSection['index']
            indexSeries=indexes['index']
    elif 'Index' in dataSection.columns:
            indexes=pd.DataFrame()
            indexes['index']=dataSection['Index']
            indexSeries=indexes['index']
    else:
        print("No index column found! Please check sample sheet for errors.")
#     display(indexes['index']+"+"+indexes['index2'])
    return indexSeries

# Hamming distance calculation function

def hamming_distance(string1, string2):
    # Start with a distance of zero, and count up
    distance = 0
    # Loop over the indices of the string
    L = len(string1)
    for i in range(L):
        # Add 1 to the distance if these two characters are not equal
        if string1[i] != string2[i]:
            distance += 1
    # Return the final count of differences
    return distance

# Request for sample sheet filename

# sampleSheet = "C:\\Users\\nvinckier\\OneDrive\\scripts\\barcode\\SampleSheet.csv"
# sampleSheet = "C:\\Users\\nvinckier\\OneDrive\\scripts\\barcode\\test.csv"
sampleSheet = ""
sampleSheet = input('Please input a file name:\n')
if sampleSheet == "":
	sampleSheet = "SampleSheet.csv"
indexSeries=""
indexSeries=open_SS(sampleSheet)
indexList=list(indexSeries)
items=len(indexList)
# print(items)
hamDistList=pd.DataFrame({'First index string':[],'Second index string':[],'Hamming Distance':[]})
for num1 in range(0,items):
#     print(num1)
    str1=indexList[num1]
    for num2 in range(0,items):
        if num1 != num2:
            str2=indexList[num2]
            hamDist=hamming_distance(str1,str2)
            newRow = {'First index string':str1, 'Second index string':str2, 'Hamming Distance':hamDist}
            hamDistList = hamDistList.append(newRow, ignore_index=True)
pd.set_option('precision',0)
print(hamDistList)
#             print('The Hamming distance between ' + str1.upper() + ' and ' + str2.upper() + ' is: ' + str(hamDist))
