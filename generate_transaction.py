import random
import os

NUM_TRANS = 20
NUM_NODES = 60

def write_into_file(f, transaction_time, node1, node2, transaction_amount):
    f.write(str(transaction_time)+" "+str(node1)+" "+str(node2)+" "+str(transaction_amount)+"\n")


def generate_transactions(len_nodes_list, time, time_interval):
    global NUM_TRANS
    trans_count = 0
    #total_trans = TRANS_RATE * len_nodes_list
    transactions = []
    while trans_count < NUM_TRANS:
        node1 = random.randint(0, len_nodes_list-1)
        node2 = random.randint(0, len_nodes_list-1)
        while node2 == node1:
            node2 = random.randint(0, len_nodes_list-1)
        time = random.randint(time, time+time_interval)
        amount = random.randint(0, 9999)
        transactions.append([time, node1, node2, amount])
        trans_count += 1
    return transactions, trans_count


dur = 600       # Time flows by 600 secs a time
endtime = 80000
time = 0
count = 0

file_path = os.getcwd() + "\\Created_data_trace\\"
if not os.path.exists(file_path):
    os.makedirs(file_path)

f = open(file_path+"transaction_nodes_"+str(NUM_NODES)+".txt", 'w+')
count = 0

while time < endtime:
    transactions, trans_count = generate_transactions(NUM_NODES, time, dur)
    for t in transactions:
        write_into_file(f, t[0], t[1], t[2], t[3])

    time += dur
    count += trans_count

f.close()
print(count)
