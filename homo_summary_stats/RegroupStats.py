import os
from datetime import datetime

def generate_record_string(record_list, contact_freq):
    str_record = ""
    contact_freq_index = 0
    while contact_freq_index < len(contact_freq):
        str_record += contact_freq[contact_freq_index]+", "
        for record in record_list:
            str_record += record[contact_freq_index]+", "
        str_record = str_record[:-2]+"\n"

        contact_freq_index += 1

    return str_record


stats_files = os.listdir(os.getcwd() + "\\averaged_stats")
plot_directory = os.getcwd() + "\\" + datetime.now().strftime('%Y-%m-%d %H-%M-%S')+"_plot_stats\\"
summarised_stats_files = ["latest_block_timestamp.csv", "convergence_speed.csv", "num_of_blockchain.csv",
                          "length_of_blockchain.csv", "block_index_with_transaction.csv",
                          "max_num_of_block.csv", "avg_num_of_block.csv"]
stats_keyword = [i.replace("statistics_", "").replace(".csv", "") for i in stats_files]

opened_files = []
opened_summary_files = []

contact_freq = []
latest_block_timestamp = []
convergence_speed = []
num_of_blockchain = []
length_of_blockchain = []
block_index_with_transaction = []
max_num_of_block = []
avg_num_of_block = []

if not os.path.exists(plot_directory):
    os.makedirs(plot_directory)
for f in stats_files:
    opened_file = open(os.getcwd()+"\\averaged_stats\\"+f, 'r')
    opened_file.readline()
    opened_files.append(opened_file)

for f in opened_files:
    temp_latest_block_timestamp = []
    temp_convergence_speed = []
    temp_num_of_blockchain = []
    temp_length_of_blockchain = []
    temp_block_index_with_transaction = []
    temp_max_num_of_block = []
    temp_avg_num_of_block = []

    line = f.readline()
    while line:
        line = line.replace("\n", "")
        line = line.split(', ')
        if line[0] not in contact_freq:
            contact_freq.append(line[0])
        temp_latest_block_timestamp.append(line[1])
        temp_convergence_speed.append(line[2])
        temp_num_of_blockchain.append(line[3])
        temp_length_of_blockchain.append(line[4])
        temp_block_index_with_transaction.append(line[6])
        temp_max_num_of_block.append(line[7])
        temp_avg_num_of_block.append(line[9])
        line = f.readline()

    latest_block_timestamp.append(temp_latest_block_timestamp)
    convergence_speed.append(temp_convergence_speed)
    num_of_blockchain.append(temp_num_of_blockchain)
    length_of_blockchain.append(temp_length_of_blockchain)
    block_index_with_transaction.append(temp_block_index_with_transaction)
    max_num_of_block.append(temp_max_num_of_block)
    avg_num_of_block.append(temp_avg_num_of_block)

for f in summarised_stats_files:
    opened_summary_files.append(open(plot_directory+f, 'w+'))

index = 0
str_keyword = "contact freq, "
for keyword in stats_keyword:
    str_keyword += keyword + ", "
str_keyword = str_keyword[:-2] + "\n"

while index < len(opened_summary_files):
    if index == 0:
        str_record = generate_record_string(latest_block_timestamp, contact_freq)

    elif index == 1:
        str_record = generate_record_string(convergence_speed, contact_freq)

    elif index == 2:
        str_record = generate_record_string(num_of_blockchain, contact_freq)

    elif index == 3:
        str_record = generate_record_string(length_of_blockchain, contact_freq)

    elif index == 4:
        str_record = generate_record_string(block_index_with_transaction, contact_freq)

    elif index == 5:
        str_record = generate_record_string(max_num_of_block, contact_freq)

    elif index == 6:
        str_record = generate_record_string(avg_num_of_block, contact_freq)

    opened_summary_files[index].write(str_keyword+str_record)

    index +=1


for f in opened_files:
    f.close()
