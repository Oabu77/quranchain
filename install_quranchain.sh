#!/bin/bash

# Constants and environment variables
QURANCHAIN_DIR="$HOME/QuranChain"
DATA_DIR="$QURANCHAIN_DIR/data"
LOG_DIR="$QURANCHAIN_DIR/logs"
JWT_SECRET_FILE="$DATA_DIR/jwtsecret"
WALLET_ADDRESS="0x4aC734e6B856C0FFDDDCAD871892bfFe1d1A1cd4"
PASSWORD="Rick&Morty91!"
PRYSM_BEACON_BINARY="$QURANCHAIN_DIR/prysm/dist/beacon-chain-v5.1.2-linux-amd64"

# Ensure the script is run as a non-root user with sudo permissions
if [ "$EUID" -eq 0 ]; then
  echo "Please do not run as root. Use a non-root user with sudo privileges."
  exit 1
fi

echo "Starting QuranChain installation..."

# Step 1: Update and Install Dependencies
echo "Updating package list and installing dependencies..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git g++ make python3 python3-pip openjdk-17-jre \
     nodejs npm jq golang software-properties-common build-essential

# Step 2: Set up directories
echo "Setting up directories..."
mkdir -p "$DATA_DIR" "$LOG_DIR"

# Step 3: Install Geth
echo "Installing Geth (Go Ethereum)..."
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt update
sudo apt install -y geth

# Step 4: Install Prysm
echo "Installing Prysm..."
PRYSM_URL="https://github.com/prysmaticlabs/prysm/releases/download/v5.1.2/beacon-chain-v5.1.2-linux-amd64"
mkdir -p "$QURANCHAIN_DIR/prysm/dist"
wget -qO "$PRYSM_BEACON_BINARY" "$PRYSM_URL"
chmod +x "$PRYSM_BEACON_BINARY"

# Step 5: Generate JWT Secret
if [ ! -f "$JWT_SECRET_FILE" ]; then
  echo "Generating JWT secret..."
  openssl rand -hex 32 > "$JWT_SECRET_FILE"
fi

# Step 6: Create Wallet Account
if [ ! -f "$DATA_DIR/keystore" ]; then
  echo "Creating wallet account..."
  echo "$PASSWORD" > "$QURANCHAIN_DIR/password.txt"
  geth account new --datadir "$DATA_DIR" --password "$QURANCHAIN_DIR/password.txt"
fi

# Step 7: Write Start Script
echo "Creating start script..."
START_SCRIPT="$QURANCHAIN_DIR/start_quranchain.sh"

cat <<EOF > "$START_SCRIPT"
#!/bin/bash
echo "Starting QuranChain nodes..."

# Start Geth Node
geth --datadir "$DATA_DIR" --networkid 323671 \
     --http --http.addr 0.0.0.0 --http.port 8545 \
     --http.api eth,net,web3,personal,miner \
     --authrpc.port 8551 --authrpc.addr 0.0.0.0 \
     --authrpc.jwtsecret "$JWT_SECRET_FILE" \
     --mine --syncmode full \
     --unlock "$WALLET_ADDRESS" --password "$QURANCHAIN_DIR/password.txt" \
     --allow-insecure-unlock \
     --port 30303 > "$LOG_DIR/geth.log" 2>&1 &

# Start Prysm Beacon Chain
"$PRYSM_BEACON_BINARY" --datadir="$DATA_DIR/beacon" \
    --execution-endpoint=http://127.0.0.1:8551 \
    --jwt-secret="$JWT_SECRET_FILE" \
    --suggested-fee-recipient="$WALLET_ADDRESS" \
    --monitoring-host=0.0.0.0 \
    --monitoring-port=5052 > "$LOG_DIR/beacon.log" 2>&1 &
EOF

chmod +x "$START_SCRIPT"

# Step 8: Finalize
echo "Installation completed!"
echo "Run QuranChain using the following command:"
echo "bash $START_SCRIPT"
