import random
import os


def choose_nodes(len_node_list):
    node1 = random.randint(0, len_node_list-1)
    node2 = random.randint(0, len_node_list-1)
    while node2 == node1:
        node2 = random.randint(0, len_node_list-1)
    return node1, node2


def write_into_file(f, transaction_time, node1, node2, transaction_amount):
    f.write(str(transaction_time)+" "+str(node1)+" "+str(node2)+" "+str(transaction_amount)+"\n")


def generate_nodes_transaction():
    node1, node2 = choose_nodes(20)
    transaction_amount = random.randint(0, 9999)
    return node1, node2, transaction_amount


dur = 600       # Time flows by 600 secs a time
endtime = 80000
time = 0
count = 0

file_path = os.getcwd() + "\\Created_data_trace\\"
if not os.path.exists(file_path):
    os.makedirs(file_path)

f = open(file_path+"transaction.txt", 'w+')
count = 0

while time < endtime:
    time_elapse = random.randint(0, 300)
    time += time_elapse

    node1, node2, transaction_amount = generate_nodes_transaction()
    write_into_file(f, time, node1, node2, transaction_amount)
    repeat = random.random()
    count += 1

    while repeat > 0.7:
        node1, node2, transaction_amount = generate_nodes_transaction()
        write_into_file(f, time, node1, node2, transaction_amount)
        repeat = random.random()
        count += 1

f.close()
print(count)
