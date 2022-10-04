#!/home/nvinckier/anaconda3/bin/python

import sys
import getopt
import os

# Command line arguments
sample_sheet_file = None    # -i
hamming_distance_maximum = 3    # -d

# Define colors for printing to terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'
# print(bcolors.HEADER + "This is the text color for HEADER" + bcolors.ENDC)
# print(bcolors.OKBLUE + "This is the text color for OKBLUE" + bcolors.ENDC)
# print(bcolors.OKGREEN + "This is the text color for OKGREEN" + bcolors.ENDC)
# print(bcolors.WARNING + "This is the text color for WARNING" + bcolors.ENDC)
# print(bcolors.FAIL + "This is the text color for FAIL" + bcolors.ENDC)
# print(bcolors.BOLD + "This is the text color for BOLD" + bcolors.ENDC)
# print(bcolors.UNDERLINE + "This is the text color for UNDERLINE" + bcolors.ENDC)

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
    print("     \\        0.2.1          )_ /")
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
                    # print(index1)
                elif 'index2' == col.lower().strip():
                    index2 = header.index(col)
                    # print(index2)
            for sampleNum in range(0,len(indexes)-1):
                if index2 != 'single-indexed':
                    # print(sampleNum)
                    # print(indexes[sampleNum][index1:])
                    index1List.append(indexes[sampleNum][index1])
                    index2List.append(indexes[sampleNum][index2])
                    sampleIndex = indexes[sampleNum][index1] + '+' +  indexes[sampleNum][index2]
                    # print(indexes[sampleNum][0] + '+' + indexes[sampleNum])
                    # print(sampleIndex)
                else:
                    index1List.append(indexes[sampleNum][index1])
                    sampleIndex = indexes[sampleNum][index1]
                indexList.append(sampleIndex)
            # print(index1List)
            # print(index2List)
            # print(indexList)
    return index1List, index2List, indexList

# Hamming distance calculation function
def hamming_distance(string1, string2):
    # Start with a distance of zero, and count up
    distance = 0
    # Loop over the indices of the string
    L = len(string1) - 1
    for i in range(L):
        # Add 1 to the distance if these two characters are not equal
        # print(i)
        # print(string1)
        # print(string2)
        if string1[i] != string2[i]:
            distance += 1
    # Return the final count of differences
    return distance

def get_hamming_distance(inputList):
    global hamDist, str1, str2 
    while len(inputList) > 1:
        for num1 in range(0,len(inputList)):
            str1 = inputList.pop(0)
            for num2 in range(0,len(inputList)):
                str2 = inputList[num2]
                hamDist = hamming_distance(str1,str2)
                if hamDist == 0:
                    newRow = (bcolors.FAIL + str1 + '\t' + str2 + '\t' + str(hamDist) + '\t' +  'Barcode Collision! Cannot demultiplex these samples.' + bcolors.ENDC)
                    print(newRow)
                elif 0 < hamDist <= 2:
                    newRow = (bcolors.WARNING + str1 + '\t' + str2 + '\t' + str(hamDist) + '\t' + 'No mismatches in index reads can be allowed during demultiplexing.' + bcolors.ENDC)
                    print(newRow)
                elif 2 < hamDist <= int(hamming_distance_maximum):
                    newRow = (str1 + '\t' + str2 + '\t' + str(hamDist))
                    print(newRow)
    return hamDist

####################################################################################################
#                                          Main function                                           #
####################################################################################################
def main():
    global sample_sheet_file, hamming_distance_maximum, v2detected
    hamDist = 0
    process_args()
    # Find sample sheet on system
    print("Reporting indexes with hamming distance of %s or less" % hamming_distance_maximum)
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
        print("V2 sample sheet detected")
        print('')
        print('1st Index' + '\t' + '2nd Index' + '\t' + 'Hamming Distance'+ '\t' + 'Comment')
        for currentList in [index1List, index2List, indexList]:
            # print(currentList)
            get_hamming_distance(currentList)
    else:
        print('')
        print('1st Index' + '\t' + '2nd Index' + '\t' + 'Hamming Distance'+ '\t' + 'Comment')
        get_hamming_distance(indexList)
if __name__ == "__main__":
    main()
