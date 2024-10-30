# Transfer-XRPL-NFTs
This script automates the transfer of NFTs on the XRP Ledger (XRPL) from one account to another. The script allows you to specify an NFT issuer address and taxon, find all matching NFTs in your wallet, and transfer them to a recipient address.

Features
Connects to either XRPL Testnet or Mainnet.
Uses xrpl-py to fetch NFTs from a specified issuer and taxon.
Transfers all matching NFTs from the specified account to a recipient.
Optionally allows testing with a single NFT before sending all.
Validates all input data, including account addresses and taxon.
Loads sensitive information like seed phrase from an environment file.

## Prerequisites
- Python 3.7 or higher
- `xrpl-py` library
- `dotenv` for loading environment variables

## Installation
1. Clone the repository:
```bash
git clone https://github.com/joshuahamsa/XRPL-NFT-Auto-Transfer.git
cd XRPL-NFT-Auto-Transfer
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Configure the `.env` file
- Create a `.env` file in the root directory with the following line:
```
SEED=your_seed_here
```
- Alternatively, this can be done at runtime.
- Make sure you have access to your account's seed phrase. If you only have your Xaman Secret Numbers written down, they can be converted using Wietse's Tool: https://github.com/WietseWind/secret-numbers-to-family-seed .

## Usage
1. Run the script
```bash
python3 transfer.py
```
2. Follow the prompts:
- Select the network (1 for Testnet, 2 for Mainnet).
- Enter the issuer address of the NFTs you'd like to send.
- Enter the NFT taxon to filter NFTs by.
- Enter the recipient address for the NFTs.
- Choose whether to test by sending a single NFT first.
3. Transfer Process:
- The script will fetch NFTs that match the specified issuer and taxon.
- If testing is enabled, it will transfer one NFT as a test.
- After testing, it will transfer all remaining NFTs.

## Example Run
```vbnet
Select the network to use (1 for Testnet, 2 for Mainnet): 1
Using Testnet
Enter the issuer address of the NFTs you'd like to send: rExampleIssuerAddress
Issuer address validated: rExampleIssuerAddress
Enter the Taxon of the NFT collection you'd like to send: 12345
NFT Taxon validated: 12345
Enter the address you'd like to send the NFTs to: rRecipientAddress
Recipient address validated: rRecipientAddress
Would you like to send 1 NFT as a test before sending all? (Y/N): y
Fetching NFTs for account rYourAddress...
Found 3 NFTs.
Creating offer to transfer NFT 000... to rRecipientAddress...
Offer created with index: 123456789
Sending one NFT as a test.
Starting transfer of remaining NFTs.
Sending NFT 001... to rRecipientAddress...
All NFTs have been sent.
```

## Important Notes
- **Environment Variables:** Ensure that `SEED` is securely set in the `.env` file to avoid exposing your wallet’s seed phrase.
- **Rate Limiting:** Consider adding delays or rate-limiting if sending a large number of NFTs on the XRPL to avoid hitting rate limits on public nodes.
- **Use Testnet for Testing:** For initial testing, it is recommended to use Testnet.