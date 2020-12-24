# 계절학기 PJT - 발표

## Block Chain



### Proof of Work(작업 증명) or Mining(채굴)

작업 증명은 새로운 블록을 블록체인에 추가하는 작업을 완료했음을 증명하는 것이다. '새로운 블록을 블록체인에 추가한다'는 것은, 그동안 진행된 거래를 유효한 것으로 만들어 공식화한다는 것을 뜻한다. 새로운 블록을 블록체인에 추가하려면, 그 새로운 블록의 해쉬의 값이 특정 숫자보다 작아지게 만드는 임의의 숫자 X를 찾아야 한다. 그 숫자 X는 블록의 헤더에서 유일하게 변화시킬 수 있는, nonce 값을 변화시키며 찾는다. 결론적으로 이 nonce 값을 구하는 것이 바로 작업 증명이다. 한 블록에 유효한 nonce를 가장 먼저 찾은 채굴자에게 보상이 주어지며, 즉시 다음 블록이 진행된다. N-1번 블록이 생성되었다는 소식을 접한 각 노드는 이 정보(previous block hash)를 바탕으로 즉시 N번 블록을 채굴하기 시작하는 것이다.



### Test형 가상화폐 채굴을 위한 웹 프로젝트

> Flask 사용
>
> difficulty = 5

```python
# Block
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
```



```python
# Block Chain

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
```



```python
# index

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
```