#!/bin/bash

for i in {1..99}
do
  DATA_DIR="/home/oem/QuranChain/data$i"
  HTTP_PORT=$((8544 + $i))
  AUTHRPC_PORT=$((8550 + $i))
  P2P_PORT=$((30303 + $i))

  mkdir -p $DATA_DIR

  echo "Launching Node $i with HTTP port $HTTP_PORT and AUTHRPC port $AUTHRPC_PORT..."
  geth --datadir $DATA_DIR --networkid 323671 \
    --http --http.addr "127.0.0.1" --http.port $HTTP_PORT \
    --http.api "eth,net,web3,personal,miner" \
    --ipcpath $DATA_DIR/geth.ipc \
    --authrpc.jwtsecret $DATA_DIR/jwtsecret \
    --authrpc.port $AUTHRPC_PORT --port $P2P_PORT \
    --allow-insecure-unlock --mine &
done
