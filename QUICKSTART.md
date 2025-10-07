# ⚡ Quick Start Guide

**For technical users who want to get up and running fast.**

> **New to this?** Read `README.md` instead – it has detailed explanations for non-technical users.

---

## Prerequisites

- Python 3.8+
- ETH wallet with private key
- Deployed ERC-721 contract on ZORA (chain ID: 7777777)
- USDC/ETH for Arweave uploads
- ETH on ZORA chain for gas

---

## 30-Second Setup

**macOS/Linux:**
```bash
./setup.sh
cp .env.example .env
nano .env  # Fill in: ETH_PRIVATE_KEY, ZORA_CONTRACT_ADDRESS, WATCH_FOLDERS
python3 blockchain_bimbo.py
```

**Windows:**
```cmd
pip install -r requirements.txt
copy .env.example .env
notepad .env
python blockchain_bimbo.py
```

---

## Required Environment Variables

The script **fails fast** with clear errors if these are wrong:

```bash
# Required - 66 chars, starts with 0x
ETH_PRIVATE_KEY=0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef

# Required - 42 chars, starts with 0x
ZORA_CONTRACT_ADDRESS=0x1234567890123456789012345678901234567890

# Required - absolute paths, comma-separated
WATCH_FOLDERS=/absolute/path/to/folder1,/absolute/path/to/folder2

# Optional
ZORA_RPC_URL=https://rpc.zora.energy
ZORA_CHAIN_ID=7777777
EVERPAY_CURRENCY=usdc
RECEIPT_PRINTER_NAME=POS-80
```

---

## Contract Requirements

Your contract must have this function signature:

```solidity
function safeMint(address to, uint256 tokenId, string memory uri) public
```

**Using different signature?** Modify `ERC721_ABI` and `mint_on_zora()` in the Python script.

### Example Contract (OpenZeppelin)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract BlockchainBimboRelic is ERC721URIStorage, Ownable {
    constructor() ERC721("Blockchain Bimbo Relic", "BBR") Ownable(msg.sender) {}
    
    function safeMint(address to, uint256 tokenId, string memory uri) 
        public 
        onlyOwner 
    {
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }
}
```

Deploy to ZORA chain using Remix, Hardhat, or Foundry.

---

## Workflow

```
Image saved to watch folder
  ↓
upload_to_arweave(image_path, relic_id)
  → Uploads image via arseeding (EverPay)
  → Creates metadata.json with attributes
  → Uploads metadata via arseeding
  → Returns (image_url, token_uri)
  ↓
mint_on_zora(token_uri, token_id)
  → Connects to ZORA RPC
  → Calls contract.safeMint(wallet, token_id, token_uri)
  → Waits for transaction receipt
  → Returns (nft_url, tx_hash)
  ↓
generate_qr_code(nft_url)
  → Creates QR code image
  → Returns temp file path
  ↓
create_receipt(relic_id, timestamp, nft_url, qr_path)
  → Prints receipt text
  → Prints QR code image
  → Cleans up temp files
```

---

## Platform-Specific Commands

### Check Python Version

**macOS/Linux:**
```bash
python3 --version
```

**Windows:**
```cmd
python --version
```

### Install Dependencies

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

**Windows:**
```cmd
pip install -r requirements.txt
```

### Run Script

**macOS/Linux:**
```bash
python3 blockchain_bimbo.py
```

**Windows:**
```cmd
python blockchain_bimbo.py
```

### Find Printer Name

**macOS/Linux:**
```bash
lpstat -p -d
```

**Windows:**
```
Control Panel → Devices and Printers
```

### Test Printing

**macOS/Linux:**
```bash
echo "test" > test.txt
lpr -P "PrinterName" test.txt
```

**Windows:**
```
Right-click file → Print
```

---

## Funding Your Wallet

### Arweave Uploads (via EverPay)

**Check balance:**
```
https://everpay.io
```

**Supported currencies:**
- `eth` - Ethereum
- `usdc` - USD Coin

Set in `.env`:
```bash
EVERPAY_CURRENCY=usdc  # or eth
```

**Cost per image:** ~$0.01-0.10 (depends on size)

### ZORA Chain Gas

**Bridge ETH to ZORA:**
```
https://bridge.zora.energy
```

**Check balance:**
```
https://explorer.zora.energy
```

**Cost per mint:** ~$0.001-0.01

---

## Configuration Validation

The script validates on startup and **exits immediately** if config is wrong:

✅ **Pass:**
```
============================================================
✅ Configuration validated successfully!
============================================================
```

❌ **Fail:**
```
❌ CONFIGURATION ERRORS DETECTED
============================================================

The following configuration errors must be fixed:

  1. ETH_PRIVATE_KEY is not set
  2. ZORA_CONTRACT_ADDRESS has invalid length (40 chars, expected 42)
  3. WATCH_FOLDERS must use absolute paths: 'scans' is relative
```

**Fix errors and restart.**

---

## Customization

### Change NFT Metadata

Edit `upload_to_arweave()`:

```python
metadata = {
    "name": f"Custom Name #{relic_id}",
    "description": "Your description",
    "image": img_url,
    "attributes": [
        {"trait_type": "Custom Trait", "value": "Custom Value"}
    ]
}
```

### Change Receipt Text

Edit `create_receipt()`:

```python
receipt_text = f"""
Your custom receipt text here
RELIC: {relic_id}
DATE: {timestamp}
"""
```

### Use Different Mint Function

**Auto-incrementing IDs:**

```python
# Change ERC721_ABI
ERC721_ABI = [{
    "inputs": [
        {"internalType": "address", "name": "to", "type": "address"},
        {"internalType": "string", "name": "uri", "type": "string"}
    ],
    "name": "mint",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
}]

# Change mint_on_zora()
fn = contract.functions.mint(to_addr, token_uri)  # No tokenId
```

---

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'X'`

**Solution:**
```bash
pip3 install -r requirements.txt  # macOS/Linux
pip install -r requirements.txt   # Windows
```

### Web3 Connection Errors

**Problem:** `Failed to connect to ZORA RPC`

**Solutions:**
- Check internet connection
- Try alternative RPC:
  ```bash
  ZORA_RPC_URL=https://zora-mainnet.public.blastapi.io
  ```

### Transaction Fails

**Problem:** `ZORA mint failed: insufficient funds`

**Check ZORA balance:**
```bash
curl -X POST https://rpc.zora.energy \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["YOUR_ADDRESS","latest"],"id":1}'
```

**Bridge more ETH:** https://bridge.zora.energy

### Arweave Upload Fails

**Problem:** `Arweave upload failed`

**Check EverPay balance:** https://everpay.io

**Try different currency:**
```bash
EVERPAY_CURRENCY=eth  # instead of usdc
```

### Path Issues

**Problem:** `WATCH_FOLDERS must use absolute paths`

**Get absolute path:**

**macOS/Linux:**
```bash
cd ~/Desktop/scans
pwd  # Copy this output to .env
```

**Windows:**
```cmd
cd C:\Users\username\Desktop\scans
cd  # Shows full path
```

---

## Performance Optimization

### Speed

- Use fast internet (minimize Arweave upload time)
- Resize images to 1-2MB before scanning
- Keep ZORA explorer open to monitor transactions

### Cost

- Compress images (reduces Arweave cost)
- Batch performances (amortize setup time)
- Use 300dpi scans instead of 600dpi

### Reliability

- Test with 5-10 images before live performance
- Have backup wallet with extra funds
- Use mobile hotspot as internet backup
- Print backup receipts without QR codes

---

## Architecture

```
watchdog.Observer
  → ScanHandler.on_created()
    → display_image()          # Pygame fullscreen
    → upload_to_arweave()      # arseeding + everpay
    → mint_on_zora()           # web3.py
    → generate_qr_code()       # qrcode library
    → create_receipt()         # platform-specific printing
```

### Key Libraries

- `watchdog` - File system monitoring
- `arseeding` - Arweave uploads
- `everpay` - Payment layer
- `web3` - Ethereum interaction
- `eth-account` - Key management
- `qrcode` - QR generation
- `pygame` - Display
- `python-dotenv` - Config

---

## Production Checklist

- [ ] Contract deployed to ZORA
- [ ] Wallet funded (USDC/ETH + ZORA ETH)
- [ ] `.env` configured and validated
- [ ] Watch folders created with absolute paths
- [ ] Printer connected and tested
- [ ] 10 test runs completed successfully
- [ ] Backup funds available
- [ ] Internet backup ready (hotspot)
- [ ] Pre-printed backup receipts prepared

---

## Quick Reference

| Task | macOS/Linux | Windows |
|------|-------------|---------|
| Install deps | `pip3 install -r requirements.txt` | `pip install -r requirements.txt` |
| Run script | `python3 blockchain_bimbo.py` | `python blockchain_bimbo.py` |
| Stop script | `Ctrl+C` | `Ctrl+C` |
| Copy .env | `cp .env.example .env` | `copy .env.example .env` |
| Edit .env | `nano .env` | `notepad .env` |
| List printers | `lpstat -p -d` | Control Panel |
| Get full path | `pwd` | `cd` |

---

**Need more detail?** See `README.md` for non-technical explanations.
