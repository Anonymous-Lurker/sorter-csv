from sys import argv
import csv

# unpack argv
script, filename = argv

# open the csv file
csvfile = open(filename, "rb")

# use the csv reader
csvdata = csv.reader(csvfile)

#eval the first row for sorting int and not string
csvdata = [[eval(row[0]),row[1]] for row in csvdata]

# sort the data
sortedcsv = sorted(csvdata)

# loop and print the data
for listdata in sortedcsv:
     print listdata

# close the file
csvfile.close()
