import os
import GlobalConfig as GC


def is_block_different(index, blockchain_list):
    temp_block = blockchain_list[0][index]
    for blockchain in blockchain_list:
        if index >= len(blockchain) or blockchain[index] != temp_block:
            return True
    return False


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


def get_statistics(nodes_list):
    """
    Write final blockchain information of all nodes into a file
    :param filename: the name of the file that blockchain information is stored into
    :param nodes_list: all nodes
    :return: None
    """

    blockchain_list = []
    blockchain_owner = []
    longest_blockchain = []

    for node in nodes_list:
        if node.blockchain.chain not in blockchain_list:
            blockchain_list.append(node.blockchain.chain)
        if len(node.blockchain.chain) > len(longest_blockchain):
            longest_blockchain = node.blockchain.chain.copy()
        if len(blockchain_owner) != len(blockchain_list):
            blockchain_owner.append([])
        blockchain_owner[blockchain_list.index(node.blockchain.chain)].append(node.id)

    return blockchain_list, blockchain_owner


def write_statistics_into_file(blockchain_list, blockchain_owner, entire_transaction_list, num_of_blocks_in_fork):
    import BlockchainSimulator as BS

    file_path = os.getcwd()+"\\Log\\"

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    filename2 = GC.OUTPUT_FILE

    f2 = open(file_path+filename2, 'w+')
    origin_size_entire_transactions = len(entire_transaction_list)
    f2.write("Parameters:\n")
    f2.write("Contact frequency: "+str(GC.CONTACT_FREQ)+"\n")
    f2.write("Transaction generation rate: " + str(GC.TRANS_RATE) + "\n")
    f2.write("Random transactions: " + str(GC.RANDOM_TRANS) + "\n")
    f2.write("Random winners: " + str(GC.RANDOM_WINNERS) + "\n")
    f2.write("\n")
    f2.write("Summary: \n")
    f2.write("Contact frequency: "+ str(GC.CONTACT_FREQ)+", "+str(GC.CONTACT_FREQ+600)+"\n")
    f2.write("Transaction generation rate: " + str(GC.TRANS_RATE)+"\n")
    f2.write("Maximum of number of empty blocks after the lastest transaction block in fork: "
             + str(max(num_of_blocks_in_fork)) + "\n")
    f2.write("Minumum of number of empty blocks after the lastest transaction block in fork: "
             + str(min(num_of_blocks_in_fork)) + "\n")
    f2.write("Minumum of number of empty blocks after the lastest transaction block in fork: "
             + str(sum(num_of_blocks_in_fork)/len(num_of_blocks_in_fork)) + "\n")
    f2.write("Number of Blockchain: "+str(len(blockchain_list))+"\n")

    count = 0

    for blockchain in blockchain_list:
        f2.write("Blockchain "+str(count)+" Length: "+str(len(blockchain))+"\n")
        last_index = BS.find_last_block_with_trans(blockchain)
        f2.write("Convergence speed:" + str(blockchain[last_index]['time'])+"\n")
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


def write_csv_statistics_file(blockchain_list, num_of_blocks_in_fork, dict_num_of_blocks_in_fork):
    import BlockchainSimulator as BS

    last_block_timestamp = 0
    length_longest_blockchain = 0
    last_block_index_with_trans = 0
    last_block_timestamp_with_trans = 0
    filename_suffix = ""

    for blockchain in blockchain_list:
        if blockchain[-1]['time'] > last_block_timestamp:
            last_block_timestamp = blockchain[-1]['time']
        if len(blockchain) > length_longest_blockchain:
            length_longest_blockchain = len(blockchain)
        last_index = BS.find_last_block_with_trans(blockchain)
        if last_index > last_block_index_with_trans:
            last_block_index_with_trans = last_index
        if last_block_timestamp_with_trans == 0:
            last_block_timestamp_with_trans = blockchain[last_index]['time']
        else:
            last_trans_timestamp = blockchain[last_index]['time']
            if last_trans_timestamp != last_block_timestamp_with_trans:
                print("ERROR!!!!!", last_trans_timestamp, last_block_timestamp_with_trans)

    different_block_index = 0
    if len(blockchain_list) > 1:
        while different_block_index < len(blockchain_list[0]):
            if is_block_different(different_block_index, blockchain_list):
                break
            different_block_index += 1
    if different_block_index == 0:
        different_block_index = "None"

    filename_suffix += "_node"+str(GC.NUM_OF_NODES)
    filename_suffix += "_winners"+str(GC.NUM_OF_WINNERS)
    if GC.RANDOM_TRANS:
        filename_suffix += "_RT"
    if GC.RANDOM_WINNERS:
        filename_suffix += "_RW"
    if GC.RANDOM_START_CONNECT_TIME:
        filename_suffix += "_RSC"
    if GC.RANDOM_CONNECT_TIME:
        filename_suffix += "_RC"

    if not filename_suffix:
        filename_suffix = "_ALLFALSE"

    stat_file = 'statistics'+filename_suffix+'.csv'
    file_path = os.getcwd()+"\\Stats\\"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    if not os.path.exists(file_path+stat_file):
        f = open(os.getcwd()+"\\Stats\\"+stat_file, 'w+')
        f.write("Contact time interval, Lastest block timestamp with transactions, Convergence speed, "
                "Number of blockchain, Length of the longest blockchain, Block index with forks occurred, "
                "The last block contains transactions, Max num of blocks, Min num of blocks, Avg num of blocks"
                #"Converge 20%, Converge 40%, Converge 60%, Converge 80%, Converge 100%"
                +"\n")
        f.close()
    f = open(os.getcwd()+"\\Stats\\"+stat_file, 'a')

    #converge_progress_string = ""

    #for i in range(20, 101, 20):
    #    if i in converge_progress.keys():
    #        converge_progress_string += str(converge_progress[i])+", "
    #    else:
    #        converge_progress_string += "None, "
    #converge_progress_string = converge_progress_string[:-2]
    occurance_num_of_blocks_string = ""
    sorted_keys = list(dict_num_of_blocks_in_fork.keys())
    sorted_keys.sort()
    for i in sorted_keys:
        occurance_num_of_blocks_string += str(i)+": "+str(dict_num_of_blocks_in_fork[i]) + ", "
    occurance_num_of_blocks_string = occurance_num_of_blocks_string[:-2]
    f.write(str(GC.CONTACT_FREQ) + "-"+str(GC.CONTACT_FREQ+600) + ", "+str(last_block_timestamp_with_trans) + ", " +
            str(last_block_timestamp) + ", "+str(len(blockchain_list)) + ", " + str(length_longest_blockchain) + ", " +
            str(different_block_index) + ", " + str(last_block_index_with_trans) + ", " +
            str(max(num_of_blocks_in_fork)) + ", " + str(min(num_of_blocks_in_fork)) + ", " +
            str(sum(num_of_blocks_in_fork)/len(num_of_blocks_in_fork)) + #", " + converge_progress_string
            ", "+ occurance_num_of_blocks_string + "\n")
    f.close()
