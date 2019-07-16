"""
using Anaconda for virtual enviornment  "pycoin"
This is the file in which we have imported all of the classes and then we are working on it 
use case = "Major use"
made: 14/5
no_of updated = 97
last_update: 18/6


"""


from functools import reduce
import hashlib as hl

import json
#not majorly using this pickle but still addded
#picle will make file with extension .p which cant be readed
import pickle
import requests
#this package is used to have url connections inside this python code

# Import two functions from our hash_util.py file. Omit the ".py" in the import
from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet

# The reward we give to miners (for creating a new block)
MINING_REWARD = 10

print(__name__)


class Blockchain:
    """The Blockchain class manages the chain of blocks as well as open transactions and the node on which it's running.

    Attributes:
        :chain: The list of blocks
        :open_transactions (private): The list of open transactions
        :hosting_node: The connected node (which runs the blockchain).
    """

    def __init__(self, public_key, node_id):
        """The constructor of the Blockchain class."""
        # Our starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Initializing our (empty) blockchain list
        self.chain = [genesis_block]
        # Unhandled transactions
        self.__open_transactions = []
        self.public_key = public_key
        self.__peer_nodes = set()
        self.node_id = node_id
        self.resolve_conflicts = False
        #always call load data after the nodes are initialized or else it will detete existing nodes
        self.load_data()

    # This turns the chain attribute into a property with a getter (the method below) and a setter (@chain.setter)
    @property
    def chain(self):
        return self.__chain[:]

    # The setter for the chain property
    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        """Returns a copy of the open transactions list."""
        return self.__open_transactions[:]

    def load_data(self):
        """Initialize blockchain + open transactions data from a file."""
        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                # We need to convert  the loaded data because Transactions should use OrderedDict
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1][:-1])
                # We need to convert  the loaded data because Transactions should use OrderedDict
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
            pass
        finally:
            print('Cleanup!')

    def save_data(self):
        """Save blockchain + open transactions snapshot to a file."""
        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [
                    tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed!')

    def proof_of_work(self):
        """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        # Try different PoW numbers and return the first valid one
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self, sender=None):
        """Calculate and return the balance for a participant.
        """
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
        # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
        # This fetches sent amounts of transactions that were already included in blocks of the blockchain
        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == participant] for block in self.__chain]
        # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
        # This fetches sent amounts of open transactions (to avoid double spending)
        open_tx_sender = [tx.amount
                          for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        print(tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                             if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
        # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant] for block in self.__chain]
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                                 if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        # Return the total balance
        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    # This function accepts two arguments.
    # One required one (transaction_amount) and one optional one (last_transaction)
    # The optional one is optional because it has a default value => [1]

    def add_transaction(self, recipient, sender, signature, amount=1.0, is_receiving=False):
        """ Append a new value as well as the last blockchain value to the blockchain.

        Arguments:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins.
            :amount: The amount of coins sent with the transaction (default = 1.0)
        """
        # transaction = {
        #     'sender': sender,
        #     'recipient': recipient,
        #     'amount': amount
        # }
        # if self.public_key == None:
        #     return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = 'http://{}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json={
                                                 'sender': sender, 'recipient': recipient, 'amount': amount, 'signature': signature})
                        if response.status_code == 400 or response.status_code == 500:
                            print('Transaction declined, needs resolving')
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False

    def mine_block(self):
        """Create a new block and add open transactions to it."""
        # Fetch the currently last block of the blockchain
        if self.public_key == None:
            return None
        last_block = self.__chain[-1]
        # Hash the last block (=> to be able to compare it to the stored hash value)
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        # Miners should be rewarded, so let's create a reward transaction
        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }
        reward_transaction = Transaction(
            'MINING', self.public_key, '', MINING_REWARD)
        # Copy transaction instead of manipulating the original open_transactions list
        # This ensures that if for some reason the mining should fail, we don't have the reward transaction stored in the open transactions
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        for node in self.__peer_nodes:
            url = 'http://{}/broadcast-block'.format(node)
            converted_block = block.__dict__.copy()
            converted_block['transactions'] = [
                tx.__dict__ for tx in converted_block['transactions']]
            try:
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declined, needs resolving')
                if response.status_code == 409:
                    self.resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                continue
        return block

    def add_block(self, block):
        """Add a block which was received via broadcasting to the local blockchain."""
        # Create a list of transaction objects
        transactions = [Transaction(
            tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
        # Validate the proof of work of the block and store the result (True or False) in a variable
        proof_is_valid = Verification.valid_proof(
            transactions[:-1], block['previous_hash'], block['proof'])
        # Check if previous_hash stored in the block is equal to the local blockchain's last block's hash and store the result in a block
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False
        # Create a Block object
        converted_block = Block(
            block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp'])
        self.__chain.append(converted_block)
        stored_transactions = self.__open_transactions[:]
        # Check which open transactions were included in the received block and remove them
        # This could be improved by giving each transaction an ID that would uniquely identify it
        for itx in block['transactions']:
            for opentx in stored_transactions:
                if opentx.sender == itx['sender'] and opentx.recipient == itx['recipient'] and opentx.amount == itx['amount'] and opentx.signature == itx['signature']:
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print('Item was already removed')
        self.save_data()
        return True

    def resolve(self):
        """Checks all peer nodes' blockchains and replaces the local one with longer valid ones."""
        # Initialize the winner chain with the local chain
        winner_chain = self.chain
        replace = False
        for node in self.__peer_nodes:
            url = 'http://{}/chain'.format(node)
            try:
                # Send a request and store the response
                response = requests.get(url)
                # Retrieve the JSON data as a dictionary
                node_chain = response.json()
                # Convert the dictionary list to a list of block AND transaction objects
                node_chain = [Block(block['index'], block['previous_hash'], [Transaction(
                    tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']],
                                    block['proof'], block['timestamp']) for block in node_chain]
                node_chain_length = len(node_chain)
                local_chain_length = len(winner_chain)
                # Store the received chain as the current winner chain if it's longer AND valid
                if node_chain_length > local_chain_length and Verification.verify_chain(node_chain):
                    winner_chain = node_chain
                    replace = True
            except requests.exceptions.ConnectionError:
                continue
        self.resolve_conflicts = False
        # Replace the local chain with the winner chain
        self.chain = winner_chain
        if replace:
            self.__open_transactions = []
        self.save_data()
        return replace

    def add_peer_node(self, node):
        """Adds a new node to the peer node set.

        Arguments:
            :node: The node URL which should be added.
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """Removes a node from the peer node set.

        Arguments:
            :node: The node URL which should be removed.
        """
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        """Return a list of all connected peer nodes."""
        #returning a copy of the peer node
        # return self.__peer_nodes[:]
        #as if the set method is not scriptable this will bump into an error
        return list(self.__peer_nodes)
        #since we are returning the list this will already make a copy.




















# #in all of the blockchain there is problem of initial stage because when we call last block the case occurs when
# #we dont have any block in the chain then it is one of the major problems hence we are using a dummy genesis_block
# #as the first block


# # #our starting block for the blockchain
# # genesis_block = {
# #         'previous_hash': '',
# #         'index' : 0,
# #         'transactions' : [],
# #         'proof' : 100
# #     }

# #initializing our empty blockchian
# #blockchain = [genesis_block]

# blockchain = []

# #unhandled transactions
# open_transactions = []

# #well we are going to pass owner from the node to have a specific identification id's
# owner = 'Dhruv'
# # participant = {'Dhruv'} 



# def load_data(): 
#     global blockchain
#     global open_transactions
#     try:
#         with open('blockchain.txt', mode = 'r') as f:
#             file_content = f.readlines()
#             blockchain = json.loads(file_content[0][:-1])
#             updated_blockchain = []
#             for block in blockchain:
#                 convertex_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
#                 updated_block = Block(block['index'], block['previous_hash'], convertex_tx, block['proof'], block['timestamp'])#calling here
#                 # updated_block = {
#                 #     'previous_hash': block['previous_hash'],
#                 #     'index': block['index'],
#                 #     'proof': block['proof'],
#                 #     'transactions': [OrderedDict(
#                 #         [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount' ,tx['amount'])]) for tx in block['transactions']]
#                 # }
#                 updated_blockchain.append(updated_block)
#             blockchain = updated_blockchain
#             open_transactions = json.loads(file_content[1])

#             updated_transactions = []
#             for tx in open_transactions:
#                 updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
#                 # updated_transaction = OrderedDict(
#                 #         [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount' ,tx['amount'])])
#                 updated_transactions.append(updated_transaction)
#             open_transactions = updated_transactions
#     #this is only going to trigger when we don't had made blockchain.txt file
#     #due to try except block it is sure that the code is wrong still this will not crash
#     except IOError:
#         genesis_block = Block(0, '', [], 100, 0)        
#         # genesis_block = {
#         # 'previous_hash': '',
#         # 'index' : 0,
#         # 'transactions' : [],
#         # 'proof' : 100
#         # }
#         blockchain = [genesis_block]
#         open_transactions = []

#     finally:
#         print('cleanup!')


# def load_data(): 
#     with open('blockchain.p', mode = 'rb') as f:
#         file_content = pickle.loads(f.read())
#         global blockchain
#         global open_transactions        
#         blockchain = file_content['chain']
#         open_transactions = file_content['ot']
#         print(file_content)





# load_data()






# def save_data():
#     try:
#         with open('blockchain.txt', mode = 'w') as f:
#             saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in blockchain]]
#             f.write(json.dumps(saveable_chain))
#             f.write('\n')
#             saveable_tx = [tx.__dict__ for tx in open_transactions]
#             f.write(json.dumps(saveable_tx))
#     except (IOError, IndexError):
#         print('saving failed!!')

 

                #old dumping code
# def save_data():
#     with open('blockchain.p', mode = 'wb') as f:
#         save_data = {
#             'chain': blockchain,
#             'ot': open_transactions
#         }
#         f.write(pickle.dumps(save_data))




                    #moved to the class here for backup code if needed
# def get_balance(participant):
#     #using nested list comprehension with two for loops like work
#     tx_sender = [[tx.amount for tx in block.transactions
#                     if tx.sender == participant] for block in blockchain]
#     open_tx_sender = [tx.amount for tx in open_transactions
#                      if tx.sender == participant]
#     tx_sender.append(open_tx_sender)
#     amount_sent = reduce(lambda tx_sum ,tx_amt : tx_sum + sum(tx_amt) if len(tx_amt)>0 else tx_sum + 0, tx_sender, 0)
#     #we implemented that funtion with the help of the lambad and inline arguments
#     #we can't use ternary operations with lambda functions
#     '''
#     amount_sent = 0
#     for tx in tx_sender:
#         #to remove the error generated due to first empty block
#         if len(tx) > 0:
#             amount_sent += sum(tx)
#     '''
#     tx_recipient = [[tx.amount for tx in block.transactions
#                      if tx.recipient == participant] for block in blockchain]
#     amount_received = reduce(lambda tx_sum ,tx_amt : tx_sum + sum(tx_amt) if len(tx_amt)>0 else tx_sum + 0, tx_recipient, 0)
#     '''
#     amount_received = 0
#     for tx in tx_recipient:
#         #to remove the error generated due to first empty block
#         if len(tx) > 0:
#             amount_received += sum(tx[])
#     '''
#     return amount_received - amount_sent




                    #this is also moved to blockchain class to have better utility of the code
# #this function is made to send the last element of the blockchain hence in the case when whe have 
# # an empty blockchain we will pass the null value else what we had done continues 
# def get_last_blockchain_value():
#     if len(blockchain) < 1:
#         return None 
#         #none is usefull to show tha there is nothing
    
#     return blockchain[-1]
#     # here indexing value -1 will refer to the last element of the list



# def verify_transaction(transaction):
#     sender_balance = get_balance(transaction.sender)
#     return sender_balance >= transaction.amount
#     #this will ruturn the value in true or false(boolean )






'''
def add_transaction(transaction_amount, last_transaction=[1]):
    #this is making our our blocks to be in chain

    if last_transaction == None:
        last_transaction = [1]
        #with this code we are giving all of the blockchain first block as one !!
        #anycase first element of the block will be 1
    blockchain.append([last_transaction, transaction_amount])
'''

                    #this is also been moved to the blockchain class
# def add_transaction(recipient, sender = owner,amount = 1.0):
#     #sender : the sender of the coins
#     #recipient : the recipient of the coin
#     #amount : the amount of soin send from sender to recipient and the default is set to be 1.0

#     #this is unodered dictonary
#     #making dictionary
#     # transaction = {
#     #     'sender' : sender,
#     #     'recipient' : recipient,
#     #     'amount' : amount
#     # }

#     transaction = Transaction(sender, recipient, amount)
#     # transaction = OrderedDict(
#     #     [('sender', sender), ('recipient', recipient), ('amount' ,amount)])



#     #if the verify chain value will be true then and only then the transaction will be validated
    
#     verifier = Verification()
#     if verifier.verify_transaction(transaction, get_balance):
#         open_transactions.append(transaction)
#         #participant is set hence it will only allow us to enter the unique value 
#         #if any kind of duplicate value comes then it will simply ignore it
#         # participant.add(sender)
#         # participant.add(recipient)
#         save_data()
#         return True

#     return False
    

# def valid_proof(transactions, last_hash, proof):
#     guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
#     # print(guess)
#     guess_hash = hash_string_256(guess)
#     # print(guess_hash)
#     #returning only first and the second element
#     return guess_hash[0:2] == '00'


                #added to the blockchain class
# def proof_of_work():
#     last_block = blockchain[-1]
#     last_hash = hash_block(last_block)
#     proof = 0
#     verifier = Verification()
#     while not verifier.valid_proof(open_transactions ,last_hash, proof):
#         proof += 1
#     return proof

'''
#this is also true but we can do it very easily
add_value(2,[1])
add_value(0.9,get_last_blockchain_value())
add_value(10.80,get_last_blockchain_value())
add_value(5,get_last_blockchain_value())
'''

# def mine_block():
#     last_block = blockchain[-1]
#     #can use it like this instead of for loop
#     #this will work but let do it which looks better known as "list comprehensions"
#     #hashed_block = str([ last_block[key] for key in last_block ])
#     #hashed_block = '-'.join([str(last_block[key]) for key in last_block])
    
#     hashed_block = hash_block(last_block)
#     # #gives us last element of blockchain
#     # for key in last_block:
#     #     values = last_block[key]
#     #     hashed_block = hashed_block + str(values)
#     proof = proof_of_work()
#     #rewarding the miner who is responsible to validate the transactiona
#     '''
#     reward_transaction = {
#         'sender' : 'MINING',
#         'recipient' : owner,
#         'amount' : MINING_REWARD
#     }
#     '''
#     reward_transaction = Transaction('MINING', owner, MINING_REWARD)
#     # reward_transaction = OrderedDict(
#     #     [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
#     #we are doing this whole thing because what if the sender do have balance heile we authenticate the transactiona
#     #and soon after the balance is less then our chain would be wrong
#     '''
#     well here we need to make a copy of all of the open_transaction hence we had done this
#      now this cant be done directly because python don't support whole copying by call by value
#      hence we need to use call by reference to achive this copy
#      so we are using range validator [:]
#      the blank space before and after indicated that the range is infinity and copy the whole list 
#     '''
#     copied_transactions = open_transactions[:]
#     copied_transactions.append(reward_transaction)
#     block = Block(len(blockchain), hashed_block, copied_transactions, proof)
#     # block = {
#     #     'previous_hash': hashed_block ,
#     #     'index' : len(blockchain),
#     #     'transactions' : copied_transactions,
#     #     'proof' : proof
#     # }
#     blockchain.append(block)
#     return True





'''
this whole code is just mess!!

#now what if we take transaction amount from the user to create next block of the blockchain
tx_amount = float(input('Please Enter Your Transaction amount: '))
add_value(tx_amount)
tx_amount = float(input('Please Enter Your Transaction amount: '))
add_value(tx_amount,get_last_blockchain_value())
tx_amount = float(input('Please Enter Your Transaction amount: '))
add_value(tx_amount,get_last_blockchain_value())
tx_amount = float(input('Please Enter Your Transaction amount: '))
add_value(tx_amount,get_last_blockchain_value())
#well we can also chage teh order of transaction_amount and last_transaction by initializing them here also
tx_amount = float(input('Please Enter Your Transaction amount: '))
add_value(last_transaction=get_last_blockchain_value(),transaction_amount=tx_amount)
#this is perfectly working! but here we can not use user enterd values

'''

# lets define single function which will take input from the user each time to neglate this heavy code
# this could be also done by looping

# def get_transaction_value():
#     """
#         returnns the value of transaction amount and sender and recipient details
#     """
#     #well we are making this blochain on our own system hence we don't need sender bucause we are the only sender in this blockhain system
#     tx_recipient = input("Enter the recipient of the transaction : ")
#     tx_amount = float(input("Enter The amount here Please : "))
#     return tx_recipient , tx_amount


# def get_user_choice():
#     #prompts the user input page or we can say it a menu 
#     tx_amount = input("Enter The Choice : ")
#     return tx_amount


# def print_blockchain_elements():
#     #console output of blockchain with help of loops
#     for block in blockchain:
#         print('Outputing Blocks Here')
#         print(block)    
#     else:
#         print('-' * 20)
'''
def verify_chain():
    block_index = 0
    is_valid = True
    for block in blockchain:
        #now here if there is case for first block then we cant have any block before it hence we will just increment it by one 
        #because always first block in the chain could be anything of anykind
        if block_index == 0:
            block_index += 1#blockindex = blockindex + 1
            continue
        elif block[0] == blockchain[block_index -1]:     #checking that thae current block of the chain do have te elements of the previous block 
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid
'''


# def verify_chain():
#     is_valid = True
#     #here the range would start from 0 and go to len(blockchain-1) this is the major objective of the range in python
#     for block_index in range(len(blockchain)):
#         if block_index == 0:
#             continue
#         elif blockchain[block_index][0] == blockchain[block_index - 1]:
#             is_valid = True
#         else:
#             is_valid = False
#             break
#     return is_valid



# def verify_chain():
#     """ Verify that the current blockchain is totally valid and if false then it will show us a message
#         here in this new function we are checking the hash of the last block with newly generated hash value if 
#         they differs then they are returning false or else they will return value as true
#         what if we manupulate both of them ??
#         then the previous to previous block will find an error 
#         this is the chaining process    
    
#     """
#     #this enumerate function will give us the tuple which contains indexes of the blockchian list and the data of the liist too
#     for (index, block) in enumerate(blockchain):
#         if index == 0:#need to remove genesis block
#             continue
#         if block.previous_hash != hash_block(blockchain[index - 1]):
#             return False
#         if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
#             print('proof of work is invalid')
#             return False
#     return True


'''
def verify_transactions():
    is_valid = True
    for tx in open_transactions:
        if verify_transaction(tx) == True:
            is_valid = True
        else:
            is_valid = False
    return is_valid    
'''

'''
#this is very lengthy code lets make it small
def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])
    #this will check the whole list is true or not if any of them is false then it is false for all of them
'''


# #getting the first transaction amount from the user
# tx_amount = get_transaction_value()
# add_value(tx_amount)
'''
#getting the second transaction amount from the user
tx_amount = get_tx_amount()
add_value(tx_amount, get_last_blockchain_value())
#getting the third transaction amount from the user
tx_amount = get_tx_amount()
add_value(tx_amount, get_last_blockchain_value())
'''

'''
#lets use loop to ask user multple time to run this blockchain 
x='y'#reson: because we want to say compiler that x is string variable instead of integer or float
while (x !='n'):
    tx_amount = get_tx_amount()
    add_value(tx_amount, get_last_blockchain_value())
    #now all the blocks printing each time the user enters the value
    for block in blockchain:
        print('Outputing Blocks Here')
        print(block)
    x=input("Do you want to continue y/n?")
'''

#
#
#please note this whole part is modved to node part
#total user interaction is moved from here
#
#

# waiting_for_input = True

# while waiting_for_input:
#     print()
#     print("Please Choose!")
#     print("1.Add a new transaction")
#     print("2.Mine a new block")
#     print("3.Output the all blockchainn Blocks.")
#     # print("4.Output all participant")
#     print("4.Check transaction Validity")
#     # print("6.Manipulate/Hack the Blockchain")
#     print("e.Exit")
#     print()
#     user_choice = get_user_choice()

#     if user_choice == '1':
#         tx_data = get_transaction_value()
#         recipient, amount = tx_data
#         #this will pull out the first emement of touple and save it in recipient and second element on amount
#         if add_transaction(recipient, amount=amount):
#             print('Transaction Added')
#         else:
#             print('Transaction Failed')
#         #here we are skipping the second argument which is sender
#         print(open_transactions)
    
#     elif user_choice == '2':
#         if mine_block():
#             open_transactions = []
#             save_data()
    
#     elif user_choice == '3':
#         print_blockchain_elements()

#     # elif user_choice == '4':
#     #     print(participant)

#     elif user_choice == '4':
#         verifier = Verification()
#         if verifier.verify_transactions(open_transactions,get_balance) == True:
#             print("All transactions are valid")
#         else:
#             print("There are invalid transaction")


#     # elif user_choice == '6':
#     #     #if user wants to manipulate the chain then we are just changing the first block which is 
#     #     #[1] in any case to [2]
#     #     if len(blockchain) >= 1 :
#     #         blockchain[0] = {
#     #             'previous_hash': '',
#     #             'index' : 0,
#     #             'transactions' : [{'sender': 'Dhruv', 'recipient': 'Tejas','amount': 100.0}]
#     #         }
#     #     #by manupulating this kind just one block our whole blockchain becomes invalid 
#     #     #this invalid blockchain will be detected by function verify_chain
    
#     elif user_choice == 'e':
#         #break
#         #insted of break we can do it like this also
#         waiting_for_input = False
#     else:
#         print("Seems Like Wrong Input Please try Again!!")
    
#     #if the returning value is not True then we are breaking the while loop
#     verifier = Verification()
#     if not verifier.verify_chain(blockchain):
#         print_blockchain_elements()
#         print('Invalid Blockchian')
#         break 
#     '''
#     #this is really very bad condered to user experience
#     print(get_balance('Dhruv'))
#     '''
#     print('Balance of {}: {:6.2f}'.format('Dhruv',get_balance('Dhruv')))
#     #here this :6.2f suggests teh range of the balance which means maximum 6 digits and 2 decials

# # while loop in python is giving facility to have else like if-else statemments 
# #this will only execuited when we left out from the loop
# else:
#     print('User Left!')



# '''
# #printing the whole blockchain in one line
# print(blockchain)
# '''

# #console output of blockchain with help of loops
# # for block in blockchain:
# #     print('Outputing Blocks Here')
# #     print(block)

# print("Done")
# # print(open_transactions)
