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
        List2 = [x for x in self.tips + self.has_verified if ((x.has_been_verified == False) and (not(x.node_identifier == T.node_identifier)))]
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
        U = [x for x in Tangle.tips if V.hash == x.hash]
        if(U):
            Tangle.tips.remove(U[0])
        
        U = [x for x in Tangle.has_verified if V.hash == x.hash]
        if(U):
            Tangle.has_verified.remove(U[0])
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

    Vc = [x for x in Tangle.currupt if (x.node_identifier == n_id)]
    if(Vc):
        response = {'index': -2}
        return jsonify(response),200

    V = [x for x in Tangle.tips if (x.node_identifier == n_id)]

    if not V:
        response = {'index': -1,}
        return jsonify(response),200

    V = V[0]
    
    if(len(V.verified) > 2):
        response = {
            'index' : 1
        }
        return jsonify(response),200
        
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
    Hash = Request["state_hash"]
    V = [x for x in Tangle.tips if x.hash == Hash]
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


