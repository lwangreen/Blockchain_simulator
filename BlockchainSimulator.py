import mysql.connector
import random
import os
from Nodes import Nodes


def get_node(node_id, nodes_list):
    for node in nodes_list:
        if node.id == node_id:
            return node


def write_transactions_into_file(f, transactions):
    for t in transactions:
        f.write(str(t) + "\n")


def write_blocks_into_file(f, blocks):
    """
    Write each block of a node into file
    :param f: file instance
    :param blocks: the blockchain of a node
    :return: None
    """
    f.write("-------------Blockchain:---------------------------:" + "\n")
    for block in blocks:
        for keyword in block:
            if keyword != 'transactions':
                f.write(keyword+": "+str(block[keyword])+"\n")
            else:
                write_transactions_into_file(f, block['transactions'])
        f.write("\n")
    f.write("-------------------------------------------------------------------------------------\n")
    f.write("\n")


def is_block_different(index, blockchain_list):
    temp_block = blockchain_list[0][index]
    for blockchain in blockchain_list:
        if blockchain[index] != temp_block:
            return True
    return False



def write_node_blockchain_into_file(nodes_list):
    """
    Write final blockchain information of all nodes into a file
    :param filename: the name of the file that blockchain information is stored into
    :param nodes_list: all nodes
    :return: None
    """

    blockchain_list = []
    blockchain_owner = []
    longest_blockchain = []
    filename1 = "Nodes_blockchain.txt"

    file_path = os.getcwd()+"\\Log\\"

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    f = open(file_path+filename1, 'w+')

    for node in nodes_list:
        if node.blockchain.chain not in blockchain_list:
            blockchain_list.append(node.blockchain.chain)
        if len(node.blockchain.chain) > len(longest_blockchain):
            longest_blockchain = node.blockchain.chain.copy()
        if len(blockchain_owner) != len(blockchain_list):
            blockchain_owner.append([])
        blockchain_owner[blockchain_list.index(node.blockchain.chain)].append(node.id)

        f.write("Node ID:"+str(node.id)+"\n")

        f.write("-------------Incomplete transaction----------------:" + "\n")
        write_transactions_into_file(f, node.blockchain.incomplete_transactions)
        f.write("\n")

        write_blocks_into_file(f, node.blockchain.chain)

    f.close()
    return blockchain_list, blockchain_owner


def write_statistics_into_file(blockchain_list, blockchain_owner, entire_transaction_list):
    filename2 = "statistics.txt"
    file_path = os.getcwd() + "\\Log\\"

    f2 = open(file_path+filename2, 'w+')
    origin_size_entire_transactions = len(entire_transaction_list)

    f2.write("Summary: \n")
    f2.write("Number of Blockchain: "+str(len(blockchain_list))+"\n")
    count = 0
    print(len(blockchain_list))


    for blockchain in blockchain_list:
        f2.write("Blockchain "+str(count)+" Length: "+str(len(blockchain))+"\n")
        temp_entire_transaction_list = entire_transaction_list.copy()
        print(len(temp_entire_transaction_list))
        for block in blockchain:
            for transaction in block['transactions']:
                if transaction in temp_entire_transaction_list:
                    temp_entire_transaction_list.remove(transaction)
        print(len(temp_entire_transaction_list))
        f2.write("Owners: "+str(blockchain_owner[blockchain_list.index(blockchain)])+"\n")
        f2.write("Number of all transactions: " + str(origin_size_entire_transactions) + "\n")
        f2.write("Number of transactions not in lonest chain: " + str(len(temp_entire_transaction_list)) + "\n")
        count+=1

    f2.write("\n")
    f2.write("Block difference \n")

    index = 0

    if len(blockchain_list) > 1:
        while index < len(blockchain_list[0]):
            if is_block_different(index, blockchain_list):
                for blockchain in blockchain_list:
                    f2.write("Blockchain "+str(blockchain_list.index(blockchain))+"\n")
                    write_blocks_into_file(f2, [blockchain[index]])
            index+=1

    f2.write("\n")
    for blockchain in blockchain_list:
        write_blocks_into_file(f2, blockchain)
    #write_transactions_into_file(f2, entire_transaction_list)

    f2.close()

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
#central_server_contact_frequency = 600 #seconds
nodes_list = []
current_transactions = []
entire_transaction_list = []
min_time_interval = 0
max_time_interval = 600
cnx = mysql.connector.connect(user='root', database='cambridge')
cur = cnx.cursor(buffered=True)

f = open(os.getcwd() + "\\Created_data_trace\\transaction.txt", 'r')

for i in range(20):
    nodes_list.append(Nodes(i, min_time_interval, max_time_interval))

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
    print([i.id for i in winners])
    for w in winners:
        w.blockchain.add_new_block()

    for node1 in nodes_list:
        for node2 in nodes_list:
            if(current_time <= node1.next_server_contact_time <= current_time+time_interval
                    and current_time <= node2.next_server_contact_time <= current_time+time_interval):
                node1.blockchain.resolve_conflict_and_update_transactions(node2.blockchain)
                node2.blockchain.resolve_conflict_and_update_transactions(node1.blockchain)

    current_time += time_interval
    for node in nodes_list:
        node.update_next_connect_time(current_time)

blockchain_list, blockchain_owner = write_node_blockchain_into_file(nodes_list)
write_statistics_into_file(blockchain_list, blockchain_owner, entire_transaction_list)

for node in nodes_list:
    print(len(node.blockchain.approved_transactions))
