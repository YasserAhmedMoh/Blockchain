import json, time
from hashlib import sha256
import random
import datetime


####################  CLASS THAT DEFINES USERS OF THE COIN AND THE AMOUNT OF COINS  #################
class Node:
    #CONTAINS ALL THE USERS WITH THE THE AMOUNT OF COINS THEY HAVE   
    NodesDict = {}

    def __init__(self, id):
        #Initial Amount of any User = 500$
        self.amount=500
        self.id = id
        Node.NodesDict[id] = self.amount
       
    def GetAmount(self):
        return self.amount
    
    def PerformTransaction(id1, amount, id2):
        Node.NodesDict[id1] -= amount 
        Node.NodesDict[id2] += amount
    
    def printNodes():
        print(Node.NodesDict)


######################  CLASS THAT IS RESPONSIBLE FOR TRANSACTION BETWEEN USERS  #################
class Transaction:
    def __init__(self, id1, amount , id2):
        self.id1 = id1
        self.id2 = id2
        self.amount = amount
        self.transactionString = (id1 + " Pays " + id2 + " " + str(self.amount) + "$")

    def ValidateTransaction(self):
        #CAN ID1 PAY ID2 ?
        id1_Total = Node.NodesDict[self.id1] - self.amount
        if ( id1_Total < 0):
            print("INVALID TRANSACTION")
            return False  
        #ID1 pays 'amount' to ID2
        Node.PerformTransaction(self.id1, self.amount, self.id2)
        #Return True if transaction is correct
        return True


    def GetTransaction(self):
        return (self.transactionString)

######################  CLASS THAT REPRESENTS A SINGLE BLOCK IN THE BLOCK CHAIN  #################
class Block:

    def __init__(self, index, transactions , timestamp, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.data = []
        for transaction in transactions:
            self.data.append(transaction.GetTransaction())

    def compute_hash(self):
        #A function that returns the hash of the block contents.
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
    
    
    def print_block(self):
        print('Index:', self.index)
        print('data:', self.data)
        print('timestamp:', self.timestamp)
        print('previoshash:', self.previous_hash)
        print('nonce:', self.nonce)


######################  BLOCKCHAIN CLASS RESPONISIBLE FOR ADDING BLOCKS AND ETC. #################
class Blockchain:
     
     unconfirmed_transactions = []
     
     def __init__(self,difficulty):
        self.difficulty=difficulty
        # Creating First Block
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain = [genesis_block]
     
     def PrintChain(self):
         for block in self.chain:
             block.print_block()
     
     def last_block(self):
        return self.chain[-1]
     
     def proof_of_work(self,block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith( "0" * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
            block.hash=computed_hash  
        #print(computed_hash,block.nonce)
        return computed_hash
     
     def add_block(self, block, proof):
        previous_hash = self.last_block().compute_hash()
        block.hash = proof
        self.chain.append(block)
        return True
   
     def add_new_transaction(self, transaction):
         #appends new transaction to the list of all unconfirmed transactions
        self.unconfirmed_transactions.append(transaction)

     def is_valid_proof(cls, block, block_hash):
        #Check if block_hash is valid hash of block and satisfies
        #the difficulty criteria.
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())
     
     def mine(self):    
        #This function serves as an interface to add the pending
        #transactions to the blockchain by adding them to the block
        #and figuring out Proof Of Work.
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block()
        new_block = Block(last_block.index + 1, self.unconfirmed_transactions, time.time(), last_block.hash)
        #Get proof of work
        proof = self.proof_of_work(new_block)
        #Add Block to the BlockChain
        self.add_block(new_block, proof)
        #Validate Transactions
        for transaction in self.unconfirmed_transactions:
            transaction.ValidateTransaction()
        #Empty the list, as all transactions have now been confirmed
        self.unconfirmed_transactions = []
        self.adjust_difficulty()
        #print('for block',new_block.index)
        return True

     def adjust_difficulty(self):
         #feedback to adjust difficulty
         tt=int(time.time()-self.chain[0].timestamp)
         if(len(self.chain)>tt):self.difficulty+=1
         elif(len(self.chain)<tt and self.difficulty-1>0):self.difficulty-=1  
         print('current difficulty is',self.difficulty) 


def simulate_attack(blockChain,fakeBlock,computingPower,attack_speed) :
        # Represents the number of blocks found by the attacker
        counterAttacker = 0.0
        # Represents the number of blocks found by the honest miner
        counterHonestMiner = len(blockChain.chain)
        #attacker state
        attack_success=False
        #attack time calculation
        maxDurationCounter=1/attack_speed
        attackDurationCounter = 0
        #attack until attacker chain > official block chain or official block chain has enough confirmations
        while counterAttacker<=counterHonestMiner and attackDurationCounter<maxDurationCounter:
            attackDurationCounter+=1
            randomNumber = (random.randint(1, 100)) / 100
            if randomNumber>1-computingPower:counterAttacker+=1
            #if counterHonestMiner-fakeBlock.index >= confirmations_no:
             #   attack_success=False
              #  break
        if counterAttacker >= counterHonestMiner:
             attack_success=True
             blockChain.chain.pop(fakeBlock.index)
             blockChain.chain.insert(fakeBlock.index,fakeBlock)
        revenue_blocks_mined = counterAttacker
        speed=1/attackDurationCounter
        return revenue_blocks_mined,speed,attack_success



#USERS WHO PERFORM TRANSACTIONS ON THE COIN
Node("Yasser")
Node("Abbas")
Node("Shams")
Node("Waleed")
Node("Maher")

T1 = Transaction("Yasser",50,"Shams")
T2 = Transaction("Shams",50,"Abbas")
T3 = Transaction("Abbas",50,"Yasser")
T4 = Transaction("Waleed",50,"Maher")
T5 = Transaction("Maher",50,"Waleed")


difficulty=input("Enter difficulty value:")
bchain=Blockchain(int(difficulty))

#print('First Ledger')
bchain.add_new_transaction(T1)
bchain.add_new_transaction(T2)
bchain.add_new_transaction(T3)
bchain.mine()

#print('Second Ledger')
bchain.add_new_transaction(T4)
bchain.add_new_transaction(T5)
bchain.mine()

#print('Third Ledger')
bchain.add_new_transaction(T1)
bchain.add_new_transaction(T4)
bchain.add_new_transaction(T5)
bchain.mine()

#print('Fourth Ledger')
bchain.add_new_transaction(T2)
bchain.add_new_transaction(T3)
bchain.mine()

#print('Fifth Ledger')
bchain.add_new_transaction(T1)
bchain.add_new_transaction(T2)
bchain.add_new_transaction(T4)
bchain.mine()

#PRINTS ALL USERS WITH THE AMOUNT OF COINS AFTER TRANSACTION
Node.printNodes()
bchain.PrintChain()

computing_power=input('Enter computing Power of attacker:')
attack_speed=input('Enter attack speed:')
Fake_block_index=input('Enter Attacked Block index:')
fakeblock=Block(int(Fake_block_index),[T4,T5], time.time(), bchain.chain[int(Fake_block_index)].previous_hash)
bchain.proof_of_work(fakeblock)
blocks_mined,speed,attackStatus=simulate_attack(bchain,fakeblock,float(computing_power),float(attack_speed))
print('Attacker Block chain length:',blocks_mined,'Attacking Speed:',speed,'Attacking Status:',attackStatus)
print('Block chain after attack:')
bchain.PrintChain()

print('Legit Blockchain speed:',1/int(bchain.chain[len(bchain.chain)-1].timestamp-bchain.chain[0].timestamp))
print('Successful attack speed:',speed)

