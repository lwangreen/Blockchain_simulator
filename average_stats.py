import os

data = []
prefix = []
attributes_name = []
DATA_FILLED = False

stats_directory_path = os.getcwd()+"\\summary_stats\\"
output_directory = os.getcwd()+"\\averaged_stats\\"
stats_directories = os.listdir(stats_directory_path)
stats_files = os.listdir(stats_directory_path+stats_directories[0])
print(stats_directories)

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for file in stats_files:
    file_count = 1
    data = []
    DATA_FILLED = False
    for directory in stats_directories:
        stats_file = stats_directory_path + directory + "\\" + file
        if os.path.exists(stats_file):
            f = open(stats_file, 'r')
            line = f.readline()
            num_line = 0
            while line:
                line = line.replace('\n', '')
                line = line.split(', ')
                if line[1].isdigit():
                    if not DATA_FILLED:
                        prefix.append(line[0])
                        line_list = []
                        for index in range(1, len(line)):
                            if line[index] == 'None':
                                line_list.append(0)
                            else:
                                line_list.append(float(line[index]))
                        data.append(line_list)
                    else:
                        for index in range(len(line)-1):
                            if line[index+1] == 'None':
                                line[index+1] = 0
                            data[num_line][index] += (float(line[index+1]) - data[num_line][index]) / float(file_count)
                        num_line += 1
                else:
                    if not attributes_name:
                        attributes_name = line
                line = f.readline()
            f.close()
            if not DATA_FILLED:
                DATA_FILLED = True
            file_count += 1

    output_file = open(output_directory+file, 'w')
    output_file.write(str(attributes_name).replace("'", "").replace('[', '').replace(']' ,'') + "\n")

    for row_num in range(len(data)):
        record_string = prefix[row_num]+", "
        for col_num in range(len(data[0])):
            record_string += str(data[row_num][col_num]) + ", "
        record_string = record_string[:-2] + "\n"
        output_file.write(record_string)
    output_file.close()





