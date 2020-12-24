from flask import Flask, render_template, jsonify, request
import hashlib
import json


class Block:
    def __init__(self, data, previous_hash, nonce=0):
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = nonce
        self.hash = self.generate_hash()

    def print_block(self):
        print(f"nonce: {self.nonce}\n"
              f"data: {self.data}\n"
              f"prev_hash: {self.previous_hash}\n"
              f"hash: {self.hash}\n\n")

    def generate_hash(self):
        block_contents = str(self.previous_hash) + str(self.nonce)
        block_hash = hashlib.sha256(block_contents.encode())
        return block_hash.hexdigest()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4, separators=(',', ': '))


class Blockchain(object):
    def __init__(self):
        self.chain = [Block("Genesis", 0)]

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self):
        previous_block_hash = self.chain[len(self.chain) - 1].hash
        new_block = Block(len(self.chain), previous_block_hash)
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)
        return new_block

    def proof_of_work(self, block, difficulty=5):
        proof = block.generate_hash()

        while proof[:difficulty] != '0' * difficulty:
            block.nonce += 1
            proof = block.generate_hash()
        return proof


app = Flask(__name__)
block_chain = Blockchain();


@app.route('/', methods=['GET', 'POST'])  # url
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        block_chain.add_block()
        index = str(block_chain.last_block.data)
        hash = str(block_chain.last_block.hash)
        nonce = str(block_chain.last_block.nonce)
        prev_hash = str(block_chain.last_block.previous_hash)

        return render_template('index.html', index=index, hash=hash, nonce=nonce, prev_hash=prev_hash)


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': list(map(Block.toJSON, block_chain.chain)),
        'length': len(block_chain.chain)
    }
    print(response)
    return jsonify(response), 200


if __name__ == "__main__":

    for i in range(5):
        block_chain.add_block()

    app.run(debug=True)
