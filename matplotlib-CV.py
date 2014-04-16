#!/usr/bin/env python
import matplotlib.pyplot
import csv

voltage_list = []
current_list = []
with open("V-I.csv") as csvfile:
    rows = csv.reader(csvfile, delimiter='\t')
    for row in rows:
        number_of_rows_to_skip = 1
        if rows.line_num <= number_of_rows_to_skip: 
            continue # skip headers

        i = rows.line_num - number_of_rows_to_skip # datapoint index to be added
        n = i - 1 # nominal number of datapoints
        assert n == len(voltage_list)
        assert n == len(current_list)

        voltage = float(row[0])
        current = float(row[1])

        if n > 2:
            voltage_previous = voltage_list[-1]

            dV = voltage_previous  - voltage
            dV_previous = voltage_list[-2] - voltage_previous 

            # If dV and dV_previous have different signs, we've detected a beginning or end of a cycle
            # TODO: implement debouncing
            if dV*dV_previous < 0:
                print "Sign reversal in voltage detected at line", rows.line_num
                print "dV =", dV
                print "dV_previous =", dV_previous

        voltage_list.append(voltage)
        current_list.append(current)


matplotlib.pyplot.plot(voltage_list, current_list)
matplotlib.pyplot.show()
