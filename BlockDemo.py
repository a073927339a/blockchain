# coding=UTF-8
import time
import json
import hashlib

class Block():

    def __init__(self):
        self.hashlist = []
        self.chain = []
        self.transactions = []

    def Genesis_block(self):
        global Previous_hash, Next_hash
        block = {
            'Hash': "This is Genesis Block",
            'Index': len(self.chain)+1,
            'Timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  ,
            'Transactions': [],
            'Previous_hash': "",
            'Nonce': "",
            'Merkle_Root': "",
            'Transaction_amount': 0,
            'CostTime': "0 sec"
        }
        Previous_hash = "This is Genesis Block"
        Next_hash = self.hash(block)
        self.chain.append(block)
        self.hashlist.append(Previous_hash)
        return block

    def new_block(self):
        start = time.time()
        global Previous_hash, Next_hash
        block = {
            'Hash': Next_hash,
            'Index': len(self.chain)+1,
            'Timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,
            'Transactions': self.transactions,
            'Previous_hash': Previous_hash,
            'Nonce': self.mine(),
            'Merkle_Root': self.root(),
            'Transaction_amount': len(self.transactions),
            'CostTime': 0
        }
        stop = time.time()
        block['CostTime'] = "%d sec" % (stop - start)
        Previous_hash = block['Hash']
        Next_hash = self.hash(block)
        self.transactions = []
        self.chain.append(block)
        self.hashlist.append(Previous_hash)
        return block

    def new_transaction(self,recipent, amount, comment = ""):
        self.transactions.append(
            {
                'Recipent': str(recipent),
                'Amount': str(amount),
                'comment': comment
            }
        )
        return self.transactions

    def root(self):
        treelist = []
        newlist = []
        for i in self.transactions:
            hash = self.hash(i)
            treelist.append(hash)
        while len(treelist) == 0:
            return 'Null'
        while len(treelist) == 1:
            hash = self.hash(treelist[0])
            return hash
        while len(treelist) > 1:
            # print treelist
            if (len(treelist) % 2) == 1:
                num = 1
                first = self.hash(treelist[0])
                newlist.append(first)
                for i in range((len(treelist) - 1) / 2):
                    second = self.hash(treelist[num])
                    third = self.hash(treelist[num + 1])
                    newlist.append(self.hash(second + third))
                    num += 2
                treelist = []
                for i in newlist:
                    treelist.append(i)
                newlist = []
                    # print '基數'
            elif (len(treelist) % 2) == 0:
                num = 1
                for i in range((len(treelist)) / 2):
                    first = self.hash(treelist[num - 1])
                    second = self.hash(treelist[num])
                    newlist.append(self.hash(first + second))
                    num += 2
                treelist = []
                for i in newlist:
                    treelist.append(i)
                newlist= []
                    # print '偶數'
        # print treelist
        return treelist[0]
        
    def mine(self):
        global nonce, mktree
        tx = json.dumps(self.transactions)
        mktree = hashlib.sha256(json.dumps(tx)).hexdigest()
        nonce = 1
        minehash = hashlib.sha256(json.dumps(mktree * nonce)).hexdigest()
        while True:
            if minehash < self.difficult():
                # print("Nonce:" + `nonce`, "Success Mining", "Result:" + `minehash`)
                return nonce
            else:
                nonce += 1
                print("Nonce: " + str(nonce))
                minehash = hashlib.sha256(json.dumps(mktree * nonce)).hexdigest()

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys = True).encode()   #dumps：把字典轉成json字符串
        return  hashlib.sha256(block_string).hexdigest()

    def last_block(self):
        return self.chain[-1]

    def getchain(self):
        return self.chain

    def printAllblock(self,chain):
        for i in chain:
            print 'Index : %s' %i["Index"]
            print 'Timestamp : %s' % i["Timestamp"]
            print 'Transaction_amount : %s' % i["Transaction_amount"]
            print 'Transactions : '
            for j in i["Transactions"]:
                print "【 " +"Recipent: %s, " % j["Recipent"] + "Amount: %s, " % j["Amount"] + "comment: %s" % j["comment"] + " 】"
            print 'Hash : %s' %i["Hash"]
            print 'Previous_hash : %s' % i["Previous_hash"]
            print 'Merkle_Root : %s' % i["Merkle_Root"]
            print 'Nonce : %s' % i["Nonce"]
            print 'CostTime : %s\n' % i["CostTime"]

    def printLastblock(self,block):
        i = block[-1]
        print 'Index : %s' % i["Index"]
        print 'Timestamp : %s' % i["Timestamp"]
        print 'Transaction_amount : %s' % i["Transaction_amount"]
        print 'Transactions : '
        for j in i["Transactions"]:
            print "【 " + "Recipent: %s, " % j["Recipent"] + "Amount: %s, " % j["Amount"] + "comment: %s" % j["comment"] + " 】"
        print 'Hash : %s' % i["Hash"]
        print 'Previous_hash : %s' % i["Previous_hash"]
        print 'Merkle_Root : %s' % i["Merkle_Root"]
        print 'Nonce : %s' % i["Nonce"]
        print 'CostTime : %s\n' % i["CostTime"]

    def difficult(self):
        return '000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'

# if __name__ == "__main__":
#     Blockchain = Block()
#     Blockchain.Genesis_block()
#     Blockchain.new_transaction("Lin","100","Hello")
#     Blockchain.new_transaction("Shan", "87", "World")
#     Blockchain.new_block()
#     Blockchain.printLastblock(Blockchain.chain)
