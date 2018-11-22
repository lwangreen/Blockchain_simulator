import mysql.connector
import random
import os
from Nodes import Nodes


def get_node(node_id, nodes_list):
    for node in nodes_list:
        if node.id == node_id:
            return node


def write_transactions_into_file(f, transactions):
    f.write("-------------Incomplete transaction----------------:" + "\n")
    for t in transactions:
        f.write(str(t) + "\n")
    f.write("\n")

def write_blocks_into_file(f, blocks):
    """
    Write each block of a node into file
    :param f: file instance
    :param blocks: the blockchain of a node
    :return: None
    """
    for block in blocks:
        for keyword in block:
            if keyword != 'transactions':
                f.write(keyword+": "+str(block[keyword])+"\n")
            else:
                write_transactions_into_file(f, block['transactions'])
        f.write("\n")


def write_into_file(nodes_list, entire_transaction_list):
    """
    Write final blockchain information of all nodes into a file
    :param filename: the name of the file that blockchain information is stored into
    :param nodes_list: all nodes
    :return: None
    """
    blockchain_list = []
    filename1 = "testresult.txt"
    filename2 = "blockinfo.txt"
    file_path = os.getcwd()+"\\Log\\"
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    f = open(file_path+filename1, 'w+')
    f2 = open(file_path+filename2, 'w+')
    for node in nodes_list:
        f.write("Node ID:"+str(node.id)+"\n")
        write_transactions_into_file(f, node.blockchain.incomplete_transactions)

        f.write("-------------Blockchain:---------------------------:"+"\n")
        write_blocks_into_file(f, node.blockchain.chain)
        f.write("-------------------------------------------------------------------------------------\n")
        f.write("\n")


    f.close()


def retrieve_transaction_from_file(f, end_time):
    transactions = []
    t = f.readline()
    t = t.split()
    while t and int(t[0]) < end_time:
        transactions.append([int(t[i]) for i in range(len(t))])
        t = f.readline()
        t = t.split()
    if t:
        transactions.append([int(t[i]) for i in range(len(t))])
    #print("Time concern", end_time, transactions[-1][0])
    return transactions


def retrieve_transaction_records(records, current_time, time_interval):
    c_list = []

    while records:
        if records[0][0] >= current_time+time_interval:
            break
        c_list.append(records.pop(0))
    if c_list:
        return c_list
    return None


def random_select_winner(nodes_list):
    winners = []
    terminate_prob = random.random()
    node1 = random.choice(nodes_list)
    winners.append(node1)
    while terminate_prob < 0.8:
        node2 = random.choice(nodes_list)
        while node2 in winners:
            node2 = random.choice(nodes_list)
        winners.append(node2)
        break
    terminate_prob = random.random()
    while terminate_prob < 0.8:
        node3 = random.choice(nodes_list)
        while node3 in winners:
            node3 = random.choice(nodes_list)
        winners.append(node3)
        break

    return winners

current_time = 0
end_time = 100000
current_period_end_time = 10000
time_interval = 600
central_server_contact_frequency = 600 #seconds
next_broadcast_time = 0
nodes_list = []
current_transactions = []
entire_transaction_list = []
cnx = mysql.connector.connect(user='root', database='cambridge')
cur = cnx.cursor(buffered=True)

f = open(os.getcwd() + "\\Created_data_trace\\transaction.txt", 'r')

for i in range(20):
    nodes_list.append(Nodes(i))

while current_time < end_time:
    #fetch transaction
    if not current_transactions:
        current_transactions = retrieve_transaction_from_file(f, current_period_end_time)
        current_period_end_time += 10000
    current_transactions_within_time_interval = retrieve_transaction_records(current_transactions, current_time,
                                                                             time_interval)
    if current_transactions_within_time_interval:
        for t in current_transactions_within_time_interval:
            node1 = get_node(t[1], nodes_list)
            transaction = {
                'sender': t[1],
                'recipient': t[2],
                'amount': t[3],
                'timestamp': t[0],
            }
            node1.blockchain.add_new_transaction(transaction)
            entire_transaction_list.append(transaction)

    winners = random_select_winner(nodes_list)

    for w in winners:
        w.blockchain.add_new_block()
        #print(w.blockchain.chain)

    if current_time > next_broadcast_time:
        for node1 in nodes_list:
            for node2 in nodes_list:
                node1.blockchain.resolve_conflict_and_update_transactions(node2.blockchain)
                node2.blockchain.resolve_conflict_and_update_transactions(node1.blockchain)

    write_into_file(nodes_list, entire_transaction_list)

    current_time += time_interval
# print(nodes_id)