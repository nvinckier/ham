#!/bin/python

import sys
import getopt
import os

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

def print_colors():
    print(bcolors.TEAL + "This is the TEAL color/style." + bcolors.ENDC)
    print(bcolors.PURPLE + "This is the PURPLE color/style." + bcolors.ENDC)
    print(bcolors.BLUE + "This is the BLUE color/style." + bcolors.ENDC)
    print(bcolors.YELLOW + "This is the YELLOW color/style." + bcolors.ENDC)
    print(bcolors.GREEN + "This is the GREEN color/style." + bcolors.ENDC)
    print(bcolors.RED + "This is the RED color/style." + bcolors.ENDC)
    print(bcolors.UNDERLINE + "This is the UNDERLINE color/style." + bcolors.ENDC)
    print(bcolors.ITALIC + "This is the ITALIC color/style." + bcolors.ENDC)
    print(bcolors.BOLD + "This is the BOLD color/style." + bcolors.ENDC)
    print(bcolors.ENDC + "This is the ENDC color/style." + bcolors.ENDC)
    return

# Uncomment to check colors in terminal
# print_colors()

# process_args - Process command line arguments and update globals variables.
def process_args():
    global sample_sheet_file, hamming_distance_maximum, demux_program

    if len(sys.argv) <= 1:
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:hi:p:", ["distance=", "help", "input=", "program="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(1)
    sample_sheet_file = None
    hamming_distance_maximum = 3
    demux_program = 0

    for o, a in opts:
        if o in ("-d", "--distance"):
            hamming_distance_maximum = int(a)
        elif o in ("-h", "--help"):
            usage()
        elif o in ("-i", "--input"):
            sample_sheet_file = a
        elif o in ("-p", "--program"):
            demux_program = int(a)

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
    print("Usage:")
    print("  hamming_distance_calculcator.py [Options] -i <SampleSheet CSV File>")
    print("")
    print("Options:")
    print("  -d, --distance INT                  Set maximum hamming distance to show in report to INT (default: 3)")
    print("  -h, --help                          Display this help message")
    print("  -i, --input <path/to/SampleSheet>   Sample sheet expected in standard CSV format with [Data] or [BCLConvert_Data] section")
    print("  -p, --program NUM                   Demultiplexing program to be used (default: BCL Convert). Possible options:")
    print("                                        1) BCL Convert")
    print("                                        2) bcl2fastq")
    print("")
    sys.exit(1)

# Remove any blank lines in sample sheet to avoid throwing errors
def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def open_SS(file):
    global v1detected, v2detected, index1List, index2List, indexList, dualIndexed
    with open(file, 'rt') as ss_data_raw:
        # for rawLine in inputData:
        #     print(rawLine)
        newSheet = []
        num = 0
        header = []
        indexes = []
        v1detected = False
        v2detected = False
        index1List = []
        index2List = []
        indexList = []
        dualIndexed = False
        for line in nonblank_lines(ss_data_raw):
            newSheet+=[line.split(',')]
        for num in range(0, len(newSheet)):
            newLine=newSheet[num]
            if "[Data]" in newLine:
                v1detected = True
                header=newSheet[num+1]
                indexes=newSheet[num+2:]
            elif "[BCLConvert_Data]" in newLine:
                v2detected = True
                header=newSheet[num+1]
                indexes=newSheet[num+2:]
            num+=1
        if header == []:
            print("No [Data] or [BCLConvert_Data] section found! Please check sample sheet for errors.")
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
                    dualIndexed = True
                    index1List.append(indexes[sampleNum][index1])
                    index2List.append(indexes[sampleNum][index2])
                    sampleIndex = indexes[sampleNum][index1] + '+' +  indexes[sampleNum][index2]
                else:
                    index1List.append(indexes[sampleNum][index1])
                    sampleIndex = indexes[sampleNum][index1]
                indexList.append(sampleIndex)
    return v2detected, index1List, index2List, indexList, dualIndexed

# Hamming distance calculation function
def hamming_distance(string1, string2):
    # Start with a distance of zero, and count up
    distance = 0
    # Loop over the indices of the string
    if len(string1) >= len(string2):
        L = len(string1)
    else:
        L= len(string2)
    for i in range(L):
        if string1[i] != string2[i]:
            distance += 1
    # Return the final count of differences
    return distance

def get_hamming_distance(inputList):
    global hamDist, results, hamDistValues
    hamDist = 0
    results = ""
    resultsHeader = ""
    headerCol3 = 'Hamming Distance'
    headerCol4 = 'Comment'
    hamDistValues = []
    while len(inputList) > 0:
        if inputList == index1List:
            print("")
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
                    newRow = (bcolors.RED + str1 + '\t' + str2 + '\t' + str(hamDist) + (" " * (len(str(headerCol3)) - len(str(hamDist)))) + '\t' +  'Barcode Collision!' + bcolors.ENDC + '\n')
                    results+=newRow
                    hamDistValues.append(0)
                elif 0 < hamDist <= 2:
                    newRow = (bcolors.YELLOW + str1 + '\t' + str2 + '\t' + str(hamDist) + (" " * (len(str(headerCol3)) - len(str(hamDist)))) + '\t' + '0 mismatches allowed for this index/index combination during demultiplexing.' + bcolors.ENDC + '\n')
                    results+=newRow
                    hamDistValues.append(hamDist)
                elif 3 <= hamDist <= 4:
                    newRow = (bcolors.GREEN + str1 + '\t' + str2 + '\t' + str(hamDist) + (" " * (len(str(headerCol3)) - len(str(hamDist)))) + '\t' + '1 mismatch allowed for this index/index combination during demultiplexing.' + bcolors.ENDC + '\n')
                    results+=newRow
                    hamDistValues.append(hamDist)
                elif 4 < hamDist <= hamming_distance_maximum:
                    newRow = (bcolors.TEAL + str1 + '\t' + str2 + '\t' + str(hamDist) + (" " * (len(str(headerCol3)) - len(str(hamDist)))) + '\t' + '2 mismatches allowed for this index/index combination during demultiplexing.' + bcolors.ENDC + '\n')
                    results+=newRow
                    hamDistValues.append(hamDist)
    if any(val <= hamming_distance_maximum for val in hamDistValues):
        print(results)
    else:
        print('All hamming distances calculated are greater than ' + str(hamming_distance_maximum))
    return hamDist, results, hamDistValues

def bcl_convert_mismatch_settings(inputList):
    global barcodeMismatchIndex1Settings, barcodeMismatchIndex2Settings
    settingsNotice1=('The following sample sheet setting ' + bcolors.ITALIC + 'must' + bcolors.ENDC + ' be used with BCL Convert for this index/index combination:')
    settingsNotice2=('The following sample sheet setting can be used with BCL Convert for this index/index combination:')
    settingsHeader='[BCLConvert_Settings]'
    settingsDisclaimer=('\n' + bcolors.ITALIC + bcolors.RED + 'Note: this is one possibility and is not necessarily recommended.' + bcolors.ENDC)
    settingsMessage=""
    if inputList == index1List:
        get_hamming_distance(inputList)
        if any(val == 0 for val in hamDistValues):
            i7collision = True
            barcodeMismatchIndex1Settings='BarcodeMismatchIndex1,0'
            settingsMessage=(settingsNotice1 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex1Settings)
        elif any(val < 5 for val in hamDistValues):
            barcodeMismatchIndex1Settings='BarcodeMismatchIndex1,1'
            settingsMessage=(settingsNotice2 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex1Settings)
        elif all(val > 4 for val in hamDistValues):
            barcodeMismatchIndex1Settings='BarcodeMismatchIndex1,2'
            settingsMessage=(settingsNotice2 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex1Settings)
    elif inputList == index2List:
        get_hamming_distance(inputList)
        if any(val == 0 for val in hamDistValues):
            barcodeMismatchIndex2Settings='BarcodeMismatchIndex2,0'
            settingsMessage=(settingsNotice1 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex2Settings)
        elif any(val < 5 for val in hamDistValues):
            barcodeMismatchIndex2Settings='BarcodeMismatchIndex2,1'
            settingsMessage=(settingsNotice2 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex2Settings + '\n' + settingsDisclaimer)
        elif all(val > 4 for val in hamDistValues):
            barcodeMismatchIndex2Settings='BarcodeMismatchIndex2,2'
            settingsMessage=(settingsNotice2 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex2Settings + '\n' + settingsDisclaimer)
    elif inputList == indexList:
        get_hamming_distance(inputList)
        if barcodeMismatchIndex1Settings == 'BarcodeMismatchIndex1,0' and barcodeMismatchIndex2Settings == 'BarcodeMismatchIndex2,0':
            settingsMessage=(settingsNotice1 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex1Settings + '\n' + barcodeMismatchIndex2Settings)
        elif barcodeMismatchIndex1Settings == 'BarcodeMismatchIndex1,1' or barcodeMismatchIndex1Settings == 'BarcodeMismatchIndex1,2' or barcodeMismatchIndex2Settings == 'BarcodeMismatchIndex2,1' or barcodeMismatchIndex2Settings == 'BarcodeMismatchIndex2,2':
            settingsMessage=(settingsNotice2 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex1Settings + '\n' + barcodeMismatchIndex2Settings + '\n' + settingsDisclaimer)
    print(settingsMessage)
    print('')
    return

def bcl2fastq_mismatch_settings(inputList):
    global index1mismatchSettings, index2mismatchSettings
    settingsNotice1=('The following command-line setting ' + bcolors.ITALIC + 'must' + bcolors.ENDC + ' be used with bcl2fastq for this index/index combination:')
    settingsNotice2=('The following command-line setting can be used with bcl2fastq for this index/index combination:')
    settingsDisclaimer=('\n' + bcolors.ITALIC + bcolors.RED + 'Note: this is one possibility and is not necessarily recommended.' + bcolors.ENDC)
    settingsFail=(bcolors.RED + 'Barcode Collision! Unable to demultiplex. Please verify indexes in sample sheet are correct.' + bcolors.ENDC)
    settingsMessage=""
    if inputList == index1List:
        get_hamming_distance(inputList)
        if any(val == 0 for val in hamDistValues):
            i7collision = True
            index1mismatchSettings='collision'
        elif any(0 < val < 3 for val in hamDistValues):
            index1mismatchSettings='--mismatches 0'
            settingsMessage=(settingsNotice1 + '\n' + index1mismatchSettings)
        elif any(val < 5 for val in hamDistValues):
            index1mismatchSettings='--mismatches 1'
            settingsMessage=(settingsNotice2 + '\n' + index1mismatchSettings + '\n' + settingsDisclaimer)
        elif all(val > 4 for val in hamDistValues):
            index1mismatchSettings='--mismatches 2'
            settingsMessage=(settingsNotice2 + '\n' + index1mismatchSettings + '\n' + settingsDisclaimer)
    elif inputList == index2List:
        get_hamming_distance(inputList)
        if any(val == 0 for val in hamDistValues):
            index2mismatchSettings='collision'
        elif any(0 < val < 3 for val in hamDistValues):
            index2mismatchSettings='--mismatches 0'
            settingsMessage=(settingsNotice1 + '\n' + index2mismatchSettings)
        elif any(val < 5 for val in hamDistValues):
            index2mismatchSettings='--mismatches 1'
            settingsMessage=(settingsNotice2 + '\n' + index2mismatchSettings + '\n' + settingsDisclaimer)
        elif all(val > 4 for val in hamDistValues):
            index2mismatchSettings='--mismatches 2'
            settingsMessage=(settingsNotice2 + '\n' + index2mismatchSettings + '\n' + settingsDisclaimer)
    elif inputList == indexList:
        get_hamming_distance(inputList)
        if any(val == 0 for val in hamDistValues):
            settingsMessage=settingsFail
        elif index1mismatchSettings == 'collision' and index2mismatchSettings == 'collision':
            settingsMessage=settingsFail
        elif index1mismatchSettings == 'collision' and index2mismatchSettings == '--mismatches 0':
            settingsMessage=(settingsNotice1 + '\n' + index2mismatchSettings)
        elif index1mismatchSettings == '--mismatches 0' and index2mismatchSettings == 'collision':
            settingsMessage=(settingsNotice1 + '\n' + index1mismatchSettings)
        elif index1mismatchSettings == '--mismatches 0' and index2mismatchSettings == '--mismatches 0':
            settingsMessage=(settingsNotice1 + '\n' + index1mismatchSettings + '(' + index1mismatchSettings + index2mismatchSettings.replace('--mismatches ',',') + ' is also accepted)')
        elif index1mismatchSettings == '--mismatches 1' or index1mismatchSettings == '--mismatches 2' or index2mismatchSettings == '--mismatches 1' or index2mismatchSettings == '--mismatches 2':
            settingsMessage=(settingsNotice2 + '\n' + index1mismatchSettings + index2mismatchSettings.replace('--mismatches ',',') + '\n' + settingsDisclaimer)
    print(settingsMessage)
    print('')
    return
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
    if demux_program in (0,1):
        run_settings = bcl_convert_mismatch_settings
    elif demux_program == 2:
        run_settings = bcl2fastq_mismatch_settings
    else:
        print(str(demux_program) + ' is not a valid demultiplexing program option. Please choose 1 for BCL Convert or 2 for bcl2fastq')
        sys.exit(1)
    
    if v2detected == True:
        print(bcolors.PURPLE + "V2 sample sheet detected" + bcolors.ENDC)
    else:
        if demux_program == 0:
            run_settings = bcl2fastq_mismatch_settings
            print(bcolors.PURPLE + "V1 sample sheet detected" + bcolors.ENDC + ' (' + bcolors.ITALIC + 'Defaulting to bcl2fastq settings' + bcolors.ENDC + ')')
        else:
            print(bcolors.PURPLE + "V1 sample sheet detected" + bcolors.ENDC)

    if dualIndexed == True:
        run_settings(index1List)
        run_settings(index2List)
        run_settings(indexList)
    elif dualIndexed == False:
        run_settings(index1List)
    else:
        print('Unknown error: value for "dualIndexed" should be ' + bcolors.GREEN + '"true"' + bcolors.ENDC + ' or ' + bcolors.RED + '"false"' + bcolors.ENDC + '\n' + 'Value is instead: ' + bcolors.BLUE + dualIndexed + bcolors.ENDC)
        sys.exit(1)

if __name__ == "__main__":
    main()
