import os
import re
import time
import xrpl
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.requests import AccountNFTs
from xrpl.models.transactions import NFTokenCreateOffer, NFTokenAcceptOffer
from xrpl.transaction import submit_and_wait
from dotenv import load_dotenv
import subprocess

# Load environment variables
load_dotenv()

# Set up constants
XRP_REGEX = r'^r[1-9A-HJ-NP-Za-km-z]{25,34}$'  # Matches XRPL account addresses
TAXON_REGEX = r'^\d+$'  # Matches taxon (integer)

# Prompt user to select network
network = input("Select the network to use (1 for Testnet, 2 for Mainnet): ").strip()
if network == "1":
    client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
    print("Using Testnet")
elif network == "2":
    client = JsonRpcClient("https://xrplcluster.com")
    print("Using Mainnet")
else:
    print("Invalid selection. Exiting.")
    exit()

# Check if the seed is updated in the .env file
if not os.getenv("SEED") or os.getenv("SEED") == "your_seed_here":
    update_seed = input("The .env file has not been configured with your seed phrase. Would you like to update it now? (Y/N): ").strip().lower()
    if update_seed == "y":
        print("Opening .env file in nano editor. Please update your seed phrase.")
        subprocess.call(["nano", ".env"])
    else:
        print("Please update the .env file with your seed phrase and run the script again.")
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

# Prompt for issuer address and validate format
issuer_address = input("Enter the issuer address of the NFTs you'd like to send: ").strip()
if not re.match(XRP_REGEX, issuer_address):
    print("Invalid issuer address format. Exiting.")
    exit()
print(f"Issuer address validated: {issuer_address}")

# Prompt for taxon and validate format
taxon = input("Enter the Taxon of the NFT collection you'd like to send: ").strip()
if not re.match(TAXON_REGEX, taxon):
    print("Invalid taxon format. Exiting.")
    exit()
print(f"NFT Taxon validated: {taxon}")

# Prompt for recipient address and validate format
recipient_address = input("Enter the address you'd like to send the NFTs to: ").strip()
if not re.match(XRP_REGEX, recipient_address):
    print("Invalid recipient address format. Exiting.")
    exit()
print(f"Recipient address validated: {recipient_address}")

# Ask if the user wants to test with one NFT
test_one = input("Would you like to send 1 NFT as a test before sending all? (Y/N): ").strip().lower()
if test_one == "y":
    print("User selected to test with 1 NFT before sending all.")

# Function to fetch NFTs matching the issuer and taxon
def fetch_nfts():
    print(f"Fetching NFTs for account {address}...")
    account_nfts = AccountNFTs(account=address)
    response = client.request(account_nfts)
    if "account_nfts" in response.result:
        print(f"Found {len(response.result['account_nfts'])} NFTs.")
        print("NFTs fetched:", response.result.get("account_nfts", []))
    else:
        print("No NFTs found.")
    return [
    nft for nft in response.result.get("account_nfts", [])
    if nft.get("Issuer") == issuer_address and nft.get("NFTokenTaxon") == int(taxon)
]


# Function to transfer an NFT
def transfer_nft(nft):
    print(f"Creating offer to transfer NFT {nft['NFTokenID']} to {recipient_address}...")
    offer_create_tx = NFTokenCreateOffer(
        account=address,
        nftoken_id=nft["NFTokenID"],
        amount="0",
        flags=1,
        destination=recipient_address
    )
    try:
        response = submit_and_wait(offer_create_tx, client, wallet)
        offer_index = response.result.get("offer_index")
        print(f"Offer created with index: {offer_index}")
    except Exception as e:
        print(f"Failed to create offer for NFT {nft['NFTokenID']}: {e}")
        return

# Fetch NFTs to send
nfts_to_send = fetch_nfts()
if not nfts_to_send:
    print("No NFTs found matching the specified issuer and taxon.")
    exit()

print(f"Total NFTs found for transfer: {len(nfts_to_send)}")

# Send one NFT for testing if chosen
if test_one == "y" and nfts_to_send:
    print("Sending one NFT as a test.")
    transfer_nft(nfts_to_send[0])
    nfts_to_send = nfts_to_send[1:]  # Remove the sent NFT from the list

# Send remaining NFTs
print("Starting transfer of remaining NFTs.")
for nft in nfts_to_send:
    print(f"Sending NFT {nft['NFTokenID']} to {recipient_address}")
    transfer_nft(nft)
    time.sleep(1)  # Optional delay between transfers

print("All NFTs have been sent.")
