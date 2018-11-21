import hashlib
import json



class NodeBlockchain:
    def __init__(self, id):
        self.id = id
        self.chain = []
        self._incomplete_transactions = []
        self.unsolved_block = {}
        self.create_unsolved_block(None)

    @property
    def incomplete_transactions(self):
        return self._incomplete_transactions

    @incomplete_transactions.setter
    def incomplete_transactions(self, transaction):
        """
        Observer pattern that keeps track on self._incomplete_transactions list.
        PoW is only triggered when there are incompleted transactions exist.
        If there is any new transaction added into the list, we start the PoW all over again.
        When a new block is generated, we clean the incomplete transaction list and shut down the PoW thread
        :param transaction:
        :return:
        """

        # clean transaction list after a block is generated.
        if not transaction:
            self._incomplete_transactions = []

        # add new transaction into incomplete_transaction and start PoW thread all over again
        else:
            self._incomplete_transactions.append(transaction)
            self.unsolved_block['transactions'] = self._incomplete_transactions.copy()

    def create_unsolved_block(self, previous_hash):
        self.unsolved_block = {
            'index': len(self.chain)+1,
            'transactions': self.incomplete_transactions,
            'previous_hash': previous_hash,
            'block generator': self.id
        }

    def add_new_block(self):
        self.chain.append(self.unsolved_block)
        self.incomplete_transactions = []
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
        self.incomplete_transactions = transaction


    def resolve_conflict_and_update_transactions(self, other_node):
        if len(other_node.chain) > len(self.chain):  # and self.valid_chain(other_node.chain):
            self.chain = other_node.chain.copy()
            self.create_unsolved_block(self.hash(self.chain[-1]))

            if other_node.incomplete_transactions:
                self.broadcast_transactions(other_node)

            if self.incomplete_transactions:
                for block in self.chain:
                    self.remove_approved_incomplete_transactions(block)


    def broadcast_transactions(self, other_node):
        if other_node.incomplete_transactions:
            for transaction in other_node.incomplete_transactions:
                if transaction not in self.incomplete_transactions:
                    self.add_new_transaction(transaction)

    def remove_approved_incomplete_transactions(self, block):
        if self.incomplete_transactions:
            for transaction in self.incomplete_transactions:
                if transaction in block['transactions']:
                    self.incomplete_transactions.remove(transaction)

