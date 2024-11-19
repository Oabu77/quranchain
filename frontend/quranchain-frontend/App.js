import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

function App() {
  const [walletAddress, setWalletAddress] = useState("");
  const [balance, setBalance] = useState(null);
  const [transferData, setTransferData] = useState({
    sender: "",
    recipient: "",
    amount: "",
    currency: "QuranCoin",
  });

  // Fetch wallet balance
  const fetchBalance = () => {
    if (!walletAddress) {
      alert("Please enter a wallet address");
      return;
    }
    axios
      .get(`${API_URL}/wallet/balance/${walletAddress}`)
      .then((response) => setBalance(response.data))
      .catch((error) => alert("Error fetching balance: " + error));
  };

  // Transfer funds
  const transferFunds = () => {
    axios
      .post(`${API_URL}/wallet/transfer`, transferData)
      .then((response) => alert(response.data.message))
      .catch((error) => alert("Error transferring funds: " + error));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>QuranChain with Muslim Wallet</h1>

      <section>
        <h2>Wallet Dashboard</h2>
        <input
          type="text"
          placeholder="Wallet Address"
          value={walletAddress}
          onChange={(e) => setWalletAddress(e.target.value)}
        />
        <button onClick={fetchBalance}>Check Balance</button>
        {balance && <p>Balance: {JSON.stringify(balance)}</p>}
      </section>

      <section>
        <h2>Transfer Funds</h2>
        <input
          type="text"
          placeholder="Sender Wallet"
          value={transferData.sender}
          onChange={(e) =>
            setTransferData({ ...transferData, sender: e.target.value })
          }
        />
        <input
          type="text"
          placeholder="Recipient Wallet"
          value={transferData.recipient}
          onChange={(e) =>
            setTransferData({ ...transferData, recipient: e.target.value })
          }
        />
        <input
          type="number"
          placeholder="Amount"
          value={transferData.amount}
          onChange={(e) =>
            setTransferData({ ...transferData, amount: e.target.value })
          }
        />
        <select
          value={transferData.currency}
          onChange={(e) =>
            setTransferData({ ...transferData, currency: e.target.value })
          }
        >
          <option value="QuranCoin">QuranCoin</option>
          <option value="MuslimCoin">MuslimCoin</option>
        </select>
        <button onClick={transferFunds}>Transfer</button>
      </section>
    </div>
  );
}

export default App;
