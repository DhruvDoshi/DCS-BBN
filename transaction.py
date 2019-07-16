'''
this file includes and operates the functionality of the transaction and we are importing
printable file from utility 

use case = "Major use"
made: 22/5
no_of updated = 17
last_update: 19/6


'''


from collections import OrderedDict

from utility.printable import Printable

class Transaction(Printable):
    """A transaction which can be added to a block in the blockchain.

    Attributes:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :signature: The signature of the transaction.
        :amount: The amount of coins sent.
    """
    def __init__(self, sender, recipient, signature, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_ordered_dict(self):
        """Converts this transaction into a (hashable) OrderedDict."""
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])
