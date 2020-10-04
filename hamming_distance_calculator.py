#!/usr/bin/python3

import sys
import getopt
import pandas as pd
import numpy as np
import os

# Command line arguments
sample_sheet_file = None    # -i
hamming_distance_maximum = 3    # -d

# process_args - Process command line arguments and update globals variables.
def process_args():
    global sample_sheet_file, hamming_distance_maximum

    if len(sys.argv) <= 1:
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:d:h")
    except Exception:
        usage()
        sys.exit(1)

    for o, a in opts:
        if o == "-i":
            sample_sheet_file = a
        if o == "-d":
            hamming_distance_maximum = a
        if o == "-h":
            usage()

def usage():
    print("")
    print("                                 )\\   /|")
    print("                              .-/'-|_/ |")
    print("           __            __,-' (   / \\/")
    print("       .-'\"  \"'-..__,-'\"\"          -o.`-._")
    print("      /                                   (\")")
    print("*--._ ./      Hamming                  ___.-'")
    print("    |         Distance             _.-' ")
    print("    :         Calculator        .-/   ")
    print("     \\        0.2.0          )_ /")
    print("      \\                _)   / \\(")
    print("        `.   /-.___.---'(  /   \\\\ ")
    print("         (  /   \\\\       \\(     L\\ ")
    print("          \\(     L\\       \\\\ ")
    print("           \\\\              \\\\ ")
    print("            L\\              L\\ ")
    print("")
    print("Usage: hamming_distance_calculcator.py [Options] -i <SampleSheet CSV File>")
    print("")
    print("[Options]")
    print("    -d <string>                Maximum hamming distance to report. Default = 3")
    print("    -i <path/to/SampleSheet>   Sample sheet expected in standard CSV format with [Data] section")
    print("")
    sys.exit(1)

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

####################################################################################################
# Main function
def main():
    global sample_sheet_file, hamming_distance_maximum
    process_args()
    print("Reporting indexes with hamming distance of %s or less" % hamming_distance_maximum)
    if str(type(sample_sheet_file)) == "<class 'NoneType'>":
        sample_sheet_file = sys.argv[len(sys.argv) - 1]
        print("Sample sheet is: " + str(sample_sheet_file))
    if not os.path.exists(sample_sheet_file):
        print("ERROR: Sample sheet %s does not exist" % sample_sheet_file)
        usage()

    indexSeries=""
    indexSeries=open_SS(sample_sheet_file)
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
                # print(str1 + "\t" + str2)
                hamDist=hamming_distance(str1,str2)
                if 0 < hamDist <= int(hamming_distance_maximum):
                    newRow = {'First index string':str1, 'Second index string':str2, 'Hamming Distance':hamDist}
                    hamDistList = hamDistList.append(newRow, ignore_index=True)
                elif hamDist == 0:
                	newRow = {'First index string':str1, 'Second index string':str2, 'Hamming Distance':"Barcode Collision!"}
                	hamDistList = hamDistList.append(newRow, ignore_index=True)
    pd.set_option('precision',0)
    if len(hamDistList) == 0:
        print()
        print("No indexes found with hamming distance of %s or less in %s" % (hamming_distance_maximum, sample_sheet_file))
    else:
        hamDistListStyled = hamDistList.style.set_properties(**{'text-align': 'left'})
        hamDistListStyled.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
        hamDistList = hamDistList.to_string(index = False)
        print()
        print(hamDistList)
    return hamDistList

if __name__ == "__main__":
    main()
