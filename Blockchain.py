import hashlib
import json


class NodeBlockchain:
    def __init__(self, id):
        self.id = id
        self.chain = []
        self._mempool = []
        self.unsolved_block = {}
        self.approved_transactions = []
        self.max_trans_per_block = 50
        #self.max_trans_in_mempool = 4096
        self.create_unsolved_block(None)

    @property
    def mempool(self):
        return self._mempool

    @mempool.setter
    def mempool(self, transaction):
        """
        Observer pattern that keeps track on self._mempool list.
        PoW is only triggered when there are incompleted transactions exist.
        If there is any new transaction added into the list, we start the PoW all over again.
        When a new block is generated, we clean the incomplete transaction list and shut down the PoW thread
        :param transaction:
        :return:
        """

        # clean transaction list after a block is generated.
        if not transaction:
            self._mempool = []

        # remove the transactions that was added in to the new block
        elif type(transaction) == list:
            self._mempool = transaction

        # add new incomplete transaction into the incomplete transaction list
        else:
            # if len(self._mempool) < self.max_trans_in_mempool:
            self._mempool.append(transaction)
            self.unsolved_block['transactions'] = self._mempool.copy()  # [:self.max_trans_per_block]

    def create_unsolved_block(self, previous_hash):
        self.unsolved_block = {
            'index': len(self.chain)+1,
            'transactions': self.mempool,  # [:self.max_trans_per_block],
            'previous_hash': previous_hash,
            'block generator': self.id
        }

    def add_new_block(self, time):
        self.unsolved_block['time'] = time
        self.chain.append(self.unsolved_block)
        for t in self.unsolved_block['transactions']:
            if t not in self.approved_transactions:
                self.approved_transactions.append(t)

        # self.mempool = self.mempool[self.max_trans_per_block:]
        self.mempool = []
        self.create_unsolved_block(self.hash(self.chain[-1]))

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_new_transaction(self, transaction):
        if transaction not in self.mempool and transaction not in self.approved_transactions:
            self.mempool = transaction

    def resolve_conflict(self, other_node):
        if len(other_node.chain) > len(self.chain):  # and self.valid_chain(other_node.chain):

            self.chain = other_node.chain.copy()

            self.create_unsolved_block(self.hash(self.chain[-1]))

            # If the transactions are approved but not in current longest chain:
            # Remove it from approved transaction list and add it back to incomplete transaction again, and wait for
            # next block generation
            for transaction in self.approved_transactions:
                if transaction not in other_node.approved_transactions:
                    self.mempool = transaction
                    self.approved_transactions.remove(transaction)

            # If the transactions in the longest chain are not in self approved transaction list
            for block in self.chain:
                for transaction in block['transactions']:
                    if transaction not in self.approved_transactions:
                        self.approved_transactions.append(transaction)
                    if transaction in self.mempool:
                        self.mempool.remove(transaction)

    def broadcast_transactions(self, other_node):
        if other_node.mempool:
            for transaction in other_node.mempool:
                if transaction not in self.mempool and transaction not in self.approved_transactions:
                    self.add_new_transaction(transaction)


