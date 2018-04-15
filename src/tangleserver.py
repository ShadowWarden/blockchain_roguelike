# blockchain/main.py
#
# Omkar H. Ramachandran
# omkar.ramachandran@colorado.edu
#
# My first shot at building a blockchain. Will use an API for the
# actual hackathon
#

import hashlib
import json
from time import time
from textwrap import dedent
from uuid import uuid4
import numpy as np

import state as S

from flask import Flask, jsonify, request

class TangleServer(object):
    def __init__(self):
        self.tips = []
        self.has_verified = []
        self.currupt = []

    def add_tip(self, State):
        self.tips.append(State)

    def remove_tip(self, State):
        try:
            self.tips.remove(State)
        except:
            print("State not a tip!")
            return -1
        self.has_verified.append(State)

    def scrub_tip(self):
        for v in self.tips:
            if(len(v.verified) >= 2):
                self.remove_tip(v)

    def assign(self,T):
        List2 = [x for x in self.tips + self.has_verified if ((not (x.has_been_verified)) and (not(x.node_identifier == T.node_identifier)))]
        if((len(T.toverify) >= 2) or (not List2)):
            return -1
        p = np.ones(len(List2))/(len(List2))
        C = np.random.choice(np.linspace(1,len(List2),len(List2)),p=p)
        T.toverify.append(List2[int(C-1)])
        return 0

    def set_verified(self, S, index):
        V = S.toverify[index]
        S.toverify.remove(V)
        S.verified.append(V)
        V.has_been_verified = True

    def set_currupt(self, S, index):
        V = S.toverify[index]
        S.toverify.remove(V)
        self.currupt.append(V)
        V.has_been_verified = False

    def scrub_verified(self):
        for v in self.has_verified:
            if(v.has_been_verified):
                self.has_verified.remove(v)

Tangle = TangleServer()

app = Flask(__name__)

@app.route('/create_instance',methods=['POST'])
def add_to_Tangle():
    values = request.get_data() 
    Request = json.loads(values)
    St = S.State()
    St.Mhash = Request["Mhash"]
    St.ithash = Request["ithash"]
    St.hash = Request["hash"]
    St.node_identifier = Request["n_id"]
    Tangle.add_tip(St)
    print(Request)
    print("New tip added")
    response = {'message': f'Success'}
    return jsonify(response),200

@app.route('/check',methods=['POST'])
def get_verify():
    values = request.get_data() 
    Request = json.loads(values)
    n_id = Request["n_id"]

    print(n_id)

    Vc = [x for x in Tangle.currupt if (x.node_identifier == n_id)]
    print(Vc)
    if(Vc):
        response = {'index': -2}
        return jsonify(response),200

    V = [x for x in Tangle.tips if (x.node_identifier == n_id)]

    if not V:
        response = {'index': f'-1',}
        return jsonify(response),200

    V = V[0]

    res = Tangle.assign(V)

    if(res == -1):
        response = {
                'index' : -1
                }
    else:
        Mhash = V.toverify[0].Mhash
        ithash = V.toverify[0].ithash   
        Hash = V.toverify[0].hash   
        response = {
                'index': 0,
                'Mhash': Mhash,
                'ithash': ithash,
                'hash': Hash,
                }
    print(response)
    return jsonify(response),200



@app.route('/verify',methods=['Post'])
def verify():
    values = request.get_data()
    Request = json.loads(values) 
    n_id = Request["n_id"]
    V = [x for x in Tangle.tips if x.node_identifier == n_id]
    is_verified = Request["is_verified"]
    response = {
            'message': "Success",
            }

    print(is_verified)

    if(is_verified):
        Tangle.set_verified(V[0],0)        
        Tangle.scrub_tip()
        Tangle.scrub_verified()
    if(not is_verified):
        Tangle.set_currupt(V[0],0)
        Tangle.scrub_tip()
        Tangle.scrub_verified()

    return jsonify(response),200

if __name__=="__main__":
    app.run('127.0.0.1',port=5000)

#class Blockchain(object):
#    def __init__(self):
#        # Each Blockchain contains two main class variables,
#        # the current transactions in progress and the chain of
#        # blocks
#        self.chain = []
#        self.current_transactions = []
#
#        # This is the, so called, genesis block.
#        self.new_block(previous_hash=1,proof=100)
#
#    def new_block(self,proof,previous_hash=None):
#        # Creates new block and adds it to the chain
#        block = {
#            'index': len(self.chain)+1,
#            'timestamp': time(),
#            'transactions': self.current_transactions,
#            'proof': proof,
#            'previous_hash': previous_hash or self.hash(self.chain[-1]),
#        }
#        self.current_transactions = []
#        self.chain.append(block)
#        return block
#
#
#    def new_transaction(self,sender,recipient,amount):
#        # Adds a new transaction to the current list.
#        # Transaction indices are currently sequential
#        self.current_transactions.append({
#                'sender': sender,
#                'recipient':recipient,
#                'amount':amount,    
#            })
#        return self.last_block['index'] + 1
#
#    def proof_of_work(self, last_proof):
#        """
#        Simple POW algorithm:
#        - Find new p such that hash(p*p_old) contains a leading zero
#        """
#        proof = 0
#        while self.valid_proof(last_proof,proof) is False:
#            proof += 1
#
#        return proof
#
#    def valid_proof(self,last_proof,proof):
#        guess = f'{last_proof}{proof}'.encode()
#        guess_hash = hashlib.sha256(guess).hexdigest()
#        return guess_hash[:1] == '0'
#    
#    def hash(self,block):
#        # Hashes a block
#        block_string = json.dumps(block, sort_keys=True).encode()
#        return hashlib.sha256(block_string).hexdigest()
#
#    @property
#    def last_block(self):
#        return self.chain[-1]
#
#app = Flask(__name__)
#
#node_identifier = str(uuid4()).replace('-','')
#
#blockchain = Blockchain()
#
#@app.route('/mine',methods=['GET'])
#
#def mine():
#    last_block = blockchain.last_block
#    last_proof = last_block['proof']
#    proof = blockchain.proof_of_work(last_proof)
#    # Carrot for finding new hash
#    # Sender = 0 signifies mining of new coin
#    blockchain.new_transaction(
#        sender = "0",
#        recipient = node_identifier,
#        amount = 1,
#    )
#    # Forge new block
#    previous_hash = blockchain.hash(last_block)
#    block = blockchain.new_block(proof, previous_hash)
#
#    response = {
#        'message': "New Block Forged",
#        'index': block['index'],
#        'transactions': block['transactions'],
#        'proof': block['proof'],
#        'previous_hash': block['previous_hash'],
#    }
#
#    return jsonify(response),200
#
#@app.route('/chain',methods=['GET'])
#def full_chain():
#    response = {
#        'chain': blockchain.chain,
#        'length': len(blockchain.chain),
#    }
#    return jsonify(response), 200
#
#@app.route('/transactions/new/', methods=['POST'])
#def new_transaction():
#    values = request.get_json()
#    print(values)
#
#    required = ['sender','recipient','amount']
#    if not all(k in values for k in required):
#        return 'Missing Values', 400
#
#    index = blockchain.new_transaction(values['sender'],values['recipient'],values['amount'])
#
#    response = {'message': f'Transaction will be added to Block {index}'}
#    return jsonify(response), 201
#
#if __name__ == '__main__':
#    app.run(host='127.0.0.1', port=5000)
