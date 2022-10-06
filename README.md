# ham
Hamming distance calculator for Illumina sample sheets

                                 )\   /|
                              .-/'-|_/ |
           __            __,-' (   / \/
       .-'"  "'-..__,-'""          -o.`-._
      /                                   (")
*--._ ./      Hamming                  ___.-'
    |         Distance             _.-' 
    :         Calculator        .-/   
     \        0.2.2          )_ /
      \                _)   / \(
        `.   /-.___.---'(  /   \\ 
         (  /   \\       \(     L\ 
          \(     L\       \\ 
           \\              \\ 
            L\              L\ 

Usage:
  hamming_distance_calculcator.py [Options] -i <SampleSheet CSV File>

Options:
  -d, --distance INT                  Set maximum hamming distance to show in report to INT (default: 3)
  -h, --help                          Display this help message
  -i, --input <path/to/SampleSheet>   Sample sheet expected in standard CSV format with [Data] or [BCLConvert_Data] section
  -p, --program NUM                   Demultiplexing program to be used (default: BCL Convert). Possible options:
                                        1) BCL Convert
                                        2) bcl2fastq

