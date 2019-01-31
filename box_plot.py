import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os


def set_text_font(xlabels):
    plot.set_xticklabels(xlabels)
    plt.xticks(fontsize=6, rotation=40)
    plt.yticks(fontsize=6)
    #plt.legend(legend, fontsize=8, loc='upper left')


INPUT_DIRECTORY = os.getcwd()+"\\" + "summary_stats"
OUTPUT_DIRECTORY = os.getcwd()+"\\" + "box_plot"
summarised_stats_files = ["latest_block_timestamp", "convergence_speed", "num_of_blockchain",
                          "length_of_blockchain", "block_index_with_transaction",
                          "max_num_of_block", "avg_num_of_block"]
x = []
data = []

stats_directories = os.listdir(INPUT_DIRECTORY)
stats_files = os.listdir(INPUT_DIRECTORY + "\\" + stats_directories[0])

for file_num in range(0, len(stats_files)):
    data.append([])
    DATA_FILLED = False
    for directory in stats_directories:
        num_line = 0

        f = open(INPUT_DIRECTORY + "\\" + directory + "\\" + stats_files[file_num], 'r')
        f.readline()
        line = f.readline()

        while line:
            line = line.split(", ")
            if not DATA_FILLED:
                if line[0] not in x:
                    x.append(line.pop(0))
                else:
                    del line[0]
                data[file_num].append([])
                for index in range(0, 9):
                    if index != 4 and index != 7:
                        if line[index] == 'None':
                            line[index] = 0
                        data[file_num][-1].append([float(line[index])])

            else:
                del line[0]
                temp_index = 0
                for index in range(0, 9):
                    if index != 4 and index != 7:
                        if line[index] == 'None':
                            line[index] = 0
                        data[file_num][num_line][temp_index].append(float(line[index]))
                        temp_index += 1
            num_line += 1
            line = f.readline()
        if not DATA_FILLED:
            DATA_FILLED = True


for index in range(len(summarised_stats_files)):
    attribute_data = []
    for file_num in range(len(data)):
        attribute_data.append([])
        for contact_freq in range(len(x)):
            attribute_data[file_num].append(data[file_num][contact_freq][index])

    for num in range(0, 3):
        fig = plt.figure(num, figsize=(6, 3))
        plot = fig.add_subplot(111)
        #for num2 in range(num, len(stats_files), 3):
        classified_data = attribute_data[0]
        bp = plot.boxplot(classified_data)
        set_text_font(x)
        plt.show()
        break
    break

print(len(attribute_data))