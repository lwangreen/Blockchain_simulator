import sys
import getopt
import random
import os
from Nodes import Nodes

CONTACT_FREQ = 0
TRANS_RATE = 1
RANDOM_TRANS = False
RANDOM_WINNERS = False
OUTPUT_FILE = ""

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
        if index >= len(blockchain) or blockchain[index] != temp_block:
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
        write_transactions_into_file(f, node.blockchain.mempool)
        #for block in node.blockchain.chain[-6:]:
        #    write_transactions_into_file(f, block['transactions'])
        #f.write("\n")

        #write_blocks_into_file(f, node.blockchain.chain)

    f.close()
    return blockchain_list, blockchain_owner


def write_statistics_into_file(blockchain_list, blockchain_owner, entire_transaction_list):
    global CONTACT_FREQ
    global TRANS_RATE
    global OUTPUT_FILE

    filename2 = OUTPUT_FILE
    file_path = os.getcwd() + "\\Log\\"

    f2 = open(file_path+filename2, 'w+')
    origin_size_entire_transactions = len(entire_transaction_list)
    f2.write("Parameters:\n")
    f2.write("Contact frequency: "+str(CONTACT_FREQ)+"\n")
    f2.write("Transaction generation rate: " + str(TRANS_RATE) + "\n")
    f2.write("Random transactions: " + str(RANDOM_TRANS) + "\n")
    f2.write("Random winners: " + str(RANDOM_WINNERS) + "\n")
    f2.write("\n")
    f2.write("Summary: \n")
    f2.write("Contact frequency: "+ str(CONTACT_FREQ)+", "+str(CONTACT_FREQ+600)+"\n")
    f2.write("Transaction generation rate: "+ str(TRANS_RATE)+"\n")
    f2.write("Number of Blockchain: "+str(len(blockchain_list))+"\n")
    count = 0

    for blockchain in blockchain_list:
        f2.write("Blockchain "+str(count)+" Length: "+str(len(blockchain))+"\n")
        last_index = find_last_block_with_trans(blockchain)
        f2.write("Convergence speed:"+ str(blockchain[last_index]['time'])+"\n")
        f2.write("Timestamp of the last block:" + str(blockchain[-1]['time']) + "\n")
        temp_entire_transaction_list = entire_transaction_list.copy()
        for block in blockchain:
            for transaction in block['transactions']:
                if transaction in temp_entire_transaction_list:
                    temp_entire_transaction_list.remove(transaction)
        f2.write("Owners: "+str(blockchain_owner[blockchain_list.index(blockchain)])+"\n")
        f2.write("Number of all transactions: " + str(origin_size_entire_transactions) + "\n")
        f2.write("Number of transactions not in the longest chain: " + str(len(temp_entire_transaction_list)) + "\n")
        count += 1

    f2.write("\n")
    index = 0

    if len(blockchain_list) > 1:
        f2.write("Block difference: \n")
        while index < len(blockchain_list[0]):
            if is_block_different(index, blockchain_list):
                for blockchain in blockchain_list:
                    f2.write("Blockchain "+str(blockchain_list.index(blockchain))+"\n")
                    if(index < len(blockchain)):
                        write_blocks_into_file(f2, [blockchain[index]])
            index += 1
        f2.write("-------------------------------------------------------------------------------------\n")
        f2.write("\n")
    for blockchain in blockchain_list:
        write_blocks_into_file(f2, blockchain)
    f2.close()


def retrieve_records_from_file(f, end_time):
    records = []
    t = f.readline()
    t = t.split()
    while t and int(t[0]) < end_time:
        records.append([int(t[i]) for i in range(len(t))])
        t = f.readline()
        t = t.split()
    if t:
        records.append([int(t[i]) for i in range(len(t))])
    return records


def retrieve_records_from_temp_storage(records, current_time, time_interval):
    r_list = []
    while records:
        if records[0][0] >= current_time+time_interval:
            break
        r_list.append(records[0])
        records.pop(0)
    if r_list:
        return r_list
    return None


def generate_transactions(nodes_list, time, time_interval):
    global TRANS_RATE
    trans_count = 0
    total_trans = TRANS_RATE * len(nodes_list)
    transactions = []
    while trans_count < total_trans:
        node1 = random.randint(0, len(nodes_list)-1)
        node2 = random.randint(0, len(nodes_list)-1)
        while node2 == node1:
            node2 = random.randint(0, len(nodes_list)-1)
        time = random.randint(time, time+time_interval)
        amount = random.randint(0, 9999)
        transactions.append([time, node1, node2, amount])
        trans_count += 1
    return transactions


def random_select_winner(time, nodes_list, num_of_winners):
    winners = []

    terminate_prob = 0
    ongoing_winning_time = 0
    while terminate_prob < 0.8 and len(winners) < num_of_winners:
        node = random.randint(0, len(nodes_list)-1)
        ongoing_winning_time += random.randint(0, 200)
        winners.append([time+ongoing_winning_time, node])
        terminate_prob = random.random()
    return winners


def cal_contact_frequency_range(cfreq_arg, time_interval):
    min_cfreq_range = int(cfreq_arg/time_interval) * time_interval
    max_cfreq_range = min_cfreq_range + time_interval
    return min_cfreq_range, max_cfreq_range


def find_last_block_with_trans(blockchain):
    index = len(blockchain)-1
    while index > 0:
        if blockchain[index]['transactions']:
            break
        index -=1
    return index

def is_only_one_blockchain_left(nodes_list):
    blockchain = []
    for node in nodes_list:
        if node.blockchain.mempool:
            return False
        if not blockchain:
            blockchain = node.blockchain.chain.copy()
        else:
            if not node.blockchain.chain[-1]['transactions']:
                last_index = find_last_block_with_trans(node.blockchain.chain)
                if node.blockchain.chain[:last_index+1] != blockchain[:last_index+1]:
                    return False
            else:
                if node.blockchain.chain != blockchain:
                    return False
    return True


def running():
    current_time = 0
    end_time = 100000
    time_interval = 600
    nodes_list = []
    entire_transaction_list = []
    min_cfreq_range, max_cfreq_range = cal_contact_frequency_range(CONTACT_FREQ, time_interval)
    if not RANDOM_TRANS:
        current_period_end_time = 10000
        current_transactions_within_10000 = []
        f = open(os.getcwd() + "\\Created_data_trace\\transaction_"+str(TRANS_RATE)+".txt", 'r')
        print(os.getcwd() + "\\Created_data_trace\\transaction_"+str(TRANS_RATE)+".txt")

    if not RANDOM_WINNERS:
        current_period_end_time = 10000
        current_winners_within_10000 = []
        f2 = open(os.getcwd() +"\\Created_data_trace\\winners_long.txt", 'r')

    for i in range(20):
        nodes_list.append(Nodes(i, min_cfreq_range, max_cfreq_range))

    while current_time < end_time or not is_only_one_blockchain_left(nodes_list):
        # fetch transaction
        if RANDOM_TRANS:
            current_transactions = generate_transactions(nodes_list, current_time, time_interval)
        else:
            if not current_transactions_within_10000:
                current_transactions_within_10000 = retrieve_records_from_file(f, current_period_end_time)
            current_transactions = retrieve_records_from_temp_storage(current_transactions_within_10000,
                                                                          current_time, time_interval)
        if current_transactions:
            for t in current_transactions:
                node1 = get_node(t[1], nodes_list)
                transaction = {
                    'sender': t[1],
                    'recipient': t[2],
                    'amount': t[3],
                    'timestamp': t[0],
                }
                node1.blockchain.add_new_transaction(transaction)
                entire_transaction_list.append(transaction)

        if RANDOM_WINNERS:
            winners = random_select_winner(current_time, nodes_list, 3)
        else:
            if not current_winners_within_10000:
                current_winners_within_10000 = retrieve_records_from_file(f2, current_period_end_time)
            winners = retrieve_records_from_temp_storage(current_winners_within_10000, current_time, time_interval)
            if not winners:
                winners = random_select_winner(current_time, nodes_list, 1)

        if winners:
            for winner_index in range(len(winners)):
                winner = get_node(winners[winner_index][1], nodes_list)
                winner.blockchain.add_new_block(winners[winner_index][0])

        for node1 in nodes_list:
            for node2 in nodes_list:
                if (node1 != node2 and current_time <= node1.next_server_contact_time <= current_time + time_interval
                        and current_time <= node2.next_server_contact_time <= current_time + time_interval):
                    node1.blockchain.broadcast_transactions(node2.blockchain)
                    node2.blockchain.broadcast_transactions(node1.blockchain)
                    node1.blockchain.resolve_conflict(node2.blockchain)
                    node2.blockchain.resolve_conflict(node1.blockchain)

        current_time += time_interval

        if (not RANDOM_WINNERS or not RANDOM_TRANS) and current_period_end_time < current_time:
            current_period_end_time += 10000

        for node in nodes_list:
            node.update_next_connect_time(current_time)
        print(current_time)

    blockchain_list, blockchain_owner = write_node_blockchain_into_file(nodes_list)
    write_statistics_into_file(blockchain_list, blockchain_owner, entire_transaction_list)

    # app_tran = 0
    for node in nodes_list:
        print("Node: "+str(node.id))
        print(node.blockchain.mempool)
        # app_tran += len(node.blockchain.approved_transactions)
    # print(app_tran)


def main(argv):
    global CONTACT_FREQ
    global TRANS_RATE
    global RANDOM_TRANS
    global RANDOM_WINNERS
    global OUTPUT_FILE

    try:
        opts, args = getopt.getopt(argv, "c:t:o:", ["CONTACT_FREQ=", "TRANS_RATE=", "OUTPUT_FILE=", "RANDOM_TRANS=",
                                                        "RANDOM_WINNERS="])
        for opt, arg in opts:
            if opt in ("-c", "--CONTACT_FREQ"):
                CONTACT_FREQ = int(arg)
            elif opt in ("-t", "--TRANS_RATE"):
                TRANS_RATE = int(arg)
            elif opt in ("-o", "--OUTPUT_FILE"):
                OUTPUT_FILE = str(arg)
            elif opt in ("--RANDOM_TRANS"):
                RANDOM_TRANS = int(arg)
            elif opt in ("--RANDOM_WINNERS"):
                RANDOM_WINNERS = int(arg)
        running()

    except getopt.GetoptError:
        print("Command line argument error")
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
