import csv
import sys

print('2015/2016 Season')
f = open('15-16.csv', 'rt')
try:
    reader = csv.reader(f)
    for row in reader:
        print (row[2], row[4], row[3], row[5], row[6])
finally:
    f.close()
    

print('2014/2015 Season')
f = open('14-15.csv', 'rt')
try:
    reader = csv.reader(f)
    for row in reader:
        print (row[2], row[4], row[3], row[5], row[6])
finally:
    f.close()