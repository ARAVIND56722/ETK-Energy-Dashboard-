# ETK Energy Dashboard 

A Streamlit-based dashboard for simulating and managing decentralized peer-to-peer (P2P) energy trading using the **EnergyToken (ETK)** smart contract on the **Sepolia Ethereum testnet**.

# Features

- 🔗 Blockchain Integration: Connects directly to a deployed ERC-20 smart contract on Sepolia.
- ⚙️ Send ETK Tokens: Transfer tokens between addresses with real-time transaction feedback.
- 💰 Live Token Balance: Check ETK token balances of House A, House B, or any wallet.
- 📜 Transaction History: View past energy trades and transfers on the dashboard.
- 🧪 Testnet Deployment: Safe experimentation with Ethereum's Sepolia testnet.

## 🛠️ Tech Stack

- Frontend: Streamlit
- Smart Contract: Solidity (ERC-20)
- Blockchain API: Web3.py + Infura (Sepolia)
- Wallets: MetaMask integration (testnet)

##  How to Run

1. **Clone the Repository**

``bash
git clone https://github.com/ARAVIND56722/ETK-Energy-Dashboard-.git
cd ETK-Energy-Dashboard-

## Install Dependencies
pip install -r requirements.txt


## Notes
This is a testnet-only project. Do not use real ETH or live wallet keys.

All token transfers are simulated using Sepolia ETH and the EnergyToken (ETK).

📄 License
MIT License — feel free to use and modify.

## Run the app
Bash 
streamlit run app.py
