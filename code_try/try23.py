
'''
well in this code we have used picle file formating to save the data on the local systems
instead of jason files we used picle file system becuase the picle file systems saves data in binary 
format and due to this the manipulation of the data of the blockchain becomes difficult
and picle is near to python object hence it will also reduce the complexity of the code
'''



'''here the code and program is same as bchai try copy 1
but we arent giving the first element directly into list instesd 
we are adding last_transaction in add_value to have more better versatility of the code
now here we can give last_tansaction a kind of default value which is [1]
'''



# import functools
#here we are ponly using reduce from functools so
from functools import reduce
import hashlib
#this is used to calculate hash of sha256
import json
#used to convert dictonaty to string
from collections import OrderedDict
#well we used this to improve our hashing capablities
import pickle

#importing our own functions from different file
from hash_util import hash_string_256,hash_block





#giving 10 coins free for each miner
MINING_REWARD = 10

#in all of the blockchain there is problem of initial stage because when we call last block the case occurs when
#we dont have any block in the chain then it is one of the major problems hence we are using a dummy genesis_block
#as the first block

genesis_block = {
        'previous_hash': '',
        'index' : 0,
        'transactions' : [],
        'proof' : 100
    }
blockchain = [genesis_block]
open_transactions = []
owner = 'Dhruv'
participant = {'Dhruv'} 



# def load_data(): 
#     with open('blockchain.txt', mode = 'r') as f:
#         file_content = f.readlines()
#         global blockchain
#         global open_transactions
#         blockchain = json.loads(file_content[0][:-1])
#         updated_blockchain = []
#         for block in blockchain:
#             updated_block = {
#                 'previous_hash': block['previous_hash'],
#                 'index': block['index'],
#                 'proof': block['proof'],
#                 'transactions': [OrderedDict(
#                     [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount' ,tx['amount'])]) for tx in block['transactions']]
#             }
#             updated_blockchain.append(updated_block)
#         blockchain = updated_blockchain
#         open_transactions = json.loads(file_content[1])
#         updated_transactions = []
#         for tx in open_transactions:
#             updated_transaction = OrderedDict(
#                     [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount' ,tx['amount'])])
#             updated_transactions.append(updated_transaction)
#         open_transactions = updated_transactions


def load_data(): 
    with open('blockchain.p', mode = 'rb') as f:
        file_content = pickle.loads(f.read())
        global blockchain
        global open_transactions        
        blockchain = file_content['chain']
        open_transactions = file_content['ot']
        print(file_content)



load_data()


# def save_data():
#     with open('blockchain.txt', mode = 'w') as f:
#         f.write(json.dumps(blockchain))
#         f.write('\n')
#         f.write(json.dumps(open_transactions))
 
def save_data():
    with open('blockchain.p', mode = 'wb') as f:
        save_data = {
            'chain': blockchain,
            'ot': open_transactions
        }
        f.write(pickle.dumps(save_data))





def get_balance(participant):
    #using nested list comprehension with two for loops like work
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum ,tx_amt : tx_sum + sum(tx_amt) if len(tx_amt)>0 else tx_sum + 0, tx_sender, 0)
    #we implemented that funtion with the help of the lambad and inline arguments
    #we can't use ternary operations with lambda functions
    '''
    amount_sent = 0
    for tx in tx_sender:
        #to remove the error generated due to first empty block
        if len(tx) > 0:
            amount_sent += sum(tx)
    '''
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum ,tx_amt : tx_sum + sum(tx_amt) if len(tx_amt)>0 else tx_sum + 0, tx_recipient, 0)
    '''
    amount_received = 0
    for tx in tx_recipient:
        #to remove the error generated due to first empty block
        if len(tx) > 0:
            amount_received += sum(tx[])
    '''
    return amount_received - amount_sent





#this function is made to send the last element of the blockchain hence in the case when whe have 
# an empty blockchain we will pass the null value else what we had done continues 
def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None 
        #none is usefull to show tha there is nothing
    
    return blockchain[-1]
    # here indexing value -1 will refer to the last element of the list



def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']
    #this will ruturn the value in true or false(boolean )






'''
def add_transaction(transaction_amount, last_transaction=[1]):
    #this is making our our blocks to be in chain

    if last_transaction == None:
        last_transaction = [1]
        #with this code we are giving all of the blockchain first block as one !!
        #anycase first element of the block will be 1
    blockchain.append([last_transaction, transaction_amount])
'''
def add_transaction(recipient, sender = owner,amount = 1.0):
    #sender : the sender of the coins
    #recipient : the recipient of the coin
    #amount : the amount of soin send from sender to recipient and the default is set to be 1.0

    #this is unodered dictonary
    #making dictionary
    # transaction = {
    #     'sender' : sender,
    #     'recipient' : recipient,
    #     'amount' : amount
    # }

    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount' ,amount)])



    #if the verify chain value will be true then and only then the transaction will be validated
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        #participant is set hence it will only allow us to enter the unique value 
        #if any kind of duplicate value comes then it will simply ignore it
        participant.add(sender)
        participant.add(recipient)
        save_data()
        return True

    return False


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    print(guess)
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    #returning only first and the second element
    return guess_hash[0:2] == '00'

def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions ,last_hash, proof):
        proof += 1
    return proof

'''
#this is also true but we can do it very easily
add_value(2,[1])
add_value(0.9,get_last_blockchain_value())
add_value(10.80,get_last_blockchain_value())
add_value(5,get_last_blockchain_value())
'''

def mine_block():
    last_block = blockchain[-1]
    #can use it like this instead of for loop
    #this will work but let do it which looks better known as "list comprehensions"
    #hashed_block = str([ last_block[key] for key in last_block ])
    #hashed_block = '-'.join([str(last_block[key]) for key in last_block])
    
    hashed_block = hash_block(last_block)
    # #gives us last element of blockchain
    # for key in last_block:
    #     values = last_block[key]
    #     hashed_block = hashed_block + str(values)
    proof = proof_of_work()
    #rewarding the miner who is responsible to validate the transactiona
    '''
    reward_transaction = {
        'sender' : 'MINING',
        'recipient' : owner,
        'amount' : MINING_REWARD
    }
    '''
    reward_transaction = OrderedDict(
        [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
    #we are doing this whole thing because what if the sender do have balance heile we authenticate the transactiona
    #and soon after the balance is less then our chain would be wrong
    '''
    well here we need to make a copy of all of the open_transaction hence we had done this
     now this cant be done directly because python don't support whole copying by call by value
     hence we need to use call by reference to achive this copy
     so we are using range validator [:]
     the blank space before and after indicated that the range is infinity and copy the whole list 
    '''
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block ,
        'index' : len(blockchain),
        'transactions' : copied_transactions,
        'proof' : proof
    }
    blockchain.append(block)
    return True





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

def get_transaction_value():
    """
        returnns the value of transaction amount and sender and recipient details
    """
    #well we are making this blochain on our own system hence we don't need sender bucause we are the only sender in this blockhain system
    tx_recipient = input("Enter the recipient of the transaction : ")
    tx_amount = float(input("Enter The amount here Please : "))
    return tx_recipient , tx_amount


def get_user_choice():
    tx_amount = input("Enter The Choice : ")
    return tx_amount


def print_blockchain_elements():
    #console output of blockchain with help of loops
    for block in blockchain:
        print('Outputing Blocks Here')
        print(block)    
    else:
        print('-' * 20)
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

def verify_chain():
    """ Verify that the current blockchain is totally valid and if false then it will show us a message
        here in this new function we are checking the hash of the last block with newly generated hash value if 
        they differs then they are returning false or else they will return value as true
        what if we manupulate both of them ??
        then the previous to previous block will find an error 
        this is the chaining process    
    
    """
    #this enumerate function will give us the tuple which contains indexes of the blockchian list and the data of the liist too
    for (index, block) in enumerate(blockchain):
        if index == 0:#need to remove genesis block
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('proof of work is invalid')
            return False
    return True


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
#this is very lengthy code lets make it small
def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])
    #this will check the whole list is true or not if any of them is false then it is false for all of them



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



waiting_for_input = True

while waiting_for_input:
    print()
    print("Please Choose!")
    print("1.Add a new transaction")
    print("2.Mine a new block")
    print("3.Output the all blockchainn Blocks.")
    print("4.Output all participant")
    print("5.Check transaction Validity")
    print("6.Manipulate/Hack the Blockchain")
    print("e.Exit")
    print()
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        #this will pull out the first emement of touple and save it in recipient and second element on amount
        if add_transaction(recipient, amount=amount):
            print('Transaction Added')
        else:
            print('Transaction Failed')
        #here we are skipping the second argument which is sender
        print(open_transactions)
    
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()
    
    elif user_choice == '3':
        print_blockchain_elements()

    elif user_choice == '4':
        print(participant)

    elif user_choice == '5':
        if verify_transactions == True:
            print("All transactions are valid")
        else:
            print("There are invalid transaction")


    elif user_choice == '6':
        #if user wants to manipulate the chain then we are just changing the first block which is 
        #[1] in any case to [2]
        if len(blockchain) >= 1 :
            blockchain[0] = {
                'previous_hash': '',
                'index' : 0,
                'transactions' : [{'sender': 'Dhruv', 'recipient': 'Tejas','amount': 100.0}]
            }
        #by manupulating this kind just one block our whole blockchain becomes invalid 
        #this invalid blockchain will be detected by function verify_chain
    
    elif user_choice == 'e':
        #break
        #insted of break we can do it like this also
        waiting_for_input = False
    else:
        print("Seems Like Wrong Input Please try Again!!")
    
    #if the returning value is not True then we are breaking the while loop
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid Blockchian')
        break 
    '''
    #this is really very bad condered to user experience
    print(get_balance('Dhruv'))
    '''
    print('Balance of {}: {:6.2f}'.format('Dhruv',get_balance('Dhruv')))
    #here this :6.2f suggests teh range of the balance which means maximum 6 digits and 2 decials

# while loop in python is giving facility to have else like if-else statemments 
#this will only execuited when we left out from the loop
else:
    print('User Left!')



'''
#printing the whole blockchain in one line
print(blockchain)
'''

#console output of blockchain with help of loops
# for block in blockchain:
#     print('Outputing Blocks Here')
#     print(block)

print("Done")
# print(open_transactions)