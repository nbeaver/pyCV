#!/usr/bin/env python
import matplotlib.pyplot
import csv
import sys
import os
import argparse

DEBUG = 1

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
            # TODO: avoid the reduplication between minima and maxima, i.e. make it more DRY
            if delta*delta_previous < 0:
                extrema.append(i)
                if cmp(delta, delta_previous) == -1:
                    maxima.append(i)
                    #TODO: check bounds first to avoid out-of-index errors
                    voltage_range = list[maxima[-1]] - list[minima[-1]]
                    if DEBUG:
                        print "Maximum at",i,"with value",val,"with delta_previous",delta_previous,"and delta",delta
                    if voltage_range < minimum_voltage_range:
                        if DEBUG:
                            print "False maximum detected at index",i,"with voltage range",voltage_range,"<",minimum_voltage_range
                        maxima.pop()
                        extrema.pop()
                else:
                    minima.append(i)
                    voltage_range = list[maxima[-1]] - list[minima[-1]]
                    if DEBUG:
                        print "Minima at",i,"with value",val,"with delta_previous",delta_previous,"and delta",delta
                    if voltage_range < minimum_voltage_range:
                        if DEBUG:
                            print "False minimum detected at index",i,"with voltage range",voltage_range,"<",minimum_voltage_range
                        minima.pop()
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

def saveplot(filename, title, xlabel='Cell potential versus Li [V]', ylabel='Cell current [mA]'):
    # Make room for larger text
    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})

    matplotlib.pyplot.xlabel(xlabel, fontsize=20)
    matplotlib.pyplot.ylabel(ylabel, fontsize=20)
    # TODO: make title configurable or omit it entirely
    matplotlib.pyplot.title(title, fontsize=24)
    # TODO: save the figures into a directory
    matplotlib.pyplot.savefig(filename+'.png', bbox_inches='tight')
    matplotlib.pyplot.savefig(filename+'.jpg', bbox_inches='tight')

#TODO: throw in a def main here for clarity
#TODO: parse --title argument
if len(sys.argv) < 2:
    # There should be at least the name of the script and the name of the datafile.
    print "Usage: python matplotlib-CV.py datafile.csv"
    exit(1)

parser = argparse.ArgumentParser(description='This is a script for plotting cyclic voltammetry data.')
parser.add_argument('-t', '--title', help='Plot title',required=True)
parser.add_argument('-i', '--input', help='Input file',required=True)
args = parser.parse_args()
if DEBUG:
    print "Plot title", args.title
    print "Plot input", args.input

file_path = args.input

voltage_list = []
current_list = []
with open(file_path) as csvfile:
    row_reader = csv.reader(csvfile, delimiter=',')
    try:
        for row in row_reader:
            number_of_rows_to_skip = 4
            voltage_column = 8 # start at 0, so this is column I on a spreadsheet
            current_column = 6 # start at 0, so this is column G on a spreadsheet
            if row_reader.line_num == number_of_rows_to_skip:
                assert row[current_column] == 'Cell.Current (A)'
                assert row[voltage_column] == 'Cell.Potential (V)'
            if row_reader.line_num <= number_of_rows_to_skip: 
                continue # skip headers

            voltage = float(row[voltage_column])
            current = float(row[current_column])
            if current == 0.0:
                print "Exiting early due to zero current at row #",row_reader.line_num
                break

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


cycle_intervals = zip(voltage_maximas, voltage_maximas[1:])

if DEBUG:
    print "Maximas:",voltage_maximas
    print "Cycle intervals:",cycle_intervals
    print "Cycle lengths:",[b - a for a, b in cycle_intervals]

# DONE: save each cycle as a separate image
# TODO: save images in their own folder
# DONE: change variable name "file_name" to "file_path" since it is more accurate.
folder_name = file_path + "_pyCV_plots"
# May cause race condition.
# Options:
# -- Add try/except structure.
# -- Upgrade to python 3.2 and use os.makedirs(path,exist_ok=True)
# http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary
#if not os.path.exists(folder_name):
#    os.makedir(folder_name)

file_path_no_extension = file_path.split('.')[0]
for i, interval in enumerate(cycle_intervals):
    a, b = interval
    nth_cycle = str(i + 1)
    matplotlib.pyplot.plot(voltage_list[a:b], current_list_mA[a:b])
    saveplot(file_path_no_extension + nth_cycle, args.title + " cycle #" + nth_cycle)
    matplotlib.pyplot.clf()

matplotlib.pyplot.plot(voltage_list, current_list_mA)
saveplot('all-cycles', args.title + " (all cycles)")
