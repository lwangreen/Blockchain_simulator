import Blockchain


class Nodes:
    def __init__(self, id):
        self.id = id
        self.blockchain = Blockchain.NodeBlockchain(id)
        self.account_balance = 0
        self.next_broadcast_time = 0
