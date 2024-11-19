from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
from quranchain_full import QuranChain, Block, load_blockchain, save_blockchain

app = Flask(__name__)
CORS(app)

# Initialize or load the blockchain
blockchain = load_blockchain()

# Muslim Wallet API URL (replace with your actual wallet service)
MUSLIM_WALLET_API_URL = "https://muslimwalletapi.com"  # Example URL


def call_wallet_api(endpoint, method="GET", payload=None):
    """
    Generic function to call the Muslim Wallet API.
    """
    url = f"{MUSLIM_WALLET_API_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    try:
        if method == "POST":
            response = requests.post(url, json=payload, headers=headers)
        else:
            response = requests.get(url, params=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Wallet API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


@app.route("/wallet/balance/<wallet_address>", methods=["GET"])
def get_wallet_balance(wallet_address):
    """
    Get the balance of a wallet.
    """
    response = call_wallet_api(f"/wallet/{wallet_address}/balance")
    return jsonify(response), 200


@app.route("/wallet/transfer", methods=["POST"])
def transfer_funds():
    """
    Transfer QuranCoin or MuslimCoin between wallets.
    """
    data = request.json
    sender = data.get("sender")
    recipient = data.get("recipient")
    amount = data.get("amount")
    currency = data.get("currency")

    if not (sender and recipient and amount and currency):
        return jsonify({"error": "Invalid transfer data"}), 400

    response = call_wallet_api(
        "/wallet/transfer",
        method="POST",
        payload={
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "currency": currency,
        },
    )
    return jsonify(response), 200


@app.route("/submit_reward", methods=["POST"])
def submit_reward():
    """
    Submit a reward to the blockchain and transfer funds to the miner's wallet.
    """
    data = request.json
    miner = data.get("miner")
    surah = data.get("surah")
    ayahs = data.get("ayahs")
    wallet_address = data.get("wallet_address")

    if not (miner and surah and ayahs and wallet_address):
        return jsonify({"error": "Invalid reward submission"}), 400

    reward_amount = int(ayahs) * 10  # Reward logic
    blockchain.add_reward(miner, surah, ayahs)

    # Transfer QuranCoin to the miner's wallet
    transfer_response = call_wallet_api(
        "/wallet/transfer",
        method="POST",
        payload={
            "sender": "QuranChain",
            "recipient": wallet_address,
            "amount": reward_amount,
            "currency": "QuranCoin",
        },
    )

    save_blockchain(blockchain)
    return jsonify(
        {
            "message": "Reward added and funds transferred successfully",
            "reward": data,
            "wallet_transfer": transfer_response,
        }
    ), 201


if __name__ == "__main__":
    app.run(debug=True)
