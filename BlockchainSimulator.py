import sys
import getopt
import random
import os
import FileWritting
from datetime import datetime
import GlobalConfig as GC
from Nodes import Nodes


def get_node(node_id, nodes_list):
    for node in nodes_list:
        if node.id == node_id:
            return node


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
        index -= 1
    return index


def is_only_one_blockchain_left(nodes_list):
    blockchain = []
    temp_last_index = 0
    for node in nodes_list:
        if node.blockchain.mempool:
            return False
        if not blockchain:
            blockchain = node.blockchain.chain.copy()
        else:
            if temp_last_index == 0:
                temp_last_index = find_last_block_with_trans(node.blockchain.chain)
            last_index = find_last_block_with_trans(node.blockchain.chain)
            if temp_last_index != last_index:
                return False
            if node.blockchain.chain[:last_index+1] != blockchain[:last_index+1]:
                return False
    return True


def running():

    current_time = 0
    end_time = 90000
    time_interval = 600
    nodes_list = []
    entire_transaction_list = []
    min_cfreq_range, max_cfreq_range = cal_contact_frequency_range(GC.CONTACT_FREQ, time_interval)
    if not GC.RANDOM_TRANS:
        current_period_end_time = 10000
        current_transactions_within_10000 = []
        f = open(os.getcwd() + "\\Created_data_trace\\transaction_"+str(GC.TRANS_RATE)+".txt", 'r')

    if not GC.RANDOM_WINNERS:
        current_period_end_time = 10000
        current_winners_within_10000 = []
        f2 = open(os.getcwd() +"\\Created_data_trace\\winners_long.txt", 'r')

    for i in range(20):
        nodes_list.append(Nodes(i, min_cfreq_range, max_cfreq_range, GC.RANDOM_START_CONNECT_TIME, GC.RANDOM_CONNECT_TIME))

    while current_time < end_time or not is_only_one_blockchain_left(nodes_list):
        # fetch transaction
        if GC.RANDOM_TRANS:
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

        if GC.RANDOM_WINNERS:
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

        if (not GC.RANDOM_WINNERS or not GC.RANDOM_TRANS) and current_period_end_time < current_time:
            current_period_end_time += 10000

        for node in nodes_list:
            node.update_next_connect_time(current_time)
        # print(current_time)

    blockchain_list, blockchain_owner = FileWritting.write_node_blockchain_into_file(nodes_list)
    FileWritting.write_statistics_into_file(blockchain_list, blockchain_owner, entire_transaction_list)
    FileWritting.write_csv_statistics_file(blockchain_list)

    # app_tran = 0
    #for node in nodes_list:
        #print("Node: "+str(node.id))
        #print(node.blockchain.mempool)
        # app_tran += len(node.blockchain.approved_transactions)
    # print(app_tran)
    print("FINISH")


def main(argv):

    try:
        file_suffix = ""
        opts, args = getopt.getopt(argv, "c:t:", ["CONTACT_FREQ=", "TRANS_RATE=", "RANDOM_TRANS=",
                                                        "RANDOM_WINNERS=", "RANDOM_CONNECT=", "RANDOM_START_CONNECT="])

        for opt, arg in opts:
            if opt in ("-c", "--CONTACT_FREQ"):
                GC.CONTACT_FREQ = int(arg)
                file_suffix += "_"+arg
            elif opt in ("-t", "--TRANS_RATE"):
                GC.TRANS_RATE = int(arg)
                file_suffix += "_" + arg
            elif opt in ("--RANDOM_TRANS"):
                GC.RANDOM_TRANS = eval(arg)
                if GC.RANDOM_TRANS:
                    file_suffix += "_RT"
            elif opt in ("--RANDOM_WINNERS"):
                GC.RANDOM_WINNERS = eval(arg)
                if GC.RANDOM_WINNERS:
                    file_suffix += "_RW"
            elif opt in ("--RANDOM_CONNECT"):
                GC.RANDOM_CONNECT_TIME = eval(arg)
                if GC.RANDOM_CONNECT_TIME:
                    file_suffix += "_RC"
            elif opt in ("--RANDOM_START_CONNECT"):
                GC.RANDOM_START_CONNECT_TIME = eval(arg)
                if GC.RANDOM_START_CONNECT_TIME:
                    file_suffix += "_RSC"

        GC.OUTPUT_FILE = datetime.now().strftime('%Y-%m-%d %H-%M-%S')+file_suffix+".txt"
        running()

    except getopt.GetoptError:
        print("Command line argument error")
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
