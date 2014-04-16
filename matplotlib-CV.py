#!/usr/bin/env python
import matplotlib.pyplot
import csv

def detect_reversals(list):
    reversal_indices = []
    for i, val in enumerate(list):
        if i > 2:
            delta =          list[i - 0] - list[i - 1]
            delta_previous = list[i - 1] - list[i - 2]

            # If delta and delta_previous have different signs, we've detected a beginning or end of a cycle
            # TODO: implement debouncing
            if delta*delta_previous < 0:
                reversal_indices.append(i)
                print "Sign reversal in voltage detected at line", i
                print "V = ", val
                print "dV =", delta
                print "dV_previous =", delta_previous
        else:
            pass
    return reversal_indices

voltage_list = []
current_list = []
with open("V-I.csv") as csvfile:
    rows = csv.reader(csvfile, delimiter='\t')
    for row in rows:
        number_of_rows_to_skip = 1
        if rows.line_num <= number_of_rows_to_skip: 
            continue # skip headers

        voltage = float(row[0])
        current = float(row[1])

        voltage_list.append(voltage)
        current_list.append(current)

        n = rows.line_num - number_of_rows_to_skip # nominal number of datapoints
        assert n == len(voltage_list)
        assert n == len(current_list)

detect_reversals(voltage_list)

matplotlib.pyplot.plot(voltage_list, current_list)
matplotlib.pyplot.show()
