#!/bin/bash

# Configuration
BASE_DIR="$HOME/QuranChain"
NODE_COUNT=99
BASE_HTTP_PORT=8545
BASE_AUTHRPC_PORT=8551
BASE_IPC_PORT=30303
LOG_FILE="$BASE_DIR/logs/node_manager.log"
JWT_SECRET="$BASE_DIR/data/jwtsecret"
GENESIS_FILE="$BASE_DIR/genesis.json"
NODE_NAME_PREFIX="quranchain-node"

# Ensure logs directory exists
mkdir -p "$BASE_DIR/logs"

# Setup logging
exec > >(tee -i "$LOG_FILE") 2>&1

# Functions

setup_nodes() {
  echo "Setting up $NODE_COUNT nodes..."
  for i in $(seq 1 $NODE_COUNT); do
    NODE_DIR="$BASE_DIR/data$i"
    HTTP_PORT=$((BASE_HTTP_PORT + i))
    AUTHRPC_PORT=$((BASE_AUTHRPC_PORT + i))
    NODE_PORT=$((BASE_IPC_PORT + i))

    mkdir -p "$NODE_DIR/geth" "$NODE_DIR/keystore"
    echo "Node $i: Configuring data directory at $NODE_DIR"

    # Initialize the node
    if [ ! -d "$NODE_DIR/geth/chaindata" ]; then
      geth --datadir "$NODE_DIR" init "$GENESIS_FILE"
      echo "Node $i: Genesis block initialized."
    fi

    # Create an account for the node if not already created
    if [ ! "$(ls -A $NODE_DIR/keystore)" ]; then
      echo "Rick&Morty91!" > "$NODE_DIR/password.txt"
      geth --datadir "$NODE_DIR" account new --password "$NODE_DIR/password.txt"
      echo "Node $i: Account created."
    fi

    # Start the node
    echo "Starting Node $i..."
    geth --datadir "$NODE_DIR" \
      --networkid 323671 \
      --http --http.addr "127.0.0.1" --http.port $HTTP_PORT \
      --http.api "eth,net,web3,personal,miner" \
      --ipcpath "$NODE_DIR/geth.ipc" \
      --authrpc.jwtsecret "$JWT_SECRET" \
      --mine --syncmode "full" \
      --unlock "$(cat $NODE_DIR/keystore/* | jq -r '.address')" \
      --password "$NODE_DIR/password.txt" \
      --port $NODE_PORT \
      --allow-insecure-unlock &

    echo "Node $i started at HTTP port $HTTP_PORT, Auth RPC port $AUTHRPC_PORT, and Node port $NODE_PORT."
  done
}

check_nodes() {
  echo "Checking status of all nodes..."
  for i in $(seq 1 $NODE_COUNT); do
    HTTP_PORT=$((BASE_HTTP_PORT + i))
    NODE_DIR="$BASE_DIR/data$i"

    if [ -S "$NODE_DIR/geth.ipc" ]; then
      echo "Node $i: IPC is accessible at $NODE_DIR/geth.ipc"
    else
      echo "Node $i: IPC is not accessible. Attempting repair..."
      repair_node $i
    fi

    if curl -s "http://127.0.0.1:$HTTP_PORT" > /dev/null; then
      echo "Node $i: HTTP is accessible at port $HTTP_PORT"
    else
      echo "Node $i: HTTP is not accessible. Attempting repair..."
      repair_node $i
    fi
  done
}

repair_node() {
  local node_index=$1
  NODE_DIR="$BASE_DIR/data$node_index"
  HTTP_PORT=$((BASE_HTTP_PORT + node_index))
  AUTHRPC_PORT=$((BASE_AUTHRPC_PORT + node_index))
  NODE_PORT=$((BASE_IPC_PORT + node_index))

  echo "Stopping Node $node_index if running..."
  pkill -f "$NODE_DIR"

  echo "Reinitializing Node $node_index..."
  geth --datadir "$NODE_DIR" init "$GENESIS_FILE"

  echo "Restarting Node $node_index..."
  geth --datadir "$NODE_DIR" \
    --networkid 323671 \
    --http --http.addr "127.0.0.1" --http.port $HTTP_PORT \
    --http.api "eth,net,web3,personal,miner" \
    --ipcpath "$NODE_DIR/geth.ipc" \
    --authrpc.jwtsecret "$JWT_SECRET" \
    --mine --syncmode "full" \
    --unlock "$(cat $NODE_DIR/keystore/* | jq -r '.address')" \
    --password "$NODE_DIR/password.txt" \
    --port $NODE_PORT \
    --allow-insecure-unlock &

  echo "Node $node_index repaired and restarted."
}

stop_nodes() {
  echo "Stopping all nodes..."
  pkill -f geth
  echo "All nodes stopped."
}

auto_troubleshoot() {
  echo "Running automatic troubleshooting..."
  for i in $(seq 1 $NODE_COUNT); do
    HTTP_PORT=$((BASE_HTTP_PORT + i))
    NODE_DIR="$BASE_DIR/data$i"

    if ! [ -S "$NODE_DIR/geth.ipc" ]; then
      echo "Node $i: IPC missing. Repairing..."
      repair_node $i
    fi

    if ! curl -s "http://127.0.0.1:$HTTP_PORT" > /dev/null; then
      echo "Node $i: HTTP inaccessible. Repairing..."
      repair_node $i
    fi
  done
  echo "Troubleshooting complete."
}

# Menu
menu() {
  while true; do
    echo ""
    echo "========== QuranChain Node Manager =========="
    echo "1. Set up and start nodes"
    echo "2. Check node status"
    echo "3. Stop all nodes"
    echo "4. Run auto-troubleshooting and repair"
    echo "5. Exit"
    echo "============================================="
    read -p "Enter your choice: " choice

    case $choice in
      1) setup_nodes ;;
      2) check_nodes ;;
      3) stop_nodes ;;
      4) auto_troubleshoot ;;
      5) echo "Exiting..."; break ;;
      *) echo "Invalid choice, please try again." ;;
    esac
  done
}

# Run the menu
menu
