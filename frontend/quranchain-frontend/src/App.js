import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

function App() {
  const [blockchain, setBlockchain] = useState([]);
  const [miner, setMiner] = useState("");
  const [surah, setSurah] = useState("");
  const [ayahs, setAyahs] = useState("");

  // Fetch blockchain data
  useEffect(() => {
    axios.get(`${API_URL}/blockchain`)
      .then((response) => setBlockchain(response.data.chain))
      .catch((error) => console.error("Error fetching blockchain:", error));
  }, []);

  // Submit a new reward
  const submitReward = () => {
    const reward = { miner, surah: parseInt(surah), ayahs: parseInt(ayahs) };
    axios.post(`${API_URL}/submit_reward`, reward)
      .then((response) => {
        alert(response.data.message);
        setMiner("");
        setSurah("");
        setAyahs("");
      })
      .catch((error) => alert("Error submitting reward: " + error));
  };

  // Process rewards into a block
  const processRewards = () => {
    axios.post(`${API_URL}/process_rewards`)
      .then((response) => alert(response.data.message))
      .catch((error) => alert("Error processing rewards: " + error));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>QuranChain</h1>

      <section>
        <h2>Submit Reward</h2>
        <input
          type="text"
          placeholder="Miner Address"
          value={miner}
          onChange={(e) => setMiner(e.target.value)}
        />
        <input
          type="text"
          placeholder="Surah Number"
          value={surah}
          onChange={(e) => setSurah(e.target.value)}
        />
        <input
          type="text"
          placeholder="Ayah Count"
          value={ayahs}
          onChange={(e) => setAyahs(e.target.value)}
        />
        <button onClick={submitReward}>Submit Reward</button>
      </section>

      <section>
        <h2>Process Rewards</h2>
        <button onClick={processRewards}>Process Pending Rewards</button>
      </section>

      <section>
        <h2>Blockchain</h2>
        {blockchain.map((block, index) => (
          <div key={index} style={{ marginBottom: "20px", padding: "10px", border: "1px solid #ccc" }}>
            <h3>Block {block.index}</h3>
            <p><b>Type:</b> {block.data.type || "Generic"}</p>
            <p><b>Hash:</b> {block.hash}</p>
          </div>
        ))}
      </section>
    </div>
  );
}

export default App;
