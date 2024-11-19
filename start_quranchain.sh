#!/bin/bash
echo "Starting QuranChain nodes..."

# Start Geth Node
geth --datadir "/home/oem/QuranChain/data" --networkid 323671      --http --http.addr 0.0.0.0 --http.port 8545      --http.api eth,net,web3,personal,miner      --authrpc.port 8551 --authrpc.addr 0.0.0.0      --authrpc.jwtsecret "/home/oem/QuranChain/data/jwtsecret"      --mine --syncmode full      --unlock "0x4aC734e6B856C0FFDDDCAD871892bfFe1d1A1cd4" --password "/home/oem/QuranChain/password.txt"      --allow-insecure-unlock      --port 30303 > "/home/oem/QuranChain/logs/geth.log" 2>&1 &

# Start Prysm Beacon Chain
"/home/oem/QuranChain/prysm/dist/beacon-chain-v5.1.2-linux-amd64" --datadir="/home/oem/QuranChain/data/beacon"     --execution-endpoint=http://127.0.0.1:8551     --jwt-secret="/home/oem/QuranChain/data/jwtsecret"     --suggested-fee-recipient="0x4aC734e6B856C0FFDDDCAD871892bfFe1d1A1cd4"     --monitoring-host=0.0.0.0     --monitoring-port=5052 > "/home/oem/QuranChain/logs/beacon.log" 2>&1 &
