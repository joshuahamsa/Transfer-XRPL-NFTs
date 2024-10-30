import os
import re
import time
import xrpl
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.requests import AccountNFTs
from xrpl.models.transactions import NFTokenCreateOffe>
from xrpl.transaction import submit_and_wait
from dotenv import load_dotenv
import subprocess

# Load environment variables
load_dotenv()

# Set up constants
XRP_REGEX = r'^r[1-9A-HJ-NP-Za-km-z]{25,34}$'  # Match>
TAXON_REGEX = r'^\d+$'  # Matches taxon (integer)

# Prompt user to select network
network = input("Select the network to use (1 for Test>
if network == "1":
    client = JsonRpcClient("https://s.altnet.rippletes>
    print("Using Testnet")
elif network == "2":
    client = JsonRpcClient("https://xrplcluster.com")
    print("Using Mainnet")
else:
    print("Invalid selection. Exiting.")
    exit()

# Check if the seed is updated in the .env file
if not os.getenv("SEED") or os.getenv("SEED") == "your>
    update_seed = input("The .env file has not been co>
    if update_seed == "y":
        print("Opening .env file in nano editor. Pleas>
        subprocess.call(["nano", ".env"])
    else:
        print("Please update the .env file with your s>
        exit()

# Reload environment variables after potential update
load_dotenv()
seed = os.getenv("SEED")

# Validate seed
if not seed or seed == "your_seed_here":
    print("Seed not properly set in .env. Exiting.")
    exit()

# Initialize wallet
wallet = Wallet.from_seed(seed)
address = wallet.classic_address
print(f"Using wallet address: {address}")

  GNU nano 5.7          transfer.py                    

# Prompt for issuer address and validate format
issuer_address = input("Enter the issuer address of th>
if not re.match(XRP_REGEX, issuer_address):
    print("Invalid issuer address format. Exiting.")
    exit()
print(f"Issuer address validated: {issuer_address}")

# Prompt for taxon and validate format
taxon = input("Enter the Taxon of the NFT collection y>
if not re.match(TAXON_REGEX, taxon):
    print("Invalid taxon format. Exiting.")
    exit()
print(f"NFT Taxon validated: {taxon}")

# Prompt for recipient address and validate format
recipient_address = input("Enter the address you'd lik>
if not re.match(XRP_REGEX, recipient_address):
    print("Invalid recipient address format. Exiting.")
    exit()
print(f"Recipient address validated: {recipient_addres>

# Ask if the user wants to test with one NFT
test_one = input("Would you like to send 1 NFT as a te>
if test_one == "y":
    print("User selected to test with 1 NFT before sen>

# Function to fetch NFTs matching the issuer and taxon
def fetch_nfts():
    print(f"Fetching NFTs for account {address}...")
    account_nfts = AccountNFTs(account=address)
    response = client.request(account_nfts)
    if "account_nfts" in response.result:
        print(f"Found {len(response.result['account_nf>
    else:
        print("No NFTs found.")
    return [nft for nft in response.result.get("accoun>

# Function to transfer an NFT
def transfer_nft(nft):
    print(f"Creating offer to transfer NFT {nft['NFTok>
    offer_create_tx = NFTokenCreateOffer(
        account=address,
        owner=address,
        nft_id=nft["NFTokenID"],
        amount="0",
        destination=recipient_address
    )
    try:
        response = submit_and_wait(offer_create_tx, cl>
        offer_index = response.result.get("offer_index>
        print(f"Offer created with index: {offer_index>
  except Exception as e:
        print(f"Failed to create offer for NFT {nft['N>
        return

# Fetch NFTs to send
nfts_to_send = fetch_nfts()
