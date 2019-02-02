import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime


def set_text_font(xlabels):
    plot.set_xticklabels(xlabels)
    plt.xticks(fontsize=10, rotation=40)
    plt.yticks(fontsize=10)
    plt.legend(legend, fontsize=8, loc='upper left')


def convert_str_to_date(string):
    return datetime.strptime(string, "%Y-%m-%d")


def convert_str_to_dict(string):
    string = string.split(": ")
    return int(string[0]), int(string[1])


INPUT_DIRECTORY = os.getcwd()+"\\" + "summary_stats"
OUTPUT_DIRECTORY = os.getcwd()+"\\" + "box_plot_revokded_trans"
correct_fmt_data_date = datetime(2019, 1, 23, 0, 0)
stats_directories = os.listdir(INPUT_DIRECTORY)
stats_files = os.listdir(INPUT_DIRECTORY + "\\" + stats_directories[0])
correct_file_index = stats_directories.index("2019-1-23") + 1

line_chart_data = []

if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

fig_count = 0
x = []


for file_num in range(0, len(stats_files)):
    dict_a = {}
    for i in range(0, 10):
        dict_a[i] = []

    for directory_num in range(correct_file_index, len(stats_directories)):
        num_line = 0
        f = open(INPUT_DIRECTORY + "\\" + stats_directories[directory_num] + "\\" + stats_files[file_num], 'r')
        f.readline()
        line = f.readline().replace("\n", "")
        while line:
            line = line.split(", ")
            if line[0] not in x:
                x.append(line[0])
            line = line[10:]

            for k in dict_a.keys():
                if len(dict_a[k]) > num_line:
                    dict_a[k][num_line].append(0)
                else:
                    dict_a[k].append([0])

            for item in line:
                key, value = convert_str_to_dict(item)
                if key < 10:
                    dict_a[key][num_line][directory_num - correct_file_index] = value
                else:
                    break
            line = f.readline()
            num_line += 1
    #
    legend = []

    keys = list(dict_a.keys())
    keys.sort()

    for key in keys:
        # box plot
        fig_box_plot = plt.figure(fig_count, figsize=(10, 6))
        plot = fig_box_plot.add_subplot(111)
        print(key, dict_a[key])
        bp = plot.boxplot(dict_a[key])
        legend.append("number of blocks "+str(key))
        set_text_font(x)
        fig_box_plot.savefig(OUTPUT_DIRECTORY+"\\number_of_blocks_"+str(key)+stats_files[file_num][10:-17]+".pdf", bbox_inches='tight')
        plt.close(fig_box_plot)
        fig_count += 1

    # line chart plot
    # fig_line_chart = plt.figure(fig_count, figsize=(21, 9))
    # fig_count += 1

    #break


