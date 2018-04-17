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


