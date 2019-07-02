'''here the code and program is same as bchai try copy 1
but we arent giving the first element directly into list instesd 
we are adding last_transaction in add_value to have more better versatility of the code
now here we can give last_tansaction a kind of default value which is [1]
'''

blockchain = []


def get_last_blockchain_value():
    return blockchain[-1]
    # here indexing value -1 will refer to the last element of the list


def add_value(transaction_amount,last_transaction=[1]):
    blockchain.append([last_transaction, transaction_amount])

'''
#this is also true but we can do it very easily
add_value(2,[1])
add_value(0.9,get_last_blockchain_value())
add_value(10.80,get_last_blockchain_value())
add_value(5,get_last_blockchain_value())
'''


add_value(2)
add_value(0.9,get_last_blockchain_value())
add_value(10.80,get_last_blockchain_value())
add_value(5,get_last_blockchain_value())
#well we can also chage teh order of transaction_amount and last_transaction by initializing them here also
add_value(last_transaction=get_last_blockchain_value(),transaction_amount=15)
#this is perfectly working!



print(blockchain)

