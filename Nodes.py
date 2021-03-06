import Blockchain
import random
import GlobalConfig as GC

class Nodes:
    def __init__(self, id, min_time_interval, max_time_interval, RSC, RC):
        self.id = id
        self.blockchain = Blockchain.NodeBlockchain(id)
        self.account_balance = 0
        self.next_broadcast_time = 0
        self.max_time = max_time_interval * 2

        if RSC:
            self.next_server_contact_time = random.randint(min_time_interval, max_time_interval)
        else:
            self.next_server_contact_time = 0

        if RC:
            self.server_connect_time_interval = random.randint(min_time_interval, max_time_interval)
        else:
            self.server_connect_time_interval = max_time_interval

    def update_next_connect_time(self, time):
        while self.next_server_contact_time < time:
            self.next_server_contact_time += self.server_connect_time_interval

