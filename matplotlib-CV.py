#!/usr/bin/env python
import matplotlib.pyplot
import csv
import sys

DEBUG = 0

def get_local_extrema(list):
    # Local extrema includes beginning of range 
    extrema = [0]
    maxima = [0]
    minima = [0]
    # To avoid counting tiny jitters as a cycle,
    # we need a minimum voltage range.
    minimum_voltage_range = 0.1 # volts
    for i, val in enumerate(list):
        if i > 2:
            delta =          list[i - 0] - list[i - 1]
            delta_previous = list[i - 1] - list[i - 2]

            # If delta and delta_previous have different signs, we've detected a beginning or end of a cycle
            # DONE: implement debouncing
            # TODO: avoid the reduplication between minima and maxima
            if delta*delta_previous < 0:
                extrema.append(i)
                if cmp(delta, delta_previous) == -1:
                    maxima.append(i)
                    voltage_range = list[maxima[-1]] - list[minima[-1]]
                    if DEBUG:
                        print "Maximum at",i,"with value",val,"with delta_previous",delta_previous,"and delta",delta
                    if voltage_range < minimum_voltage_range:
                        if DEBUG:
                            print "False maximum detected at index",i,"with voltage range",voltage_range
                        maxima.pop()
                        extrema.pop()
                else:
                    minima.append(i)
                    voltage_range = list[maxima[-1]] - list[minima[-1]]
                    if DEBUG:
                        print "Minima at",i,"with value",val,"with delta_previous",delta_previous,"and delta",delta
                    if voltage_range < minimum_voltage_range:
                        if DEBUG:
                            print "False minimum detected at index",i,"with voltage range",voltage_range
                        maxima.pop()
                        extrema.pop()
        else:
            # We've only seen two values, so we can't tell if there's been any extrema
            pass
    # Local extrema includes end of range
    end = len(list) - 1
    extrema.append(end)
    minima.append(end)
    maxima.append(end)
    return extrema, minima, maxima

def saveplot(filename):
    # Make room for larger text
    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})

    matplotlib.pyplot.xlabel('Cell potential versus Li [V]', fontsize=20)
    matplotlib.pyplot.ylabel('Cell current [mA]', fontsize=20)
    matplotlib.pyplot.title('Mesoporous carbon', fontsize=24)
    matplotlib.pyplot.savefig(filename+'.png', bbox_inches='tight')
    matplotlib.pyplot.savefig(filename+'.jpg', bbox_inches='tight')

# TODO: be a little more thorough about checking the arguments
# TODO: choose which scans to overplot on same graph
if len(sys.argv) < 2:
    # There should be at least the name of the script and the name of the datafile.
    print "Usage: python matplotlib-CV.py datafile.csv"
    exit(1)

file_name = sys.argv[1]

#DONE: make the opened file configurable from commandline
#DONE: parse EZStat potentiostat data instead of the simpler CSV file
voltage_list = []
current_list = []
with open(file_name) as csvfile:
    row_reader = csv.reader(csvfile, delimiter=',')
    try:
        for row in row_reader:
            number_of_rows_to_skip = 4
            voltage_column = 8 # start at 0
            current_column = 6 # start at 0
            if row_reader.line_num == number_of_rows_to_skip:
                assert row[current_column] == 'Cell.Current (A)'
                assert row[voltage_column] == 'Cell.Potential (V)'
            if row_reader.line_num <= number_of_rows_to_skip: 
                continue # skip headers

            voltage = float(row[voltage_column])
            current = float(row[current_column])

            voltage_list.append(voltage)
            current_list.append(current)

            n = row_reader.line_num - number_of_rows_to_skip # nominal number of datapoints
            assert n == len(voltage_list)
            assert n == len(current_list)
    # Have to do this, since aborting a scan leaves a bunch of ASCII NUL characters.
    except csv.Error, error:
        print "Warning: ignored error:",error
        print "(EZStat CSV files contain ASCII NUL characters if the scan has been aborted.)"
        pass

A_to_mA = 1000 # 1000 milliamps per amp
current_list_mA = [A_to_mA*current for current in current_list]

_, _, voltage_maximas = get_local_extrema(voltage_list)

cycle_intervals = zip(voltage_maximas[::2], voltage_maximas[1::2])

if DEBUG:
    print "Cycle intervals:",cycle_intervals
    print "Cycle lengths:",[b - a for a, b in cycle_intervals]

#TODO: save each cycle as a separate image
file_name_no_extension = file_name.split('.')[0]
for i, interval in enumerate(cycle_intervals):
    a, b = interval
    matplotlib.pyplot.plot(voltage_list[a:b], current_list_mA[a:b])
    saveplot(file_name_no_extension + str(i))
    matplotlib.pyplot.clf()

matplotlib.pyplot.plot(voltage_list, current_list_mA)
saveplot('all-cycles')
