import streamlit as st
import pandas as pd
import numpy as np
import random
import hashlib
import datetime

from web3 import Web3

# --- Blockchain Connection Settings ---
infura_url = "https://sepolia.infura.io/v3/9e4d70e97c014cf390a0e7611dc23d59"
contract_address = "0x8d101f2861539DC7DE912136bAE001768739F18e"
wallet_a = "0x976Bc2B59aaBd514a38e32ec6C5D37aF90AEb2Fa"
wallet_b = "0xB55A9452757fF1Dad60B6fdEB7fEa5fF281d60C5"

# --- Replace this with your actual ABI (as a list, not a string) ---
contract_abi = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "initialSupply",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "allowance",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "needed",
                "type": "uint256"
            }
        ],
        "name": "ERC20InsufficientAllowance",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "balance",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "needed",
                "type": "uint256"
            }
        ],
        "name": "ERC20InsufficientBalance",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "approver",
                "type": "address"
            }
        ],
        "name": "ERC20InvalidApprover",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "receiver",
                "type": "address"
            }
        ],
        "name": "ERC20InvalidReceiver",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sender",
                "type": "address"
            }
        ],
        "name": "ERC20InvalidSender",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            }
        ],
        "name": "ERC20InvalidSpender",
        "type": "error"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]



# Connect to Sepolia
w3 = Web3(Web3.HTTPProvider(infura_url))
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

@st.cache_data(ttl=60, show_spinner=False)

def fetch_transfer_events(start_block=0, end_block=None):
    try:
        if end_block is None:
            end_block = w3.eth.block_number  # ✅ NO parentheses here

        transfer_event_signature = "0x" + w3.keccak(text="Transfer(address,address,uint256)").hex()


        logs = w3.eth.get_logs({
            "fromBlock": start_block,
            "toBlock": end_block,
            "address": Web3.to_checksum_address(contract_address),
            "topics": [transfer_event_signature]
        })

        decoded_events = []
        for log in logs:
            decoded = contract.events.Transfer().process_log(log)
            decoded_events.append({
                "Tx Hash": log.transactionHash.hex(),
                "From": decoded['args']['from'],
                "To": decoded['args']['to'],
                "Amount (ETK)": decoded['args']['value'] / 10**18,
                "Block": log.blockNumber
            })

        return decoded_events

    except Exception as e:
        st.error(f"Failed to fetch events: {e}")
        return []




# Block class: represents each record/unit in the chain
class Block:
    def __init__(self, index, data, previous_hash):  # <-- Fix here
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()


    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# Blockchain class: manages the chain, adding & validating blocks
class Blockchain:
    def __init__(self):  # <-- Fix here
        self.chain = []
        self.create_genesis_block()


    def create_genesis_block(self):
        # The first block, with index=0 and arbitrary data
        genesis_block = Block(0, {"info": "Genesis Block"}, "0")
        self.chain.append(genesis_block)

    def add_block(self, data):
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), data, prev_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            cur = self.chain[i]
            prev = self.chain[i-1]
            if cur.hash != cur.compute_hash():
                return False
            if cur.previous_hash != prev.hash:
                return False
        return True


st.set_page_config(page_title="SunSplit: Energy Sharing Dashboard", layout="centered")

st.title("☀ ETKGrid:  Peer-to-Peer Token Sharing with Live Blockchain Dashboard ")

st.markdown("""
Upload your solar data or try the default.  
- *Surplus* homes will 'sell' energy.  
- *Deficit* homes will 'buy' energy.  
- The dashboard simulates blockchain-like trading and credit tokens.
""")

# 1. Data Upload or Use Demo Data
demo_data = pd.DataFrame({
    'House': ['A', 'B', 'C', 'D'],
    'Generated': [15, 10, 12, 8],
    'Consumed': [10, 12, 6, 9],
    'Tokens':[0,0,0,0]
})

uploaded_file = st.file_uploader("Upload an energy_data.csv", type=['csv'])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded!")
else:
    st.info("No file uploaded. Using demo data.")
    df = demo_data.copy()

df['Surplus'] = df['Generated'] - df['Consumed']
blockchain = Blockchain()
st.subheader("🌞 Household Energy Summary")
st.dataframe(df.drop(columns=["Tokens"]), use_container_width=True)


# 2. Surplus and Deficit Table
surplus_df = df[df['Surplus'] > 0].reset_index(drop=True)
deficit_df = df[df['Surplus'] < 0].reset_index(drop=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### ⚡ Surplus Houses")
    st.dataframe(surplus_df.drop(columns=["Tokens"]))

with col2:
    st.markdown("#### 🔌 Deficit Houses")
    st.dataframe(deficit_df.drop(columns=["Tokens"]))


# 3. Simulated P2P Trading (blockchain-like ledger)
st.subheader("🧾 Simulated 'Blockchain' Trading Ledger")
transactions = []
token_balances = {house: 0 for house in df['House']}

for i, row_s in surplus_df.iterrows():
    for j, row_d in deficit_df.iterrows():
        send = surplus_df.at[i, 'Surplus']
        need = -deficit_df.at[j, 'Surplus']
        if send > 0 and need > 0:
            amt = min(send, need)
            fake_hash = f"0x{random.getrandbits(64):016x}"
            transaction = {
                'Block': 1000 + len(transactions),
                'Txn Hash': fake_hash,
                'Sender': row_s['House'],
                'Receiver': row_d['House'],
                'Energy (kWh)': amt,
                'Tokens need to Exchange': amt,
            }
            transactions.append(transaction)
            surplus_df.at[i, 'Surplus'] -= amt
            deficit_df.at[j, 'Surplus'] += amt
            token_balances[row_s['House']] += amt
            token_balances[row_d['House']] -= amt
            
            
            trade_data = {
    "sender": row_s['House'],       # e.g., "A"
    "receiver": row_d['House'],     # e.g., "B"
    "energy": amt,
    "tokens": amt
}
blockchain.add_block(trade_data)   # ✅ Add this line
 

chain_data = [{
    "Index": block.index,
    "Timestamp": block.timestamp,
    "Sender": block.data.get("sender"),
    "Receiver": block.data.get("receiver"),
    "Energy": block.data.get("energy"),
    "Tokens": block.data.get("tokens"),
    "Prev Hash": block.previous_hash[:10] + "..." if block.previous_hash else "",
    "Hash": block.hash[:10] + "..."
} for block in blockchain.chain]

st.subheader("Blockchain Ledger")
st.dataframe(pd.DataFrame(chain_data))



if st.button("Validate Blockchain Integrity"):
    if blockchain.is_chain_valid():
        st.success("✅ Blockchain is valid!")
    else:
        st.error("❌ Blockchain integrity lost!")



if transactions:
    st.write(pd.DataFrame(transactions))
else:
    st.info("No possible trades found in this data.")

# 4. Token Balance Visualization
st.subheader("🪙 Live ETK Token Balances from Blockchain")

try:
    balance_a = contract.functions.balanceOf(wallet_a).call() / (10 ** 18)
    balance_b = contract.functions.balanceOf(wallet_b).call() / (10 ** 18)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("House A Balance", f"{balance_a:.2f} ETK")
    with col2:
        st.metric("House B Balance", f"{balance_b:.2f} ETK")

except Exception as e:
    st.error(f"Failed to fetch token balances: {e}")




st.caption("Peer-to-peer energy trading demo. In a full system, this ledger and credits could be stored on a real blockchain.")
st.subheader("🔁 Send ETK Tokens")

sender_address = st.text_input("Sender Wallet Address", value=wallet_a)
receiver_address = st.text_input("Receiver Wallet Address", value=wallet_b)
amount = st.number_input("Amount of ETK to Send", min_value=0.0, format="%.2f")
private_key = st.text_input("Private Key of Sender", type="password")

if st.button("Send ETK"):
    if not all([sender_address, receiver_address, amount, private_key]):
        st.error("Please fill in all fields.")
    else:
        try:
            amount_wei = int(amount * 10**18)
            nonce = w3.eth.get_transaction_count(sender_address)

            txn = contract.functions.transfer(
                receiver_address, amount_wei
            ).build_transaction({
                'chainId': 11155111,  # Sepolia
                'gas': 100000,
                'gasPrice': w3.eth.gas_price,
                'nonce': nonce,
            })

            signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

            st.success(f"✅ Transaction sent! Tx hash: {tx_hash.hex()}")
           

        except Exception as e:
            st.error(f"❌ Failed to send transaction: {e}")
            # 🧾 Blockchain Transfer History Section
st.markdown("---")
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=15000, limit=None, key="transfer_refresh")

st.subheader("🔁 ETK Transaction History")



latest_block = w3.eth.block_number
events = fetch_transfer_events(start_block=max(0, latest_block - 3000), end_block=latest_block)


if events:
    df = pd.DataFrame(events)
    st.dataframe(df[::-1], use_container_width=True)
else:
    st.info("No transactions found yet.")