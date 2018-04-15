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
import requests

from flask import Flask, jsonify, request

class State(object):
    def __init__(self):
        self.hash = ''
        self.Mhash = ''
        self.ithash = ''
        self.verified = []
        self.currupt = []
        self.toverify = []
        self.node_identifier = ''
        self.has_been_verified = False

    def new_state(self,node_identifier,node_count):
        self.node_identifier = node_identifier
        M = f'{node_identifier}{node_count}'.encode()
        self.Mhash = hashlib.sha256(M).hexdigest()
        node_count += 1
        it = f'{node_identifier}{node_count}'.encode()
        self.ithash = hashlib.sha256(it).hexdigest()
        node_count += 1
        Hashcount = 0
        gl = f'{Hashcount}'.encode()
        self.hash = hashlib.sha256(gl).hexdigest()
        while(not self.valid(self.Mhash,self.ithash,self.hash)):
            Hashcount += 1
            gl = f'{Hashcount}'.encode()
            self.hash = hashlib.sha256(gl).hexdigest()
        return self.hash, node_count

    def valid(self,Mhash,ithash,Hash):
        combo = f'{Mhash}{ithash}{Hash}'.encode()
#        print(combo)
        combo_hash = hashlib.sha256(combo).hexdigest()
#        print(combo_hash)
        return combo_hash[:2] == '01'
     
    def verify(self,otherState):
        return self.valid(otherState.Mhash,otherState.ithash,otherState.hash)

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
