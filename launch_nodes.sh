#!/bin/bash

for i in {1..99}
do
  DATA_DIR="/home/oem/QuranChain/data$i"
  HTTP_PORT=$((8544 + $i))
  WS_PORT=$((30302 + $i))
  IPC_PATH="$DATA_DIR/geth.ipc"
  JWT_SECRET="$DATA_DIR/jwtsecret"
  PASSWORD="Rick&Morty91!"

  mkdir -p $DATA_DIR

  echo "Launching Node $i..."
  geth --datadir $DATA_DIR --networkid 323671 \
    --http --http.addr "127.0.0.1" --http.port $HTTP_PORT \
    --http.api "eth,net,web3,personal,miner" \
    --ipcpath $IPC_PATH \
    --authrpc.jwtsecret $JWT_SECRET \
    --mine --syncmode "full" \
    --unlock "0x4aC734e6B856C0FFDDDCAD871892bfFe1d1A1cd4" --password <(echo $PASSWORD) \
    --port $WS_PORT --allow-insecure-unlock &
done
