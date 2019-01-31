import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os


def set_text_font():
    plt.xticks(fontsize=6, rotation=40)
    plt.yticks(fontsize=6)
    plt.legend(legend, fontsize=8, loc='upper left')


INPUT_DIRECTORY = os.getcwd()+"\\" + "2019-01-23 06-12-58_plot_stats"
OUTPUT_DIRECTORY = os.getcwd()+"\\" + "2019-01-23 06-12-58_plot_stats_auto"
X_FILLED = False
x = []
line_names = []
stats_files = os.listdir(INPUT_DIRECTORY)

if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

for file in stats_files:
    if file[-4:] == ".csv":
        x_cols = []
        y_label = file[-4:]

        f = open(INPUT_DIRECTORY+"\\"+file)
        if not line_names:
            line_names = f.readline().split(", ")[1:]
        else:
            line = f.readline()
        line = f.readline()
        while line:
            line = line.split(", ")
            if not X_FILLED:
                x.append(line[0])

            for index in range(1, len(line)):
                if len(x_cols) <= (index - 1):
                    x_cols.append([float(line[index])])
                else:
                    x_cols[index-1].append(float(line[index]))
            line = f.readline()
        X_FILLED = True
        f.close()

        for num in range(0, 3):
            legend = []
            fig = plt.figure(num, figsize=(6, 3))

            for num2 in range(num, len(x_cols), 3):
                plt.plot(x, x_cols[num2])
                legend.append(line_names[num2])
            set_text_font()

            if "winners3" in legend[0]:
                fig.savefig(OUTPUT_DIRECTORY + "\\"+file[:-4]+"_vs_nodes_winners3.pdf", bbox_inches='tight')
            elif "winners6" in legend[0]:
                fig.savefig(OUTPUT_DIRECTORY + "\\"+file[:-4]+"_vs_nodes_winners6.pdf", bbox_inches='tight')
            elif "winners9" in legend[0]:
                fig.savefig(OUTPUT_DIRECTORY + "\\"+file[:-4]+"_vs_nodes_winners9.pdf", bbox_inches='tight')

        fig_count = num + 1
        fig = plt.figure(fig_count, figsize=(21, 9))
        location = [(0, 0), (0, 2), (0, 4), (1, 1), (1, 3)]
        location_index = 0
        subplot = None
        for num in range(0, len(x_cols)):
            if num % 3 == 0:
                if subplot:
                    fig.add_subplot(subplot)

                subplot = plt.subplot2grid((2, 6), location[location_index], colspan=2)
                legend = []
                location_index += 1
            subplot.plot(x, x_cols[num])
            legend.append(line_names[num])
            set_text_font()

        fig.savefig(OUTPUT_DIRECTORY + "\\" + file[:-4] + "_vs_winners.pdf", bbox_inches='tight')
            # if "node20" in legend[0]:
            #     fig.savefig(OUTPUT_DIRECTORY + "\\" + file[:-4] + "_vs_winners_nodes20.pdf", bbox_inches='tight')
            # if "node30" in legend[0]:
            #     fig.savefig(OUTPUT_DIRECTORY + "\\" + file[:-4] + "_vs_winners_nodes30.pdf", bbox_inches='tight')
            # if "node40" in legend[0]:
            #     fig.savefig(OUTPUT_DIRECTORY + "\\" + file[:-4] + "_vs_winners_nodes40.pdf", bbox_inches='tight')
            # if "node50" in legend[0]:
            #     fig.savefig(OUTPUT_DIRECTORY + "\\" + file[:-4] + "_vs_winners_nodes50.pdf", bbox_inches='tight')
            # if "node60" in legend[0]:
            #     fig.savefig(OUTPUT_DIRECTORY + "\\" + file[:-4] + "_vs_winners_nodes60.pdf", bbox_inches='tight')

        print("---------------------------------------------------")


# x = ["0-600", "600-1200", "1200-1800", "1800-2400"]
# y = [1,2,3,4]
# f= plt.figure()
# plt.plot(x, y, label = "test")
# plt.title("test plot")
# plt.legend()
#
# f.savefig("test.pdf", bbox_inches = 'tight')

