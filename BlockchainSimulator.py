import hashlib
from Nodes import Nodes


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
    for block in blocks:
        for keyword in block:
            if keyword != 'transactions':
                f.write(keyword+": "+str(block[keyword])+"\n")
            else:
                write_transactions_into_file(f, block['transactions'])
        f.write("\n")


def write_into_file(filename, nodes_list):
    """
    Write final blockchain information of all nodes into a file
    :param filename: the name of the file that blockchain information is stored into
    :param nodes_list: all nodes
    :return: None
    """
    file_path = os.getcwd()+"\\Log\\"
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    f = open(file_path+filename, 'w+')
    for node in nodes_list:
        f.write("Node ID:"+str(node.id)+"\n")
        f.write("-------------Incomplete transaction----------------:"+"\n")
        write_transactions_into_file(f, node.blockchain.incomplete_transactions)
        f.write("\n")
        f.write("-------------Blockchain:---------------------------:"+"\n")
        write_blocks_into_file(f, node.blockchain.chain)

        f.write("-------------------------------------------------------------------------------------\n")
        f.write("\n")
    f.close()


current_time = 0
end_time = 100000
time_interval = 600
central_server_contact_frequency = 600 #seconds
next_broadcast_time = 0
nodes_list = []
chain_dict = {} #dict: (chain:nodes list)

for i in range(20):
    nodes_list.append(Nodes(i))

while current_time < end_time:
    if current_time > next_broadcast_time:
        for node1 in nodes_list:
            chain_dict = node1.update_chain(chain_dict)

            for node2 in nodes_list:

                node1.broadcast_transactions(node2)
                node2.broadcast_transactions(node1)
                node1.resolve_conflict(node2)
                node2.resolve_conflict(node1)


print(nodes_id)