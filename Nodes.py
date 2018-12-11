import Blockchain
import random


class Nodes:
    def __init__(self, id, min_time_interval, max_time_interval):
        self.id = id
        self.blockchain = Blockchain.NodeBlockchain(id)
        self.account_balance = 0
        self.next_broadcast_time = 0
        self.next_server_contact_time = 0
        #self.server_connect_time_interval = random.randint(min_time_interval, max_time_interval)
        self.server_connect_time_interval = max_time_interval

    def update_next_connect_time(self, time):
        while self.next_server_contact_time < time:
            self.next_server_contact_time += self.server_connect_time_interval

