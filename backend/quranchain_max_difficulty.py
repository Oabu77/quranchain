import hashlib
import time
import json


class Block:
    def __init__(self, index, timestamp, data, previous_hash=""):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # Quran data (surahs, rewards, etc.)
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        """
        Compute the SHA-256 hash of the block.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True, default=str)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        """
        Proof of Work: Adjust nonce until hash matches the difficulty target.
        """
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()


class QuranChain:
    def __init__(self, difficulty=6):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Create the genesis block.
        """
        genesis_block = Block(0, time.time(), {"message": "Genesis Block: QuranChain Begins"}, "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        """
        Get the most recent block in the chain.
        """
        return self.chain[-1]

    def add_block(self, data):
        """
        Add a new block to the chain.
        """
        last_block = self.get_last_block()
        new_block = Block(len(self.chain), time.time(), data, last_block.hash)
        print(f"Mining block for Surah: {data['surah_name']} (Chapter {data['surah_number']})...")
        new_block.mine_block(self.difficulty)
        print(f"Block mined: {new_block.hash}")
        self.chain.append(new_block)

    def is_chain_valid(self):
        """
        Validate the integrity of the blockchain.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True


def load_quran_data(filename):
    """
    Load Quran data from a JSON file.
    """
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def add_quran_to_blockchain(blockchain, quran_data):
    """
    Add Quranic text to the blockchain, one surah per block.
    """
    for surah in quran_data:
        data = {
            "type": "QuranText",
            "surah_number": surah["chapter"],
            "surah_name": surah.get("name", f"Surah {surah['chapter']}"),
            "verses": surah["verses"]
        }
        print(f"Processing Surah: {data['surah_name']} (Chapter {data['surah_number']})")
        blockchain.add_block(data)


if __name__ == "__main__":
    # Set maximum mining difficulty
    MAX_DIFFICULTY = 6  # Adjust higher for more challenge

    # Initialize the blockchain with maximum difficulty
    blockchain = QuranChain(difficulty=MAX_DIFFICULTY)

    # Load Quran data from the JSON file
    quran_data = load_quran_data("full_quran_with_arabic.json")

    # Add Quran data to the blockchain
    add_quran_to_blockchain(blockchain, quran_data)

    # Validate the blockchain
    print("\nBlockchain valid:", blockchain.is_chain_valid())

    # Print blockchain summary
    for block in blockchain.chain:
        print(f"Block {block.index} - Surah: {block.data.get('surah_name', 'N/A')}")
        print(f"  Hash: {block.hash}")
        print("-" * 50)
