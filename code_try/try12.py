'''here the code and program is same as bchai try copy 1
but we arent giving the first element directly into list instesd 
we are adding last_transaction in add_value to have more better versatility of the code
now here we can give last_tansaction a kind of default value which is [1]
'''

#in all of the blockchain there is problem of initial stage because when we call last block the case occurs when
#we dont have any block in the chain then it is one of the major problems hence we are using a dummy genesis_block
#as the first block
genesis_block = {
        'previous_hash': '',
        'index' : 0,
        'transactions' : []
    }
blockchain = [genesis_block]
open_transactions = []
owner = 'Dhruv' 

#this function is made to send the last element of the blockchain hence in the case when whe have 
# an empty blockchain we will pass the null value else what we had done continues 
def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None 
        #none is usefull to show tha there is nothing
    
    return blockchain[-1]
    # here indexing value -1 will refer to the last element of the list



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

    #making dictionary
    transaction = {'sender' : sender,
    'recipient' : recipient,
    'amount' : amount }
    open_transactions.append(transaction)



'''
#this is also true but we can do it very easily
add_value(2,[1])
add_value(0.9,get_last_blockchain_value())
add_value(10.80,get_last_blockchain_value())
add_value(5,get_last_blockchain_value())
'''

def mine_block():
    last_block = blockchain[-1]
    hashed_block = ''
    #gives us last element of blockchain
    for keys in last_block:
        values = last_block[keys]
        hashed_block = hashed_block + str(values)
    print(hashed_block)
    block = {
        'previous_hash': 'xyx' ,
        'index' : len(blockchain),
        'transactions' : open_transactions
    }
    blockchain.append(block)









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


def verify_chain():
    is_valid = True
    #here the range would start from 0 and go to len(blockchain-1) this is the major objective of the range in python
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
    return is_valid




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
    print("4.Manipulate the Blockchain")
    print("e.Exit")
    print()
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        #this will pull out the first emement of touple and save it in recipient and second element on amount
        add_transaction(recipient, amount=amount)
        #here we are skipping the second argument which is sender
        print(open_transactions)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
        print_blockchain_elements()

    elif user_choice == '4':
        #if user wants to manipulate the chain then we are just changing the first block which is 
        #[1] in any case to [2]
        if len(blockchain) >= 1 :
            blockchain[0] = [2]
        #by manupulating this kind just one block our whole blockchain becomes invalid 
        #this invalid blockchain will be detected by function verify_chain
    
    elif user_choice == 'e':
        #break
        #insted of break we can do it like this also
        waiting_for_input = False
    else:
        print("Seems Like Wrong Input Please try Again!!")
    
    # #if the returning value is not True then we are breaking the while loop
    # if not verify_chain():
    #     print_blockchain_elements()
    #     print('Invalid Blockchian')
    #     break 

# while loop in python is giving facility to have else like if-else statemments 
#this will only execuited when we left out from the loop
else:
    print('User Left!')



'''
#printing the whole blockchain in one line
print(blockchain)
'''
'''
#console output of blockchain with help of loops
for block in blockchain:
    print('Outputing Blocks Here')
    print(block)
'''
print("Done")