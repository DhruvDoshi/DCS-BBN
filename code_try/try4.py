'''here the code and program is same as bchai try copy 1
but we arent giving the first element directly into list instesd 
we are adding last_transaction in add_value to have more better versatility of the code
now here we can give last_tansaction a kind of default value which is [1]
'''

blockchain = []


def get_last_blockchain_value():
    return blockchain[-1]
    # here indexing value -1 will refer to the last element of the list


def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([last_transaction, transaction_amount])


'''
#this is also true but we can do it very easily
add_value(2,[1])
add_value(0.9,get_last_blockchain_value())
add_value(10.80,get_last_blockchain_value())
add_value(5,get_last_blockchain_value())
'''

'''
this whole code is just mess!!

#now what if we take transaction ammount from the user to create next block of the blockchain
tx_ammount = float(input('Please Enter Your Transaction Ammount: '))
add_value(tx_ammount)
tx_ammount = float(input('Please Enter Your Transaction Ammount: '))
add_value(tx_ammount,get_last_blockchain_value())
tx_ammount = float(input('Please Enter Your Transaction Ammount: '))
add_value(tx_ammount,get_last_blockchain_value())
tx_ammount = float(input('Please Enter Your Transaction Ammount: '))
add_value(tx_ammount,get_last_blockchain_value())
#well we can also chage teh order of transaction_amount and last_transaction by initializing them here also
tx_ammount = float(input('Please Enter Your Transaction Ammount: '))
add_value(last_transaction=get_last_blockchain_value(),transaction_amount=tx_ammount)
#this is perfectly working! but here we can not use user enterd values

'''

# lets define single function which will take input from the user each time to neglate this heavy code
# this could be also done by looping

def get_user_input():
    return float(input("Enter The Ammount here Please :"))

#getting the first transaction ammount from the user
tx_ammount = get_user_input()
add_value(tx_ammount)
#getting the second transaction ammount from the user
tx_ammount = get_user_input()
add_value(tx_ammount, get_last_blockchain_value())
#getting the third transaction ammount from the user
tx_ammount = get_user_input()
add_value(tx_ammount, get_last_blockchain_value())

'''
#printing the whole blockchain in one line
print(blockchain)
'''

#console output of blockchain with help of loops
for block in blockchain:
    print('Outputing Blocks Here')
    print(block)

print("Done")