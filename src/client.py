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

import state as S

node_identifier = str(uuid4()).replace('-','')
node_count = 0

def create_state(node_count):
    state1 = S.State()
    res = state1.new_state(node_identifier,node_count)
    node_count = res[1]
    request1 = {
            "n_id":state1.node_identifier,
            "Mhash":state1.Mhash,
            "ithash":state1.ithash,
            "hash":state1.hash,
            }

    request1 = json.dumps(request1)

    res = requests.post("http://127.0.0.1:5000/create_instance",data=request1)
    return state1

def create_fake_state(node_count):
    state1 = S.State()
    res = state1.new_state(node_identifier,node_count) 
    state1.hash = state1.Mhash
    node_count = res[1]
    request1 = {
            "n_id":state1.node_identifier,
            "Mhash":state1.Mhash,
            "ithash":state1.ithash,
            "hash":state1.hash,
            }

    request1 = json.dumps(request1)

    res = requests.post("http://127.0.0.1:5000/create_instance",data=request1)
    return state1


def check(state1):
    request1 = {
            "n_id":node_identifier,
            }

    request1 = json.dumps(request1)

    res = requests.post("http://127.0.0.1:5000/check",data=request1)

    Res = json.loads(res.content)

    print(Res)

    if(Res["index"] == -1):
        # Do Nothing
        return Res

    if(Res["index"] == -2):
        # Currupt entry
        print("Oooh. Naughty. Your items have been deleted")
        return Res

    else:
        stateback = S.State()
        stateback.Mhash = Res["Mhash"]
        stateback.ithash = Res["ithash"]
        stateback.hash = Res["hash"]

        sendback = state1.verify(stateback)


        requestback = {
                "state_hash":state1.hash,
                "is_verified":sendback,
        }

        requestback = json.dumps(requestback)
        res2 = requests.post("http://127.0.0.1:5000/verify",data=requestback)

        return Res
