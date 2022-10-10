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

WARNING = (bcolors.YELLOW + "  WARNING: " + bcolors.ENDC)
ERROR = (bcolors.RED + "  ERROR: " + bcolors.ENDC)

# Uncomment to check colors in terminal
# print_colors()
# sys.exit(0)

# process_args - Process command line arguments and update globals variables.
def process_args():
    global sample_sheet_file, hamming_distance_maximum, demuxer, verbose

    if len(sys.argv) <= 1:
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:hi:p:v", ["distance=", "help", "input=", "program=", "verbose"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(1)
    sample_sheet_file = None
    hamming_distance_maximum = 3
    demuxer = 0
    verbose = False

    for o, a in opts:
        if o in ("-d", "--distance"):
            hamming_distance_maximum = int(a)
        elif o in ("-h", "--help"):
            usage()
        elif o in ("-i", "--input"):
            sample_sheet_file = a
        elif o in ("-p", "--program"):
            demuxer = int(a)
        elif o in ("-v", "--verbose"):
            verbose = True 

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
    print("  -v, --verbose                       Increase verbosity of output")
    print("")
    sys.exit(1)

# Remove any blank lines in sample sheet to avoid throwing errors
def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def open_SS(file):
    with open(file, 'rt') as ss_data_raw:
        newSheet = []
        num = 0
        header = []
        allIndexes = {}
        # Determine sample sheet version (V1 or V2) and check for single-, or dual-indexed
        V1 = False
        V2 = False
        dualIndexed = False
        i7 = []
        i5 = []
        i7_i5 = []
        for line in nonblank_lines(ss_data_raw):
            newSheet+=[line.split(',')]
        for num in range(0, len(newSheet)):
            newLine=newSheet[num]
            if "[Data]" in newLine:
                V1 = True
                header=newSheet[num+1]
                indexes=newSheet[num+2:]
            elif "[BCLConvert_Data]" in newLine:
                V2 = True
                header=newSheet[num+1]
                indexes=newSheet[num+2:]
            num+=1
        if header == []:
            print("No [Data] or [BCLConvert_Data] section found! Please check sample sheet for errors.")
            sys.exit(1)
        else:
            index2 = 'single-indexed'
            for col in header:
                if 'index' == col.lower().strip():
                    index1 = header.index(col)
                elif 'index2' == col.lower().strip():
                    index2 = header.index(col)
            for sampleNum in range(0,len(indexes)):
                if index2 != 'single-indexed':
                    dualIndexed = True
                    i7.append(indexes[sampleNum][index1])
                    i5.append(indexes[sampleNum][index2])
                    i7_i5.append(indexes[sampleNum][index1] + '+' +  indexes[sampleNum][index2])
                else:
                    i7.append(indexes[sampleNum][index1])
                allIndexes['i7'] = i7
                allIndexes['i5'] = i5
                allIndexes['i7_i5'] = i7_i5
    return allIndexes, V1, V2, dualIndexed, i7, i5, i7_i5

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
    hamDist = 0
    results = []
    hamDistValues = []
    noHamMatch = 'All hamming distances calculated are greater than '
    
    for num1 in range(0,len(inputList)):
        str1 = inputList.pop(0)
        str1Length = len(str1)
        for num2 in range(0,len(inputList)):
            str2 = inputList[num2]
            str2Length = len(str2)
            hamDist = hamming_distance(str1,str2)
            if hamDist == 0:
                newRow = (bcolors.RED + str1 + '\t' + str2 + '\t' + str(hamDist) + (" " * (16 - len(str(hamDist)))) + '\t' +  'Barcode Collision!' + bcolors.ENDC + '\n')
                # results+=newRow
                results += [(str1,str2,hamDist,(bcolors.RED + 'Barcode Collision!' + bcolors.ENDC))]
                hamDistValues.append(0)
            elif 0 < hamDist <= 2:
                newRow = (bcolors.YELLOW + str1 + '\t' + str2 + '\t' + str(hamDist) + (" " * (16 - len(str(hamDist)))) + '\t' + '0 mismatches allowed for this index/index combination during demultiplexing.' + bcolors.ENDC + '\n')
                # results+=newRow
                results += [(str1,str2,hamDist,(bcolors.YELLOW + '0 mismatches allowed for this index/index combination during demultiplexing.' + bcolors.ENDC))]
                hamDistValues.append(hamDist)
            elif 3 <= hamDist <= 4:
                newRow = (bcolors.GREEN + str1 + '\t' + str2 + '\t' + str(hamDist) + (" " * (16 - len(str(hamDist)))) + '\t' + '1 mismatch allowed for this index/index combination during demultiplexing.' + bcolors.ENDC + '\n')
                # results+=newRow
                results += [(str1,str2,hamDist,(bcolors.GREEN + '1 mismatch allowed for this index/index combination during demultiplexing.' + bcolors.ENDC))]
                hamDistValues.append(hamDist)
            elif 4 < hamDist <= hamming_distance_maximum:
                newRow = (bcolors.TEAL + str1 + '\t' + str2 + '\t' + str(hamDist) + (" " * (16 - len(str(hamDist)))) + '\t' + '2 mismatches allowed for this index/index combination during demultiplexing.' + bcolors.ENDC + '\n')
                # results+=newRow
                results += [(str1,str2,hamDist,(bcolors.TEAL + '2 mismatches allowed for this index/index combination during demultiplexing.' + bcolors.ENDC))]
                hamDistValues.append(hamDist)
            elif hamDist > hamming_distance_maximum:
                hamDistValues.append(hamDist)
    return results, hamDistValues

def bcl_convert_mismatch_settings(indexDict,dualIndexed):
    settingsNotice1 = ('The following sample sheet setting(s) ' + bcolors.ITALIC + 'must' + bcolors.ENDC + ' be used with BCL Convert for this index/index combination:')
    settingsNotice2 = ('The following sample sheet setting(s) can be used with BCL Convert for this index/index combination:')
    settingsHeader='[BCLConvert_Settings]'
    settingsDisclaimer = ('\n' + bcolors.ITALIC + bcolors.RED + 'DISCLAIMER: These are options, not recommendations. Please what is appropriate for your use case.' + bcolors.ENDC)
    settingsWarning = (bcolors.RED + 'Barcode Collision! Unable to demultiplex with these indexes alone.' + bcolors.ENDC)
    settingsFail = (bcolors.RED + 'Barcode Collision! Unable to demultiplex. Please verify indexes in sample sheet are correct.' + bcolors.ENDC)
    settingsMessage = ''
    i7collision = False
    barcodeMismatchIndex1Settings = None
    i5collision = False
    barcodeMismatchIndex2Settings = None
    results = []
    resultsHeader = []
    resultsMessage = ""
    headerCol3 = 'Hamming Distance'
    headerCol4 = 'Comment'
    noHamMatch = 'All hamming distances calculated are greater than '
    for key in indexDict.keys():
        if key == 'i7' and indexDict[key] == []:
            print(ERROR + "No i7 indexes detected")
            sys.exit(1)
        elif key == 'i7' and indexDict[key] != []:
            resultsMessage = ('\n' + bcolors.BLUE + "Checking i7 index (Index 1) sequences for collisions:" + bcolors.ENDC)
            headerCol1 = '1st i7 Index'
            headerCol2 = '2nd i7 Index'
            resultsHeader = [(headerCol1, headerCol2, headerCol3, headerCol4)]
            i7results = get_hamming_distance(indexDict[key])
            if all(val > hamming_distance_maximum for val in i7results[1]):
                results = ('\n' + noHamMatch + bcolors.UNDERLINE + bcolors.TEAL + str(hamming_distance_maximum) + bcolors.ENDC)
            else:
                results = i7results[0]
            if any(val == 0 for val in i7results[1]):
                i7collision = True
                barcodeMismatchIndex1Settings='BarcodeMismatchIndex1,0'
                settingsMessage = settingsWarning
            elif any(0 < val < 3 for val in i7results[1]):
                barcodeMismatchIndex1Settings='BarcodeMismatchIndex1,0'
                settingsMessage = (settingsNotice1 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex1Settings + '\n' + settingsDisclaimer)
            elif any(val < 5 for val in i7results[1]):
                barcodeMismatchIndex1Settings='BarcodeMismatchIndex1,1'
                settingsMessage = (settingsNotice2 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex1Settings + '\n' + settingsDisclaimer)
            elif all(val > 4 for val in i7results[1]):
                barcodeMismatchIndex1Settings='BarcodeMismatchIndex1,2'
                settingsMessage = (settingsNotice2 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex1Settings + '\n' + settingsDisclaimer)
            if dualIndexed == False or verbose == True:
                print(resultsMessage)
                print(results)
                print(settingsMessage)
        elif key == 'i5' and indexDict[key] != []:
            resultsMessage = ('\n' + bcolors.BLUE + "Checking i5 index (Index 2) sequences for collisions:" + bcolors.ENDC)
            headerCol1 = '1st i5 Index'
            headerCol2 = '2nd i5 Index'
            resultsHeader = [(headerCol1, headerCol2, headerCol3, headerCol4)]
            i5results = get_hamming_distance(indexDict[key])
            if all(val > hamming_distance_maximum for val in i5results[1]):
                results = ('\n' + noHamMatch + bcolors.UNDERLINE + bcolors.TEAL + str(hamming_distance_maximum) + bcolors.ENDC)
            else:
                results = i5results[0]
            if any(val == 0 for val in i5results[1]):
                i5collision = True
                barcodeMismatchIndex2Settings='BarcodeMismatchIndex2,0'
                settingsMessage = settingsWarning
            elif any(0 < val < 3 for val in i5results[1]):
                barcodeMismatchIndex2Settings='BarcodeMismatchIndex2,0'
                settingsMessage = (settingsNotice1 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex2Settings + '\n' + settingsDisclaimer)
            elif any(val < 5 for val in i5results[1]):
                barcodeMismatchIndex2Settings='BarcodeMismatchIndex2,1'
                settingsMessage = (settingsNotice2 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex2Settings + '\n' + settingsDisclaimer)
            elif all(val > 4 for val in i5results[1]):
                barcodeMismatchIndex2Settings='BarcodeMismatchIndex2,2'
                settingsMessage = (settingsNotice2 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex2Settings + '\n' + settingsDisclaimer)
            if verbose == True:
                print(resultsMessage)
                print(results)
                print(settingsMessage)
        elif key == 'i7_i5' and indexDict[key] != []:
            resultsMessage = ('\n' + bcolors.BLUE + "Checking i7+i5 index (concatenation of Index 1 and Index 2) sequences for collisions." + bcolors.ENDC + ' (' + bcolors.ITALIC + 'i7 and i5 sequences are assessed individually for BCL Convert' +  bcolors.ENDC + '):')
            headerCol1 = '1st Index Combination'
            headerCol2 = '2nd Index Combination'
            resultsHeader = [(headerCol1, headerCol2, headerCol3, headerCol4)]
            
            i7_i5results = get_hamming_distance(indexDict[key])
            
            if any(val == 0 for val in i7_i5results) or (i7collision == True and i5collision == True):
                settingsMessage = settingsFail
            elif barcodeMismatchIndex2Settings == None:
                settingsMessage = (settingsNotice1 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex1Settings)
            elif barcodeMismatchIndex1Settings == 'BarcodeMismatchIndex1,0' and barcodeMismatchIndex2Settings == 'BarcodeMismatchIndex2,0':
                settingsMessage = (settingsNotice1 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex1Settings + '\n' + barcodeMismatchIndex2Settings)
            elif barcodeMismatchIndex1Settings == 'BarcodeMismatchIndex1,1' or barcodeMismatchIndex1Settings == 'BarcodeMismatchIndex1,2' or barcodeMismatchIndex2Settings == 'BarcodeMismatchIndex2,1' or barcodeMismatchIndex2Settings == 'BarcodeMismatchIndex2,2':
                settingsMessage = (settingsNotice2 + '\n' + settingsHeader + '\n' + barcodeMismatchIndex1Settings + '\n' + barcodeMismatchIndex2Settings + '\n' + settingsDisclaimer)
            else:
                print(ERROR + "Unexpected BarcodeMismatch setting(s)")
                print(ERROR + "Value for Index1 barcode mismatch setting: " + barcodeMismatchIndex1Settings)
                print(ERROR + "Value for Index2 barcode mismatch setting: " + barcodeMismatchIndex2Settings)
                sys.exit(1)
            
            print(resultsMessage)
            
            if all(val > hamming_distance_maximum for val in i7_i5results[1]) and verbose == True and i7collision == False and i5collision == False:
                results = ('\n' + noHamMatch + bcolors.UNDERLINE + bcolors.TEAL + str(hamming_distance_maximum) + bcolors.ENDC + ' for all i7+i5 index combinations')
                print('1')
            elif all(val > hamming_distance_maximum for val in i7_i5results[1]) and verbose == True and (i7collision == True or i5collision == True):
                results = ('\n' + noHamMatch + bcolors.UNDERLINE + bcolors.TEAL + str(hamming_distance_maximum) + bcolors.ENDC + ' for all i7+i5 index combinations.' + '\n' + bcolors.YELLOW + '  INFO:' + bcolors.ENDC + ' Collision detected in i7 and/or i5 indexes.' + '\n' + bcolors.YELLOW + '  INFO:' + bcolors.ENDC + bcolors.ITALIC + ' Re-run with the ' + bcolors.ENDC + '-v, --verbose' + bcolors.ITALIC + ' option to see more details.' + bcolors.ENDC)
                print('2')
            elif all(val <= hamming_distance_maximum for val in i7_i5results[1]):
                results += ((i7_i5results[0]))
                print('3')
            print(resultsHeader[0], sep='\t')
            # print(len(results))
            # print(results)
            # print('\n' + settingsMessage)
    return resultsMessage, results, settingsMessage

def bcl2fastq_mismatch_settings(indexDict,dualIndexed):
    settingsNotice1 = ('The following command-line setting(s) ' + bcolors.ITALIC + 'must' + bcolors.ENDC + ' be used with bcl2fastq for this index/index combination:')
    settingsNotice2 = ('The following command-line setting(s) can be used with bcl2fastq for this index/index combination:')
    
    settingsDisclaimer = ('\n' + bcolors.ITALIC + bcolors.RED + 'DISCLAIMER: These are options, not recommendations. Please what is appropriate for your use case.' + bcolors.ENDC)
    settingsWarning = (bcolors.RED + 'Barcode Collision! Unable to demultiplex with these indexes alone.' + bcolors.ENDC)
    settingsFail = (bcolors.RED + 'Barcode Collision! Unable to demultiplex. Please verify indexes in sample sheet are correct.' + bcolors.ENDC)
    settingsMessage = ''
    i7collision = False
    index1mismatchSettings = None
    i5collision = False
    index2mismatchSettings = None
    results = ''
    resultsMessage = ''
    headerCol3 = 'Hamming Distance'
    headerCol4 = 'Comment'
    noHamMatch = 'All hamming distances calculated are greater than '
    for key in indexDict.keys():
        if key == 'i7' and indexDict[key] == []:
            print("  ERROR: No i7 indexes detected")
            sys.exit(1)
        elif key == 'i7' and indexDict[key] != []:
            resultsMessage = ('\n' + bcolors.BLUE + "Checking i7 index (Index 1) sequences for collisions:" + bcolors.ENDC)
            headerCol1 = '1st i7 Index'
            headerCol2 = '2nd i7 Index'
            results = (headerCol1 + '\t' + headerCol2 + '\t' + headerCol3 + '\t' + headerCol4 + '\n')
            i7results = get_hamming_distance(indexDict[key])
            if all(val > hamming_distance_maximum for val in i7results[1]):
                results = ('\n' + noHamMatch + bcolors.UNDERLINE + bcolors.TEAL + str(hamming_distance_maximum) + bcolors.ENDC)
            else:
                reaults = i7results[0]
            if any(val == 0 for val in i7results[1]):
                i7collision = True
                index1mismatchSettings='--mismatches 0'
                settingsMessage = settingsWarning
            elif any(0 < val < 3 for val in i7results[1]):
                index1mismatchSettings='--mismatches 0'
                settingsMessage = (settingsNotice1 + '\n' + index1mismatchSettings + '\n' + settingsDisclaimer)
            elif any(val < 5 for val in i7results[1]):
                index1mismatchSettings='--mismatches 1'
                settingsMessage = (settingsNotice2 + '\n' + index1mismatchSettings + '\n' + settingsDisclaimer)
            elif all(val > 4 for val in i7results[1]):
                index1mismatchSettings='--mismatches 2'
                settingsMessage = (settingsNotice2 + '\n' + index1mismatchSettings + '\n' + settingsDisclaimer)
            if dualIndexed == False or verbose == True:
                print(resultsMessage)
                print(results)
                print(settingsMessage)
        elif key == 'i5' and indexDict[key] != []:
            resultsMessage = ('\n' + bcolors.BLUE + "Checking i5 index (Index 2) sequences for collisions:" + bcolors.ENDC)
            headerCol1 = '1st i5 Index'
            headerCol2 = '2nd i5 Index'
            results = (headerCol1 + '\t' + headerCol2 + '\t' + headerCol3 + '\t' + headerCol4 + '\n')
            i5results = get_hamming_distance(indexDict[key])
            if all(val > hamming_distance_maximum for val in i5results[1]):
                results = ('\n' + noHamMatch + bcolors.UNDERLINE + bcolors.TEAL + str(hamming_distance_maximum) + bcolors.ENDC)
            else:
                reaults = i5results[0]
            if any(val == 0 for val in i5results[1]):
                i5collision = True
                index2mismatchSettings='--mismatches 0'
                settingsMessage = settingsWarning
            elif any(0 < val < 3 for val in i5results[1]):
                index2mismatchSettings='--mismatches 0'
                settingsMessage = (settingsNotice1 + '\n' + index2mismatchSettings + '\n' + settingsDisclaimer)
            elif any(val < 5 for val in i5results[1]):
                index2mismatchSettings='--mismatches 1'
                settingsMessage = (settingsNotice2 + '\n' + index2mismatchSettings + '\n' + settingsDisclaimer)
            elif all(val > 4 for val in i5results[1]):
                index2mismatchSettings='--mismatches 2'
                settingsMessage = (settingsNotice2 + '\n' + index2mismatchSettings + '\n' + settingsDisclaimer)
            if verbose == True:
                print(resultsMessage)
                print(results)
                print(settingsMessage)
        elif key == 'i7_i5' and indexDict[key] != []:
            resultsMessage = ('\n' + bcolors.BLUE + "Checking i7+i5 index (concatenation of Index 1 and Index 2) sequences for collisions." + bcolors.ENDC + ' (' + bcolors.ITALIC + 'i7 and i5 sequences are assessed individually for BCL Convert' +  bcolors.ENDC + '):')
            headerCol1 = '1st i7+i5 Index Combination'
            headerCol2 = '2nd i7+i5 Index Combination'
            results = (headerCol1 + '\t' + headerCol2 + '\t' + headerCol3 + '\t' + headerCol4 + '\n')
            i7_i5results = get_hamming_distance(indexDict[key])
            if any(val == 0 for val in i7_i5results) or (i7collision == True and i5collision == True):
                settingsMessage = settingsFail
            elif index2mismatchSettings == None or (index1mismatchSettings == '--mismatches 0' and index2mismatchSettings == '--mismatches 0'):
                settingsMessage = (settingsNotice1 + '\n' + index1mismatchSettings)
            elif index1mismatchSettings == '--mismatches 1' or index1mismatchSettings == '--mismatches 2' or index2mismatchSettings == '--mismatches 1' or index2mismatchSettings == '--mismatches 2':
                print("THIS ONE: 4")
                settingsMessage = (settingsNotice2 + '\n' + index1mismatchSettings + '\n' + index2mismatchSettings + '\n' + settingsDisclaimer)
            else:
                print(ERROR + "Unexpected mismatch setting(s)")
                print(ERROR + "Value for Index1 barcode mismatch setting: " + index1mismatchSettings)
                print(ERROR + "Value for Index2 barcode mismatch setting: " + index2mismatchSettings)
                sys.exit(1)
            print(resultsMessage)
            if all(val > hamming_distance_maximum for val in i7_i5results[1]) and verbose == True and i7collision == False and i5collision == False:
                results = ('\n' + noHamMatch + bcolors.UNDERLINE + bcolors.TEAL + str(hamming_distance_maximum) + bcolors.ENDC + ' for all i7+i5 index combinations')
            elif all(val <= hamming_distance_maximum for val in i7_i5results[1]):
                reaults = i7_i5results[0]
            else:
                reaults = i7_i5results[0]
                print(results)
            print('\n' + settingsMessage)
    return resultsMessage, results, settingsMessage

####################################################################################################
#                                          Main function                                           #
####################################################################################################

def main():
    global sample_sheet_file, hamming_distance_maximum, v2detected, index2mismatchSettings, barcodeMismatchIndex2Settings
    process_args()
    # Find sample sheet on system
    print("Reporting indexes with hamming distance of " + bcolors.UNDERLINE + bcolors.TEAL + "%s" % hamming_distance_maximum + bcolors.ENDC + " or less" )
    print('')
    if str(type(sample_sheet_file)) == "<class 'NoneType'>":
        sample_sheet_file = sys.argv[len(sys.argv) - 1]
        print("Sample sheet is: " + str(sample_sheet_file))
    if not os.path.exists(sample_sheet_file):
        print("ERROR: Sample sheet %s does not exist" % sample_sheet_file)
        usage()
    
    # Create list of indexes to compare from sample sheet
    SS_DATA = open_SS(sample_sheet_file)
    allIndexes = SS_DATA[0]
    V1 = SS_DATA[1]
    V2 = SS_DATA[2]
    dualIndexed = SS_DATA[3]
    i7 = SS_DATA[4]
    i5 = SS_DATA[5]
    i7_i5 = SS_DATA[6]

    # print("allIndexes: " + str(allIndexes))
    # print("V1: " + str(V1))
    # print("V2: " + str(V2))
    # print("dualIndexed: " + str(dualIndexed))
    # print("i7: " + str(i7))
    # print("i5: " + str(i5))
    # print("i7_i5: " + str(i7_i5))
    
    # Check sample sheet version and which software will be used for demultiplexing and output appropriate settings
    if V2 == True and V1 == False:
        if demuxer in (0,1):
            run_settings = bcl_convert_mismatch_settings
            print(bcolors.PURPLE + "V2 sample sheet detected" + bcolors.ENDC + ' (' + bcolors.ITALIC + 'Defaulting to BCL Convert sample sheet settings' + bcolors.ENDC + ')')
        elif demuxer == 2:
            run_settings = bcl2fastq_mismatch_settings
            print(bcolors.PURPLE + "V2 sample sheet detected" + bcolors.ENDC + ' (' + bcolors.ITALIC + 'Overriding to bcl2fastq command-line settings' + bcolors.ENDC + ')' + '\n' + 'Please update sample sheet to V1 format before using with bcl2fastq ' + bcolors.ENDC + '(e.g. [BCLConvert_Data] section should be [Data])')
    elif V1 == True and V2 == False:
        if demuxer in (0,2):
            run_settings = bcl2fastq_mismatch_settings
            print(bcolors.PURPLE + "V1 sample sheet detected" + bcolors.ENDC + ' (' + bcolors.ITALIC + 'Defaulting to bcl2fastq command-line settings' + bcolors.ENDC + ')')
        elif demuxer == 1:
            run_settings = bcl_convert_mismatch_settings
            print(bcolors.PURPLE + "V1 sample sheet detected" + bcolors.ENDC + ' (' + bcolors.ITALIC + 'Overriding to BCL Convert sample sheet settings' + bcolors.ENDC + ')' + '\n' + 'Please update sample sheet to V2 format before using with BCL Convert ' + bcolors.ENDC + '(e.g. [Data] section should be [BCLConvert_Data])')
    else:
        print('Invalid value for sample sheet version. V1 and V2 should be either True or False:' + '\n' 'V1:' + V1 + '\n' + 'V2:' + V2)
        sys.exit(1)
    
    if demuxer not in (0,1,2):
        print(str(demuxer) + ' is not a valid demultiplexing program option. Please choose 1 for BCL Convert or 2 for bcl2fastq')
        sys.exit(1)
    
    # Check hamming distances and generate settings report
    run_settings(allIndexes,dualIndexed)

if __name__ == "__main__":
    main()
