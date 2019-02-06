import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os


def set_text_font(plot, xlabels, legend = None):
    plot.set_xticklabels(xlabels)
    plt.xticks(fontsize=10, rotation=40)
    plt.yticks(fontsize=10)
    if legend:
        plt.legend(legend, fontsize=8, loc='upper left')


def set_y_label(num):
    if num == 0:
        return "Latest block timestamp(s)"
    elif num == 1:
        return "Convergence speed(s)"
    elif num == 2:
        return "Number of blockchain"
    elif num == 3:
        return "Length of blockchain"
    elif num == 4:
        return "Index number of latest block with transaction"
    elif num == 5:
        return "Maximum number of blocks after revoked transaction"
    elif num == 6:
        return "Average number of blocks after revoked transactions"
    
def render_box_plot():
    global fig_count

    OUTPUT_DIRECTORY = os.getcwd()+"\\" + "box_plot"
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    for index in range(len(summarised_stats_files)):
        attribute_data = []
        for file_num in range(len(data)):
            attribute_data.append([])
            for contact_freq in range(len(x)):
                attribute_data[file_num].append(data[file_num][contact_freq][index])

        for file_num in range(0, len(stats_files)):
            fig = plt.figure(fig_count+file_num, figsize=(10, 6))
            plot = fig.add_subplot(111)
            classified_data = attribute_data[file_num]
            bp = plot.boxplot(classified_data)
            set_text_font(plot, x)
            plt.xlabel("Connection idle time range")
            plt.ylabel(set_y_label(index))
            plt.title(set_y_label(index)+stats_files[file_num][10:-4].replace("_"," "))
            fig.savefig(OUTPUT_DIRECTORY+"\\"+summarised_stats_files[index]+stats_files[file_num][10:-4]+".pdf", bbox_inches='tight')
            plt.close(fig)
        fig_count += len(stats_files)


def render_line_chart():
    global fig_count
    global summarised_stats_files
    
    OUTPUT_DIRECTORY = os.getcwd()+"\\" + "linechart_all_attributes"
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    for index in range(len(summarised_stats_files)):
        
        legend = []
        fig = plt.figure(fig_count, figsize=(10, 6))
        plot = fig.add_subplot(111)

        for file_num in range(len(data)):
            attribute_data = [] # attribute_data = [mean(all data of a attribute from different directory), next contact freq mean...]
            for contact_freq in range(len(x)):
                #print(data[file_num][contact_freq][index])
                attribute_data.append(np.mean(data[file_num][contact_freq][index]))
            #print(len(attribute_data))
            plt.plot(x, attribute_data)
            legend.append(stats_files[file_num][10:-4].replace("_", " "))
        set_text_font(plot, x, legend=legend)
        plt.xlabel("Connection idle time range")
        plt.ylabel(set_y_label(index))
        plt.title(set_y_label(index))
        fig.savefig(OUTPUT_DIRECTORY+"\\"+summarised_stats_files[index]+".pdf", bbox_inches='tight')
        plt.close(fig)
        fig_count += 1

        
INPUT_DIRECTORY = os.getcwd()  +"\\" + "heteo_summary_stats"

summarised_stats_files = ["latest_block_timestamp", "convergence_speed", "num_of_blockchain",
                          "length_of_blockchain", "block_index_with_transaction",
                          "max_num_of_block", "avg_num_of_block"]
x = []
data = [] #data[file][contact freq][attribute][directory]

stats_directories = os.listdir(INPUT_DIRECTORY)
stats_files = os.listdir(INPUT_DIRECTORY + "\\" + stats_directories[0])
print(stats_directories)
print(stats_files)

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
                        # print(file_num, num_line, temp_index, len(data), stats_files[file_num], directory)
                        data[file_num][num_line][temp_index].append(float(line[index]))
                        temp_index += 1
            num_line += 1
            line = f.readline()
        if not DATA_FILLED:
            DATA_FILLED = True

fig_count = 0
render_box_plot()
#render_line_chart()
