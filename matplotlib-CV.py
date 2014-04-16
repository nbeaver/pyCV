#!/usr/bin/env python
import matplotlib.pyplot
import csv

a = [1.0, 2.0, 3.0]

b = [4.0, 6.0, 7.0]

#matplotlib.pyplot.plot(a, b)
#matplotlib.pyplot.show()

voltage = []
current = []
with open("V-I.csv") as csvfile:
    rows = csv.reader(csvfile, delimiter='\t')
    for row in rows:
        if rows.line_num == 1: 
            print row
            continue # don't include the headers in the first row
        # We don't need to convert them to reals, since pyplot does this already
        voltage.append(row[0])
        current.append(row[1])

matplotlib.pyplot.plot(voltage, current)
matplotlib.pyplot.show()
