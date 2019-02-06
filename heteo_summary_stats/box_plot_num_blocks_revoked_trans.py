import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime


def set_text_font(plot, xaxislabels, legend = None):
    plot.set_xticklabels(xaxislabels)
    plt.xticks(fontsize=10, rotation=40)
    plt.yticks(fontsize=10)
    if legend:
        plt.legend(legend, fontsize=8, loc='upper left')


def convert_str_to_date(string):
    return datetime.strptime(string, "%Y-%m-%d")


def convert_str_to_dict(string):
    string = string.split(": ")
    return int(string[0]), int(string[1])


def render_box_plot_for_every_single_param():
    # Box plot for all parameters of number of blocks for revoked transaction
    global fig_count
    OUTPUT_DIRECTORY = os.getcwd()+"\\box_plot_revokded_trans\\detailed box plot\\"
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    keys = list(dict_a.keys())
    keys.sort()
    for key in keys:
        # box plot
        #print(key)
        #print(dict_a[key], len(dict_a[key][0]))
        legend = []
        fig_box_plot = plt.figure(fig_count, figsize=(10, 6))
        plot = fig_box_plot.add_subplot(111)
        # print(key, dict_a[key])
        bp = plot.boxplot(dict_a[key])
        legend.append("number of blocks " + str(key)+ " "+stats_files[file_num][11:-4].replace("_"," "))
        set_text_font(plot, x, legend=legend)
        plt.xlabel("Connection idle time range")
        plt.ylabel("Occurance times")
        plt.title("Number of roll-backed blocks "+str(key)+" for" + stats_files[file_num][10:-4].replace("_"," ") )
        fig_box_plot.savefig(OUTPUT_DIRECTORY + "number_of_blocks_" + str(key) + stats_files[file_num][10:-4] + ".pdf", bbox_inches='tight')
        plt.close(fig_box_plot)
        fig_count += 1
    for i in range(0, 10):
        print(i, len(dict_a[i]))
        dict_a[i] = []


def render_line_chart_different_block_nums():
##  Linechart for different number of blocks: 0-10
    global fig_count
    
    OUTPUT_DIRECTORY = os.getcwd()+"\\box_plot_revokded_trans\\line chart\\"
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    print(np.shape(dict_a[0]), dict_a[0]) #dict_a[0]: 0 blocks: files, contact freq
    legend = []
    keys = list(dict_a.keys())
    keys.sort()
    fig_line_chart = plt.figure(fig_count, figsize=(21, 9))
    plot = fig_line_chart.add_subplot(111)
    for key in keys:
        line_data = []
        for data_contact_freq in dict_a[key]:
            line_data.append(np.mean(data_contact_freq))
        legend.append("number of blocks: "+ str(key))
        plt.plot(x, line_data)
        set_text_font(plot, x, legend=legend)
    plt.xlabel("Connection idle time range")
    plt.ylabel("Occurance times")
    plt.title("Number of roll-backed blocks for" + stats_files[file_num][10:-4].replace("_"," ") )
    fig_line_chart.savefig(OUTPUT_DIRECTORY+"\\linechart_number_of_blocks"+stats_files[file_num][10:-4]+".pdf", bbox_inches='tight')
    plt.close(fig_line_chart)
    fig_count += 1
    for i in range(0, 10):
        print(i, len(dict_a[i]))
        dict_a[i] = []


def render_line_chart_different_hetero_contact_freq():
    global fig_count
    global stats_directories
    global stats_files
    
    OUTPUT_DIRECTORY = os.getcwd()+"\\box_plot_revokded_trans\\line chart\\"
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    #print(np.shape(dict_a[0]), dict_a[0]) #dict_a[0]: 0 blocks: files, contact freq
    len_stats_dir = len(stats_directories) #
    keys = list(dict_a.keys())
    keys.sort()

    for key in keys:
        legend = []
        index = 0
        fig_line_chart = plt.figure(fig_count, figsize=(21, 9))
        plot = fig_line_chart.add_subplot(111)
        while index < len(dict_a[key][0]):
            line_data = []
            for data_con_freq in dict_a[key]:
                data_for_one_hetero_contact_freq = data_con_freq[index: index+len_stats_dir]
                line_data.append(np.mean(data_for_one_hetero_contact_freq))
            #print(len(data_for_one_hetero_contact_freq), index)
            #print(len(line_data))
            file_num = (index)/len_stats_dir
            file_num = int(file_num)
            legend.append(stats_files[file_num])
            
            plt.plot(x, line_data)
            index += len_stats_dir

        set_text_font(plot, x, legend=legend)
        plt.xlabel("Connection idle time range")
        plt.ylabel("Occurance times")
        plt.title("Number of roll-backed blocks "+str(key))
        fig_line_chart.savefig(OUTPUT_DIRECTORY+"\\linechart_number_of_blocks_"+str(key)+".pdf", bbox_inches='tight')
        plt.close(fig_line_chart)
        fig_count += 1

            
            
    

def render_summary_box_plot():
    global fig_count
    
    OUTPUT_DIRECTORY = os.getcwd()+"\\box_plot_revokded_trans\\summary box plot\\"
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
        
    keys = list(dict_a.keys())
    keys.sort()

    for key in keys:
        #print(dict_a[key], len(dict_a[key][0]))
        # box plot
        legend = []
        fig_box_plot = plt.figure(fig_count, figsize=(10, 6))
        plot = fig_box_plot.add_subplot(111)
        # print(key, dict_a[key])
        bp = plot.boxplot(dict_a[key])
        legend.append("number of blocks "+str(key))
        set_text_font(plot, x)
        plt.xlabel("Connection idle time range")
        plt.ylabel("Occurance times")
        plt.title("Number of roll-backed blocks  "+str(key))
        fig_box_plot.savefig(OUTPUT_DIRECTORY+"\\number_of_blocks_"+str(key)+".pdf", bbox_inches='tight')
        plt.close(fig_box_plot)
        fig_count += 1

        
INPUT_DIRECTORY = os.getcwd()+"\\heteo_summary_stats"
OUTPUT_DIRECTORY = os.getcwd()+"\\box_plot_revokded_trans"
#correct_fmt_data_date = datetime(2019, 1, 23, 0, 0)
stats_directories = os.listdir(INPUT_DIRECTORY)
stats_files = os.listdir(INPUT_DIRECTORY + "\\" + stats_directories[0])
#correct_file_index = 0#stats_directories.index("2019-1-23") + 1

line_chart_data = []

if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

fig_count = 0
x = []

dict_a = {}
for i in range(0, 10):
    dict_a[i] = []

for file_num in range(0, len(stats_files)):
    for directory_num in range(0, len(stats_directories)):
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
                    #print(dict_a)
                    dict_a[key][num_line][-1] = value
                else:
                    break
            line = f.readline()
            num_line += 1


    # Box plot for all parameters of number of blocks for revoked transaction
    #render_box_plot_for_every_single_param()
    
    #render_line_chart_different_block_nums()
    
#render_summary_box_plot()

render_line_chart_different_hetero_contact_freq()

# Box plot for summary stats of number of blocks after revoked transactions





