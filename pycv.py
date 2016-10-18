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
    minimum_voltage_range = 1.0 # volts
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

def save_plot(basename, title, xlabel='Cell potential versus Li [V]', ylabel='Cell current [mA]'):
    # Make room for larger text
    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})

    matplotlib.pyplot.xlabel(xlabel, fontsize=20)
    matplotlib.pyplot.ylabel(ylabel, fontsize=20)
    # TODO: make title configurable or omit it entirely
    matplotlib.pyplot.title(title, fontsize=24)
    # TODO: save the figures into a directory
    matplotlib.pyplot.savefig(basename+'.png', bbox_inches='tight')
    matplotlib.pyplot.savefig(basename+'.jpg', bbox_inches='tight')

def save_csv(basename, line_list):
    # Save csv files for e.g. gnuplot
    with open(basename + ".txt", 'wb') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=' ', quoting=csv.QUOTE_NONE)
        for line in line_list:
            csv_writer.writerow(line)

#TODO: throw in a def main here for clarity and to separate out the future charge-discharge curves.
#DONE: parse --title argument

parser = argparse.ArgumentParser(description='This is a script for plotting cyclic voltammetry data.')
parser.add_argument('-t', '--title', help='Plot title',required=True)
parser.add_argument('-i', '--input', help='Input file',required=True)
args = parser.parse_args()
if DEBUG:
    print "Plot title", repr(args.title)
    print "Plot input", repr(args.input)

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
            seconds_column = 3 # start at 0, so this is column D on a spreadsheet
            step_num_column = 1 # start at 0, so this is column B on a spreadsheet
            if row_reader.line_num == number_of_rows_to_skip:
                assert row[current_column] == 'Cell.Current (A)'
                assert row[voltage_column] == 'Cell.Potential (V)'
                assert row[seconds_column] == 'Time [=] sec'
                assert row[step_num_column] == 'Step #'
            if row_reader.line_num <= number_of_rows_to_skip: 
                continue # skip headers

            voltage = float(row[voltage_column])
            current = float(row[current_column])
            seconds = float(row[seconds_column])
            step_num = int(row[step_num_column])
            if current == 0.0 and step_num != 1: # Usually start at OCV, so no current initially.
                print "Warning: Exiting early due to zero current at row #",row_reader.line_num
                break

            voltage_list.append(voltage)
            current_list.append(current)

            n = row_reader.line_num - number_of_rows_to_skip # nominal number of datapoints
            assert n == len(voltage_list)
            assert n == len(current_list)
    # Have to do this, since aborting a scan leaves a bunch of ASCII NUL characters.
    except csv.Error, error:
        print "Warning: ignored error:",error
        print "(EZStat CSV files will crash the python csv parser if the recipe was aborted.)"
        # End of successful file: ^@^@^@^ORecipe finished
        # End of aborted file: ^@^@^@^NRecipe aborted
        pass

A_to_mA = 1000 # 1000 milliamps per amp
current_list_mA = [A_to_mA*current for current in current_list]

_, _, voltage_maximas = get_local_extrema(voltage_list)


cycle_intervals = zip(voltage_maximas, voltage_maximas[1:])

if DEBUG:
    print "Maximas:",voltage_maximas
    print "Cycle intervals:",cycle_intervals
    print "Cycle lengths:",[b - a for a, b in cycle_intervals]

# TODO: write individual csv files for each plot
# DONE: save each cycle as a separate image
# TODO: save images in their own folder
# DONE: change variable name "file_name" to "file_path" since it is more accurate.

file_path_no_extension = os.path.splitext(file_path)[0]
basename_no_extension = os.path.splitext(os.path.basename(file_path))[0]
folder_name = file_path_no_extension + "_pyCV_plots"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)
# TODO: May cause race condition.
# Options:
# -- Add try/except structure.
# -- Upgrade to python 3.2 and use os.makedirs(path,exist_ok=True)
# http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary
full_basename = os.path.join(folder_name, basename_no_extension)

for i, interval in enumerate(cycle_intervals):
    nth_cycle = str(i + 1)
    a, b = interval
    matplotlib.pyplot.plot(voltage_list[a:b], current_list_mA[a:b])
    save_plot(full_basename + "_" + nth_cycle, args.title + " cycle #" + nth_cycle)
    save_csv(full_basename + "_" + nth_cycle, [("V","I")]+zip(voltage_list[a:b], current_list_mA[a:b]))
    matplotlib.pyplot.clf()

matplotlib.pyplot.plot(voltage_list, current_list_mA)
save_plot(full_basename + '_all-cycles', args.title + " (all cycles)")
