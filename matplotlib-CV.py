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
        print rows.line_num
        print row
        type(row)

        if rows.line_num == 1: 
            continue # don't include first row
        if rows.line_num == 10:
            break
        voltage.append(row[0])
        current.append(row[1])

matplotlib.pyplot.plot(voltage, current)
matplotlib.pyplot.show()
