#!/bin/bash

# Install script for setting up the system bot
# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root using sudo."
  exit
fi

echo "Starting installation..."

# Update system packages
echo "Updating system packages..."
apt update && apt upgrade -y

# Install essential system tools
echo "Installing essential tools..."
apt install -y python3 python3-pip git curl build-essential

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install web3 flask requests gitpython openai

# Create bot directories
echo "Setting up bot directories..."
BOT_DIR="/opt/project_bot"
LOG_DIR="$BOT_DIR/logs"
MODULE_DIR="$BOT_DIR/modules"
CONFIG_FILE="$BOT_DIR/config.py"

mkdir -p "$LOG_DIR" "$MODULE_DIR"

# Create a configuration file
echo "Creating configuration file..."
cat <<EOL > $CONFIG_FILE
# Bot configuration file

# Blockchain settings
INFURA_URL = "https://polygon-mainnet.g.alchemy.com/v2/YOUR_API_KEY"
WALLET_ADDRESS = "0xdCD219AeA237921a21dc69D3d5d0b4003461746F"

# OpenAI API Key
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

# Telegram settings (Optional)
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

EOL

# Create a main bot script
echo "Creating main bot script..."
cat <<EOL > $BOT_DIR/main.py
import os
import logging
from web3 import Web3
import openai
import requests
from git import Repo

# Load configuration
CONFIG = {
    "INFURA_URL": os.getenv("INFURA_URL"),
    "WALLET_ADDRESS": os.getenv("WALLET_ADDRESS"),
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),
    "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
}

# Setup logging
logging.basicConfig(filename='/opt/project_bot/logs/bot.log', level=logging.INFO)

# Blockchain interaction
w3 = Web3(Web3.HTTPProvider(CONFIG["INFURA_URL"]))

def get_balance(address):
    balance = w3.eth.get_balance(address)
    logging.info(f"Checked balance for {address}: {balance}")
    return w3.fromWei(balance, 'ether')

# OpenAI interaction
def suggest_code(prompt):
    openai.api_key = CONFIG["OPENAI_API_KEY"]
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        max_tokens=150
    )
    result = response['choices'][0]['text'].strip()
    logging.info(f"Suggested code for prompt: {prompt}")
    return result

# Git repository interaction
def sync_repository(repo_path, branch='main'):
    repo = Repo(repo_path)
    repo.git.checkout(branch)
    repo.git.pull('origin', branch)
    logging.info(f"Repository {repo_path} synced with branch {branch}.")

# Telegram notification
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{CONFIG['TELEGRAM_TOKEN']}/sendMessage"
    data = {"chat_id": CONFIG["TELEGRAM_CHAT_ID"], "text": message}
    response = requests.post(url, data=data)
    logging.info(f"Sent Telegram message: {message}")
    return response.status_code

# CLI interface
if __name__ == "__main__":
    print("Project Bot CLI")
    print("1. Check Wallet Balance")
    print("2. Sync Git Repository")
    print("3. Generate Code Suggestion")
    choice = input("Enter your choice: ")

    if choice == '1':
        balance = get_balance(CONFIG["WALLET_ADDRESS"])
        print(f"Balance: {balance} ETH")
    elif choice == '2':
        repo_path = input("Enter repository path: ")
        sync_repository(repo_path)
        print("Repository synced.")
    elif choice == '3':
        prompt = input("Enter code prompt: ")
        suggestion = suggest_code(prompt)
        print("Suggested Code:\n", suggestion)
    else:
        print("Invalid choice.")
EOL

# Make the bot executable
chmod +x $BOT_DIR/main.py

# Add environment variables to the system
echo "Exporting environment variables..."
cat <<EOL >> /etc/environment
INFURA_URL="https://polygon-mainnet.g.alchemy.com/v2/YOUR_API_KEY"
WALLET_ADDRESS="0xdCD219AeA237921a21dc69D3d5d0b4003461746F"
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
TELEGRAM_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID"
EOL

# Add bot to PATH
echo "Adding bot to PATH..."
ln -s $BOT_DIR/main.py /usr/local/bin/project-bot

# Completion message
echo "Installation complete! You can now run the bot using the command: project-bot"

# Test bot
echo "Testing bot..."
python3 $BOT_DIR/main.py
