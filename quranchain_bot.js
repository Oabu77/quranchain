const readline = require("readline");
const ethers = require("ethers");


// Initialize provider and wallet
const INFURA_URL = "https://polygon-mumbai.infura.io/v3/PViq881gKow-v2w_3asYVc4A8eY_kMOI";
const PRIVATE_KEY = "0xecb8c71be8f62f1bd6dbffb283a29158c49d4e564b936c0c94e9ed6c0c0745d3";
const CONTRACT_ADDRESS = "0xF6F117379D59a87c25B8D1658162A2bb2598aB80"; // Example deployed address
const CONTRACT_ABI = [
    // Replace this with the actual ABI of your contract
];

const provider = new ethers.JsonRpcProvider(INFURA_URL);
const wallet = new ethers.Wallet(PRIVATE_KEY, provider);
const contract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, wallet);

// Set up user interface
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function showMenu() {
    console.log("\nQuranChain Manager Bot:");
    console.log("1. Check Node Status");
    console.log("2. Query Smart Contract");
    console.log("3. Send Transaction");
    console.log("4. Exit");
    rl.question("\nChoose an option: ", handleUserChoice);
}

async function handleUserChoice(choice) {
    switch (choice.trim()) {
        case "1":
            console.log("\nChecking node status...");
            try {
                const blockNumber = await provider.getBlockNumber();
                console.log(`Node is active. Current block number: ${blockNumber}`);
            } catch (error) {
                console.error("Failed to connect to the node:", error.message);
            }
            break;
        case "2":
            rl.question("\nEnter the function name to query: ", async (functionName) => {
                try {
                    const result = await contract[functionName]();
                    console.log(`Result from ${functionName}:`, result);
                } catch (error) {
                    console.error("Error querying contract:", error.message);
                }
                showMenu();
            });
            return;
        case "3":
            rl.question("\nEnter the function name to call: ", async (functionName) => {
                rl.question("Enter parameters (comma-separated): ", async (params) => {
                    try {
                        const paramArray = params.split(",").map((p) => p.trim());
                        const tx = await contract[functionName](...paramArray);
                        console.log("Transaction sent. Hash:", tx.hash);
                        await tx.wait();
                        console.log("Transaction confirmed!");
                    } catch (error) {
                        console.error("Error sending transaction:", error.message);
                    }
                    showMenu();
                });
            });
            return;
        case "4":
            console.log("\nExiting QuranChain Manager Bot. Goodbye!");
            rl.close();
            return;
        default:
            console.log("\nInvalid choice. Please try again.");
    }
    showMenu();
}

showMenu();
