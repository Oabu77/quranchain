import hashlib
import json
import time
import random
import string
from tqdm import tqdm
import os

# Wallet class definition
class Wallet:
    def __init__(self, username, address=None):
        self.username = username
        self.address = address or self.create_wallet_address()
        self.quran_coin_balance = 0
        self.muslim_coin_balance = 0

    def create_wallet_address(self):
        return "MW" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))

    def add_quran_coin(self, amount):
        self.quran_coin_balance += amount

    def add_muslim_coin(self, amount):
        self.muslim_coin_balance += amount

    def to_dict(self):
        return {
            "username": self.username,
            "address": self.address,
            "quran_coin_balance": self.quran_coin_balance,
            "muslim_coin_balance": self.muslim_coin_balance,
        }

    @staticmethod
    def from_dict(data):
        wallet = Wallet(data["username"], data["address"])
        wallet.quran_coin_balance = data["quran_coin_balance"]
        wallet.muslim_coin_balance = data["muslim_coin_balance"]
        return wallet

# Block class definition
class Block:
    def __init__(self, index, timestamp, data, previous_hash=""):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

# Blockchain class definition
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = self.mine_block(data, previous_block.hash)
        self.chain.append(new_block)
        return new_block

    def mine_block(self, data, previous_hash):
        index = len(self.chain)
        timestamp = time.time()
        nonce = 0
        difficulty = "000000"  # Real-world mining difficulty
        print(f"Starting mining for data: {data['surah_name']} (Chapter {data['surah_number']})")
        with tqdm(total=100, desc=f"Mining Block {index}", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            while True:
                block = Block(index, timestamp, data, previous_hash)
                block.nonce = nonce
                block.hash = self.calculate_hash_with_nonce(block)
                if block.hash.startswith(difficulty):
                    return block
                nonce += 1

                if nonce % 10000 == 0:  # Update progress bar every 10,000 attempts
                    pbar.update(1)

    def calculate_hash_with_nonce(self, block):
        block_string = json.dumps({
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "previous_hash": block.previous_hash,
            "nonce": getattr(block, "nonce", 0)
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

def load_wallets(filename="wallets.json"):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        return {username: Wallet.from_dict(wallet) for username, wallet in data.items()}

def save_wallets(wallets, filename="wallets.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump({username: wallet.to_dict() for username, wallet in wallets.items()}, file, indent=4)

def user_signup(wallets, blockchain):
    username = input("Enter your username: ").strip()
    if username in wallets:
        print(f"Username '{username}' is already taken.")
        return None
    wallet = Wallet(username)
    wallets[username] = wallet
    save_wallets(wallets)
    print(f"Wallet created! Address: {wallet.address}")
    
    blockchain.add_block({
        "type": "User",
        "username": username,
        "wallet_address": wallet.address,
        "quran_coin_balance": wallet.quran_coin_balance,
        "muslim_coin_balance": wallet.muslim_coin_balance
    })
    print(f"User {username} added to the blockchain.")
    return wallet

def user_signin(wallets):
    username = input("Enter your username to sign in: ").strip()
    if username in wallets:
        wallet = wallets[username]
        print(f"\nWelcome back, {username}!")
        print(f"Wallet Address: {wallet.address}")
        print(f"QuranCoin Balance: {wallet.quran_coin_balance}")
        print(f"MuslimCoin Balance: {wallet.muslim_coin_balance}\n")
        return wallet
    else:
        print("Error: Username not found. Please sign up first.")
        return None

def main():
    blockchain = Blockchain()
    wallets = load_wallets()
    current_user = None

    print("Welcome to QuranChain!")
    while True:
        print("\n1. Sign Up")
        print("2. Sign In")
        print("3. Mine Quran Text")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            current_user = user_signup(wallets, blockchain)
        elif choice == "2":
            current_user = user_signin(wallets)
        elif choice == "3":
            if current_user:
                try:
                    with open('/home/ubuntu/quranchain/data/full_quran_with_arabic.json', 'r', encoding='utf-8') as file:
                        quran_data = json.load(file)
                except FileNotFoundError:
                    print("Error: Quran data file not found.")
                    continue

                for surah in quran_data:
                    surah_name = surah.get("name", f"Surah {surah['chapter']}")
                    print(f"\nProcessing Surah: {surah_name} (Chapter {surah['chapter']})")
                    mined_data = {
                        "type": "QuranText",
                        "surah_number": surah["chapter"],
                        "surah_name": surah_name,
                        "verses": surah["verses"]
                    }
                    mined_block = blockchain.add_block(mined_data)
                    print(f"\nBlock Mined: {mined_block.hash}")
                    print(f"Surah: {surah_name}\n")
                    for idx, verse in enumerate(surah["verses"], start=1):
                        print(f"Verse {idx}:")
                        print(f"  Arabic: {verse['arabic']}")
                        print(f"  English: {verse['english']}\n")
                    current_user.add_quran_coin(10)
                    save_wallets(wallets)
                    print(f"Rewarded {current_user.username} ({current_user.address}) with 10 QuranCoins.\n")
            else:
                print("Please sign in first to start mining.")
        elif choice == "4":
            print("Exiting QuranChain. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
