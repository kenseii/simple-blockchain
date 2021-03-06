# -*- coding: utf-8 -*-
"""

First blockchain script :-)

"""

# Libraries import

import datetime
import hashlib
import json
from flask import Flask,jsonify

# Building a blockchain

class Blockchain:
    
    """
    Initiate the object
    create a genesis block
    
    """
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    """
    
    This method creates a block using the given information and add it to the chain
    
    """
    def create_block(self, proof, previous_hash):
        block = {'index':len(self.chain)+1, 
                 'timestamp':str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash':previous_hash}
        
        self.chain.append(block)
        return block
    
    """
    
    Get the last block in the chain
    
    """
    
    def get_previous_block(self):
        return self.chain[-1]
    
    """
    
    proof of work number finder by
    
    1. setting the default to 1
    2. as long as it isnt generating a hash starting with 4 zeroes try again by incrementing the proof
    3. once the proof number gets a correct hash set the check_proof to true
    
    """
    
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        
        return new_proof
    
    
    """
    
    hash given block
    
    """
    
    def hash(self, block):
        encoded_block = json.dumps(block,sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    """
    validate bwana wangu
    
    1. check if the previous hash is correct/ existing link
    2. check if the proof hashing starts by 4 zeroes
    3. Increment the block index to take the next block and set previous block to the current/finished block
    
    """
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
            
        return True
            
            
    
# Mining a blockchain
        
# Flask Web app

app = Flask(__name__)        

# instance of the blockchain class

blockchain = Blockchain()

"""

1. return the proof of the previous block
2. calculate the proof_of_work of the new block
3. hash the previous_block
4. create a block with the data in hand
5. return the block data in json + response code

"""
@app.route('/mine_block',methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    
    # because it returns the content of that block after creating it 
    block = blockchain.create_block(proof, previous_hash)
    
    response = {'message' : 'Omedetou, you mined a block!',
                'index':block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash']
                }
    return jsonify(response), 200


"""

Return all the chain

"""
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response), 200

"""

Checking if the chain is valid via api request

"""

@app.route('/is_valid',methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message':'The chain is valid'}
    else:
        response = {'message':'Abunai, the chain is invalid!!!'}
        
    return jsonify(response), 200

"""

Run the flask app

"""

app.run(host='0.0.0.0',port=5000)