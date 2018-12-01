import sys
import getopt
import random
import os
from Nodes import Nodes

contact_freq = 0
trans_rate = 0

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
        write_transactions_into_file(f, node.blockchain.incomplete_transactions)
        f.write("\n")

        write_blocks_into_file(f, node.blockchain.chain)

    f.close()
    return blockchain_list, blockchain_owner


def write_statistics_into_file(blockchain_list, blockchain_owner, entire_transaction_list):
    global contact_freq
    global trans_rate

    filename2 = "statistics.txt"
    file_path = os.getcwd() + "\\Log\\"

    f2 = open(file_path+filename2, 'w+')
    origin_size_entire_transactions = len(entire_transaction_list)

    f2.write("Summary: \n")
    f2.write("Contact frequency: "+ str(contact_freq)+", "+str(contact_freq+600)+"\n")
    f2.write("Transaction generation rate: "+ str(trans_rate)+"\n")
    f2.write("Number of Blockchain: "+str(len(blockchain_list))+"\n")
    count = 0

    for blockchain in blockchain_list:
        f2.write("Blockchain "+str(count)+" Length: "+str(len(blockchain))+"\n")
        temp_entire_transaction_list = entire_transaction_list.copy()
        for block in blockchain:
            for transaction in block['transactions']:
                if transaction in temp_entire_transaction_list:
                    temp_entire_transaction_list.remove(transaction)
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
                    if(index < len(blockchain)):
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

def generate_transactions(nodes_list, time, time_interval):
    global trans_rate
    trans_count = 0
    total_trans = trans_rate * len(nodes_list)
    transactions = []
    while trans_count < total_trans:
        node1 = random.randint(0, len(nodes_list)-1)
        node2 = random.randint(0, len(nodes_list)-1)
        while node2 == node1:
            node2 = random.randint(0, len(nodes_list)-1)
        time = random.randint(time, time+time_interval)
        amount = random.randint(0, 9999)
        transaction = {
            'sender': node1,
            'recipient': node2,
            'amount': amount,
            'timestamp': time,
        }
        transactions.append(transaction)
        trans_count += 1
    return transactions


def random_select_winner(nodes_list):
    winners = []
    terminate_prob = 0
    ongoing_winning_time = 0
    while terminate_prob < 0.8 and len(winners) < 3:
        node = random.choice(nodes_list)
        while node in winners:
            node = random.choice(nodes_list)
        ongoing_winning_time += random.randint(0, 200)
        winners.append([node, ongoing_winning_time])

        terminate_prob = random.random()

    return winners

def cal_contact_frequency_range(cfreq_arg, time_interval):
    min_cfreq_range = int(cfreq_arg/time_interval) * time_interval
    max_cfreq_range = min_cfreq_range + time_interval
    return min_cfreq_range, max_cfreq_range

def running():
    current_time = 0
    end_time = 100000
    current_period_end_time = 10000
    time_interval = 600
    nodes_list = []
    current_transactions = []
    entire_transaction_list = []
    min_cfreq_range, max_cfreq_range = cal_contact_frequency_range(contact_freq, time_interval)
    #f = open(os.getcwd() + "\\Created_data_trace\\transaction.txt", 'r')

    for i in range(20):
        nodes_list.append(Nodes(i, min_cfreq_range, max_cfreq_range))

    while current_time < end_time:
        # fetch transaction
        #if not current_transactions:
            #current_transactions = retrieve_transaction_from_file(f, current_period_end_time)
            #current_period_end_time += 10000
        #current_transactions_within_time_interval = retrieve_transaction_records(current_transactions, current_time,
        #                                                                         time_interval)

        #if current_transactions_within_time_interval:
            #for t in current_transactions_within_time_interval:
                #node1 = get_node(t[1], nodes_list)
                #transaction = {
                #    'sender': t[1],
                #    'recipient': t[2],
                #    'amount': t[3],
                #    'timestamp': t[0],
                #}
        #       node1.blockchain.add_new_transaction(transaction)
        #       entire_transaction_list.append(transaction)

        if(current_time < end_time - 20000):
            current_transactions = generate_transactions(nodes_list, current_time, time_interval)
            for transaction in current_transactions:
                node1 = get_node(transaction['sender'], nodes_list)
                node1.blockchain.add_new_transaction(transaction)
                entire_transaction_list.append(transaction)
            winners = random_select_winner(nodes_list)
            print(winners)
            for winner_index in range(len(winners)):
                if winner_index > 0:
                    if winners[winner_index][1] - winners[winner_index - 1][1] < 100:
                        winners[winner_index][0].blockchain.add_new_block()


        for node1 in nodes_list:
            for node2 in nodes_list:
                if (node1 != node2 and current_time <= node1.next_server_contact_time <= current_time + time_interval
                        and current_time <= node2.next_server_contact_time <= current_time + time_interval):

                    node1.blockchain.resolve_conflict_and_update_transactions(node2.blockchain)
                    node2.blockchain.resolve_conflict_and_update_transactions(node1.blockchain)



        current_time += time_interval
        for node in nodes_list:
            node.update_next_connect_time(current_time)
        print(current_time)

    blockchain_list, blockchain_owner = write_node_blockchain_into_file(nodes_list)
    write_statistics_into_file(blockchain_list, blockchain_owner, entire_transaction_list)

    #app_tran = 0
    #for node in nodes_list:
        #print(len(node.blockchain.approved_transactions))
        #app_tran += len(node.blockchain.approved_transactions)
    #print(app_tran)

def main(argv):
    global contact_freq
    global trans_rate
    try:
        opts, args = getopt.getopt(argv, "c:t:", ["contact_freq=", "trans_rate:"])
        for opt, arg in opts:
            if opt in ("-c", "--contact_feq"):
                contact_freq = int(arg)
            elif opt in ("-t", "--trans_rate"):
                trans_rate = int(arg)
        running()

    except getopt.GetoptError:
        print("Command line argument error")
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])