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

def get_transaction_value():
    user_input = float(input("Enter The Ammount here Please :"))
    return user_input


def get_user_choice():
    user_input = input("Enter The Choice")
    return user_input


def print_blockchain_elements():
    #console output of blockchain with help of loops
    for block in blockchain:
        print('Outputing Blocks Here')
        print(block)    


#getting the first transaction ammount from the user
tx_ammount = get_transaction_value()
add_value(tx_ammount)
'''
#getting the second transaction ammount from the user
tx_ammount = get_user_input()
add_value(tx_ammount, get_last_blockchain_value())
#getting the third transaction ammount from the user
tx_ammount = get_user_input()
add_value(tx_ammount, get_last_blockchain_value())
'''

'''
#lets use loop to ask user multple time to run this blockchain 
x='y'#reson: because we want to say compiler that x is string variable instead of integer or float
while (x !='n'):
    tx_ammount = get_user_input()
    add_value(tx_ammount, get_last_blockchain_value())
    #now all the blocks printing each time the user enters the value
    for block in blockchain:
        print('Outputing Blocks Here')
        print(block)
    x=input("Do you want to continue y/n?")
'''

while True:
    print()
    print("Please Choose!")
    print("1.Add a new transaction")
    print("2.Output the all blockchainn Blocks.")
    print("3.Exit")
    print()
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_ammount = get_transaction_value()
        add_value(tx_ammount, get_last_blockchain_value())

    elif user_choice == '2':
        print_blockchain_elements()
    
    elif user_choice == '3  ':
        break
    
    else:
        print("Seems Like Wrong Input Please try Again!!")




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