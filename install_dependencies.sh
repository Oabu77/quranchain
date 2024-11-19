#!/bin/bash

# Ensure the script is run with sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root using sudo."
  exit 1
fi

echo "Starting installation of dependencies for QuranChain..."

# Step 1: Update the system
echo "Updating system packages..."
apt update && apt upgrade -y

# Step 2: Install general dependencies
echo "Installing general dependencies..."
apt install -y curl wget git g++ make python3 python3-pip openjdk-17-jre \
    nodejs npm jq golang software-properties-common build-essential unzip

# Step 3: Add Ethereum repository and install Geth
echo "Installing Go Ethereum (Geth)..."
add-apt-repository -y ppa:ethereum/ethereum
apt update
apt install -y geth

# Step 4: Install Prysm Beacon Chain
echo "Installing Prysm Beacon Chain..."
PRYSM_URL="https://github.com/prysmaticlabs/prysm/releases/download/v5.1.2/beacon-chain-v5.1.2-linux-amd64"
mkdir -p /opt/prysm
wget -qO /opt/prysm/beacon-chain "$PRYSM_URL"
chmod +x /opt/prysm/beacon-chain

# Step 5: Install OpenJDK (for Besu if needed)
echo "Installing OpenJDK 17..."
apt install -y openjdk-17-jre

# Step 6: Install Node.js and npm
echo "Installing Node.js and npm..."
curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
apt install -y nodejs

# Step 7: Install Python and pip dependencies
echo "Installing Python and pip dependencies..."
pip3 install --upgrade pip setuptools wheel
pip3 install psutil

# Step 8: Install Golang (for blockchain development)
echo "Installing Go programming language..."
wget -qO- https://go.dev/dl/go1.21.0.linux-amd64.tar.gz | tar -C /usr/local -xz
export PATH=$PATH:/usr/local/go/bin

# Step 9: Finalize
echo "Dependencies installation complete!"
echo "Installed components:"
echo "- Geth (Ethereum Client)"
echo "- Prysm Beacon Chain"
echo "- OpenJDK 17"
echo "- Node.js and npm"
echo "- Python and psutil library"
echo "- Golang (Go Programming Language)"
