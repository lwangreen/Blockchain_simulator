import matplotlib.pyplot as plt
import numpy as np
import os

INPUT_DIRECTORY = os.getcwd()+"\\"+"2019-01-23 06-12-58_plot_stats"
# OUTPUT_DIRECTORY = "2019-01-23 06-12-58_plot_stats"
X_FILLED = False
x = []
stats_files = os.listdir(INPUT_DIRECTORY)
print(stats_files)

for file in stats_files:
    if file[-4:] == ".csv":
        f = open(INPUT_DIRECTORY+"\\"+file)
        f.readline()
        line = f.readline()
        while line:
            line = line.split(", ")
            if not X_FILLED:
                x.append(line[0])
            
        X_FILLED = True
# x = ["0-600", "600-1200", "1200-1800", "1800-2400"]
# y = [1,2,3,4]
# f= plt.figure()
# plt.plot(x, y, label = "test")
# plt.title("test plot")
# plt.legend()
#
# f.savefig("test.pdf", bbox_inches = 'tight')

