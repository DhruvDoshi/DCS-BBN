blockchain = [[1]]
#using list inside list to hold multiple values

def get_last_blockchain_value():
    return blockchain[-1]
    #here indexing value -1 will refer to the last element of the list 



def add_value(transaction_amount):
    blockchain.append([get_last_blockchain_value(),transaction_amount])
     

add_value(2)
add_value(0.9)
add_value(10.80)
add_value(5)
print(blockchain)

