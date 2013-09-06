# sort-csv.py
# Version 0.3
# This program will sort a csv file either to standard out or to a file.  It takes arguments
# from the command line or from a config file.  It should be able to sort on any column regardless if it
# is a number or a string.  It's a work in progress.
# - Dan Mann

from sys import argv
import argparse
import csv
import operator

# all of the var_arg variables can be set either by reading in a config file or set directly through argparse
var_arg_output_filename = None
var_arg_input_filename = None
var_arg_sort_column = None
var_arg_header = None
var_arg_wf = None

headers = None
stdout_arg = None
sortcolumn = None
parser = argparse.ArgumentParser()



# setup argparse to make -config_file and -input_file mutually exclusive
root_group = parser.add_mutually_exclusive_group()
group_config_file = root_group.add_mutually_exclusive_group()
group_config_file.add_argument('-config_file', help = "A file that contains the options 'output_file, input_file, sort_column, header, and wf.  Each option needs it's own line. Header and WF should be represented by a 1 for yes or a 0 for no.", type=str)
group_config_file.add_argument('-input_file', help = "Path to the input csv file.")
parser.add_argument("-header", action='store_true',help="Declares that the CSV has a header.")
parser.add_argument("-wf", help="Write the output to a file.", action='store_true')
parser.add_argument("-output_file", help="Path to output file.")
parser.add_argument("-sort_column", help="What column number is to be sorted.  Specify integer position of the column starting at 1.", type=int)
args = parser.parse_args()



# get options from command line or a file
try:
     if type(args.config_file) == str: # if config_file is specified then this is true - get options from file
          option_config_file = open(args.config_file, 'rb')
          var_arg_output_filename = option_config_file.readline()
          var_arg_output_filename = var_arg_output_filename.strip() #strip newline
          var_arg_input_filename = option_config_file.readline()
          var_arg_input_filename = var_arg_input_filename.strip() #strip newline
          var_arg_sort_column = option_config_file.readline()
          var_arg_sort_column = int(var_arg_sort_column) # convert to int
          var_arg_header = option_config_file.readline()
          var_arg_wf = option_config_file.readline()
     
          if int(var_arg_header) == 1: # convert var_arg_header to bool
               var_arg_header = True
          else:
               var_arg_header = False

          if int(var_arg_wf) == 1: #convert var_arg_wf to bool
               var_arg_wf = True
          else:
               var_arg_wf = False
     else:
          # set the var_arg's with argparse() - get options from command line
          var_arg_output_filename = args.output_file
          var_arg_input_filename = args.input_file
          var_arg_sort_column = args.sort_column
          var_arg_header = args.header
          var_arg_wf = args.wf
except Exception,e:
     print "Had trouble reading config file.  Please check path and formatting of the file."
     print "Error: %s" % (str(e))
     quit()




try:
     # test the data type to determine how we will sort (str or float)
     csv_in_file = open(var_arg_input_filename, "rb")
     csv_data_test = csv.reader(csv_in_file, quoting=csv.QUOTE_NONNUMERIC)
     next(csv_data_test) # ignore the first line, it might be a header
     for row in csv_data_test:
          sort_type = type(row[var_arg_sort_column-1])
          break
except Exception,e:
     print "CSV file cannot test the header.  Please check the command."
     print "Error: %s" % (str(e))
     quit()



csvdatatest = None
csv_in_file.close() # we've run our test, set the object to None and close the file.




# writing to a file and writing to stdout don't handle quotes the same way, adjust the way the
# csv module reads the file based on how we plan to do the output
try:
     csv_in_file = open(var_arg_input_filename, "rb")
     if var_arg_wf:
          csvdata = csv.reader(csv_in_file) # writing to a file
     else:
          csvdata = csv.reader(csv_in_file, quoting=csv.QUOTE_NONE) #writing to stdout

except Exception,e:
     print "CSV file cannot be opened.  Please check the command."
     print "Error: %s" % (str(e))
     quit()




# If there is a header indicated in the script argument, seperate it out now
if var_arg_header:
    for row in csvdata:
         headers = row
         break



# sort the data
if sort_type != str:
     # lambda t: tell sorted what data type it's sorting
     sortedcsv = sorted(csvdata,key = lambda t: float( t[var_arg_sort_column-1]))
else:
     sortedcsv = sorted(csvdata, key = operator.itemgetter(var_arg_sort_column-1))



# loop and print the data to stdout
try:
     if var_arg_wf:
          csv_out_file = open(var_arg_output_filename, 'wb') # write the output to a file
          writer = csv.writer(csv_out_file, quoting=csv.QUOTE_NONNUMERIC)
          if var_arg_header:
               writer.writerow(headers)
               for listdata in sortedcsv:
                    writer.writerow(listdata)
               csv_out_file.close()
     else:
          if var_arg_header:
               print ','.join(headers)
               for listdata in sortedcsv:
                    print ','.join(map(str,listdata))
except Exception,e:
     print "There may have been a problem writing to the output file.  Please check the command."
     print "Error: %s" % (str(e))
     quit()


csv_in_file.close()
