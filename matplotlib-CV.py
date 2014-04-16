#!/usr/bin/env python
import matplotlib.pyplot
import csv

def get_extrema(list):
    extrema = []
    maxima = []
    minima = []
    for i, val in enumerate(list):
        if i > 2:
            delta =          list[i - 0] - list[i - 1]
            delta_previous = list[i - 1] - list[i - 2]

            # If delta and delta_previous have different signs, we've detected a beginning or end of a cycle
            # TODO: implement debouncing
            if delta*delta_previous < 0:
                extrema.append(i)
                if cmp(delta, delta_previous) == -1:
                    maxima.append(i)
                else:
                    minima.append(i)
        else:
            pass
    return extrema, minima, maxima

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

A_to_mA = 1000 # 1000 milliamps per amp
current_list_mA = [A_to_mA*current for current in current_list]

_, _, voltage_maximas  = get_extrema(voltage_list)

matplotlib.pyplot.plot(voltage_list, current_list_mA)

def saveplot(filename):
    # Make room for larger text
    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})

    matplotlib.pyplot.xlabel('Cell potential versus Li [V]', fontsize=20)
    matplotlib.pyplot.ylabel('Cell current [mA]', fontsize=20)
    matplotlib.pyplot.title('Mesoporous carbon', fontsize=24)
    matplotlib.pyplot.savefig(filename+'.png', bbox_inches='tight')
    matplotlib.pyplot.savefig(filename+'.jpg', bbox_inches='tight')

saveplot('all-cycles')
