import hashlib
import json



class NodeBlockchain:
    def __init__(self):
        self.chain=[]
        self.incomplete_transactions = []
        self.unsolved_block = {}

    def create_unsolved_block(self, previous_hash):
        self.unsolved_block = {
            'index': len(self.chain)+1,
            'transactions': self.incomplete_transactions,
            'previous_hash': previous_hash,
            'block generator': self.id
        }

    def add_new_block(self):
        self.chain.append(self.unsolved_block)

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
        self.incomplete_transactions.append(transaction)

    def broadcast_transactions(self, other_node):
        if other_node.incomplete_transactions:
            for transaction in other_node.incomplete_transactions:
                if transaction not in self.incomplete_transactions:
                    self.new_transaction(transaction)


    def resolve_conflict(self, other_node):
        if self.incomplete_transactions:
            for transaction in self.incomplete_transactions:
                if transaction in block['transactions']:
                    self.incomplete_transactions.remove(transaction)