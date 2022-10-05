#!/bin/python

import sys
import getopt
import os

# Command line arguments
sample_sheet_file = None    # -i
hamming_distance_maximum = 3    # -d

# Define colors for printing to terminal
class bcolors:
    TEAL = '\033[36m'
    PURPLE = '\033[35m'
    BLUE = '\033[34m'
    YELLOW = '\033[33m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

# print(bcolors.TEAL + "This is the TEAL color/style." + bcolors.ENDC)
# print(bcolors.PURPLE + "This is the PURPLE color/style." + bcolors.ENDC)
# print(bcolors.BLUE + "This is the BLUE color/style." + bcolors.ENDC)
# print(bcolors.YELLOW + "This is the YELLOW color/style." + bcolors.ENDC)
# print(bcolors.GREEN + "This is the GREEN color/style." + bcolors.ENDC)
# print(bcolors.RED + "This is the RED color/style." + bcolors.ENDC)
# print(bcolors.UNDERLINE + "This is the UNDERLINE color/style." + bcolors.ENDC)
# print(bcolors.ITALIC + "This is the ITALIC color/style." + bcolors.ENDC)
# print(bcolors.BOLD + "This is the BOLD color/style." + bcolors.ENDC)
# print(bcolors.ENDC + "This is the ENDC color/style." + bcolors.ENDC)

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
    print("     \\        0.2.2          )_ /")
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

# Testing new sample sheet importer
def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def open_SS(file):
    global v2detected, index1List, index2List, indexList
    with open(file, 'rt') as ss_data_raw:
        # for rawLine in inputData:
        #     print(rawLine)
        newSheet = []
        num = 0
        header = []
        indexes = []
        v2detected = 'false'
        index1List = []
        index2List = []
        indexList = []
        for line in nonblank_lines(ss_data_raw):
            newSheet+=[line.split(',')]
        for num in range(0, len(newSheet)):
            newLine=newSheet[num]
            if "[Data]" in newLine:
                header=newSheet[num+1]
                # print(header)
                indexes=newSheet[num+2:]
                # print(indexes)
            elif "[BCLConvert_Data]" in newLine:
                v2detected = 'true'
                # print(num)
                header=newSheet[num+1]
                # print(header)
                indexes=newSheet[num+2:]
                # print(indexes)
            num+=1
        if header == []:
            print("No [Data] section found! Please check sample sheet for errors.")
            sys.exit(1)
        else:
            index2 = 'single-indexed'
            # print(index2)
            for col in header:
                if 'index' == col.lower().strip():
                    index1 = header.index(col)
                elif 'index2' == col.lower().strip():
                    index2 = header.index(col)
            for sampleNum in range(0,len(indexes)):
                if index2 != 'single-indexed':
                    # print(indexes[sampleNum][index1:])
                    index1List.append(indexes[sampleNum][index1])
                    index2List.append(indexes[sampleNum][index2])
                    sampleIndex = indexes[sampleNum][index1] + '+' +  indexes[sampleNum][index2]
                else:
                    index1List.append(indexes[sampleNum][index1])
                    sampleIndex = indexes[sampleNum][index1]
                indexList.append(sampleIndex)
    return index1List, index2List, indexList

# Hamming distance calculation function
def hamming_distance(string1, string2):
    # Start with a distance of zero, and count up
    distance = 0
    # Loop over the indices of the string
    L = len(string1) - 1
    for i in range(L):
        if string1[i] != string2[i]:
            distance += 1
    # Return the final count of differences
    return distance

def get_hamming_distance(inputList):
    hamDist = 0
    results = ""
    resultsHeader = ""
    headerCol3 = 'Hamming Distance'
    headerCol4 = 'Comment'
    mismatchSettings = []
    while len(inputList) > 0:
        if inputList == index1List:
            print(bcolors.BLUE + "Checking i7 index (Index 1) sequences for collisions:" + bcolors.ENDC)
            print("")
            headerCol1 = '1st i7 Index'
            headerCol2 = '2nd i7 Index'
            resultsHeader = headerCol1 + '\t' + headerCol2 + '\t' + headerCol3 + '\t' + headerCol4 + '\n'
            results += resultsHeader
        elif inputList == index2List:
            print(bcolors.BLUE + "Checking i5 index (Index 2) sequences for collisions:" + bcolors.ENDC)
            print("")
            headerCol1 = '1st i5 Index'
            headerCol2 = '2nd i5 Index'
            resultsHeader = headerCol1 + '\t' + headerCol2 + '\t' + headerCol3 + '\t' + headerCol4 + '\n'
            results += resultsHeader
        elif inputList == indexList:
            print(bcolors.BLUE + "Checking i7+i5 index (concatenation of Index 1 and Index 2) sequences for collisions:" + bcolors.ENDC)
            print("")
            headerCol1 = '1st Index Combination'
            headerCol2 = '2nd Index Combination'
            resultsHeader = headerCol1 + '\t' + headerCol2 + '\t' + headerCol3 + '\t' + headerCol4 + '\n'
            results += resultsHeader
        for num1 in range(0,len(inputList)):
            str1 = inputList.pop(0)
            str1Length = len(str1)
            for num2 in range(0,len(inputList)):
                str2 = inputList[num2]
                str2Length = len(str2)
                hamDist = hamming_distance(str1,str2)
                if hamDist == 0:
                    newRow = (bcolors.RED + str1 + '\t' + str2 + '\t' + str(hamDist) + (" " * (len(str(headerCol3)) - len(str(hamDist)))) + '\t' +  'Barcode Collision! Cannot demultiplex these samples with these indexes alone.' + bcolors.ENDC + '\n')
                    results+=newRow
                    mismatchSettings.append('cannotDemux')
                elif 0 < hamDist <= 2:
                    newRow = (bcolors.YELLOW + str1 + '\t' + str2 + '\t' + str(hamDist) + (" " * (len(str(headerCol3)) - len(str(hamDist)))) + '\t' + 'No collision detected, however barcode mismatches must be set to 0 for demultiplexing.' + bcolors.ENDC + '\n')
                    results+=newRow
                    mismatchSettings.append(0)
                elif hamDist == 3:
                    newRow = (str1 + '\t' + str2 + '\t' + str(hamDist) + (" " * (len(str(headerCol3)) - len(str(hamDist)))) + '\t' + 'No mismatches in index reads can be allowed during demultiplexing.' + bcolors.ENDC + '\n')
                    results+=newRow
                    mismatchSettings.append(hamDist)
                elif 2 < hamDist <= int(hamming_distance_maximum):
                    newRow = (str1 + '\t' + str2 + '\t' + str(hamDist) + (" " * (len(str(headerCol3)) - len(str(hamDist)))) + '\n')
                    results+=newRow
                    mismatchSettings.append(hamDist)

    print(results)
    print(mismatchSettings)
    return hamDist, results, mismatchSettings

####################################################################################################
#                                          Main function                                           #
####################################################################################################
def main():
    global sample_sheet_file, hamming_distance_maximum, v2detected
    process_args()
    # Find sample sheet on system
    print("Reporting indexes with hamming distance of " + bcolors.GREEN + "%s" % hamming_distance_maximum + bcolors.ENDC + " or less" )
    print('')
    if str(type(sample_sheet_file)) == "<class 'NoneType'>":
        sample_sheet_file = sys.argv[len(sys.argv) - 1]
        print("Sample sheet is: " + str(sample_sheet_file))
    if not os.path.exists(sample_sheet_file):
        print("ERROR: Sample sheet %s does not exist" % sample_sheet_file)
        usage()
    # Create list of indexes to compare from sample sheet
    # indexList = open_SS(sample_sheet_file)
    open_SS(sample_sheet_file)

# Need to figure out how to exit and report no indexes found with hamming distance of hamming_distance_maximum or less
    if v2detected == 'true':
        print(bcolors.ITALIC + bcolors.PURPLE + "V2 sample sheet detected" + bcolors.ENDC)
        print('')
    get_hamming_distance(index1List)
    get_hamming_distance(index2List)
    get_hamming_distance(indexList)

if __name__ == "__main__":
    main()
