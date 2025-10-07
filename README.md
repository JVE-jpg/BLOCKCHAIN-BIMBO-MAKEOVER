# 🎨 Blockchain Bimbo Makeover

*A performance art project by Julie van Essen*

---

## What Is This?

**Blockchain Bimbo Makeover** is a provocative performance art piece that transforms your face into a permanent digital artifact on the blockchain. Created by artist **Julie van Essen**, this project explores the uncomfortable relationship between identity, technology, and value in the digital age.

When you participate in a Blockchain Bimbo Makeover session:
1. Your face is scanned
2. The image is uploaded to Arweave (permanent storage that never disappears)
3. An NFT (digital certificate) is created on the ZORA blockchain
4. You receive a printed receipt with a QR code to view your "digital relic"

The project asks: *What happens when we turn ourselves into blockchain commodities? Can art exist without value? And what does it mean to be permanently archived in code?*

### About the Artist

**Julie van Essen** is a performance artist working at the intersection of technology, identity, and economics. Through Blockchain Bimbo Makeover, she challenges the crypto world's obsession with value and permanence by creating NFTs that are explicitly "minted without value" – yet the blockchain refuses this intention, always ready to assign a price.

Her work transforms the gallery into a space of contradiction: participants become digital relics, their presence archived forever, while simultaneously critiquing the very systems that make this archival possible.

---

## For Artists & Performers

This repository contains the complete technical implementation of the Blockchain Bimbo Makeover system. Whether you're Julie setting up for a performance, or another artist inspired by this work, this guide will help you run your own sessions.

**You don't need to be a programmer** – this guide explains everything step by step, for both technical and non-technical users.

---

## What You'll Need

### Hardware
- A computer (Windows, Mac, or Linux)
- A scanner or camera to capture face images
- A thermal receipt printer (optional but recommended)
- Internet connection

### Software
- Python 3.8 or newer (free programming language)
- All the code in this repository (you're already here!)

### Blockchain Requirements
- An Ethereum wallet with a private key
- Some cryptocurrency:
  - **USDC or ETH** (about $10-20) for storing images on Arweave
  - **ETH on ZORA chain** (about 0.01 ETH, ~$30-40) for creating NFTs
- A deployed smart contract on ZORA blockchain

**Don't worry if this sounds complicated** – we'll walk through everything below.

---

## Installation Guide

### Step 1: Install Python

#### On macOS:
```bash
# Check if Python is already installed
python3 --version

# If not installed, download from python.org or use Homebrew:
brew install python3
```

#### On Windows:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
4. Open Command Prompt and verify:
```cmd
python --version
```

#### On Linux:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip
```

### Step 2: Download the Project

#### On macOS/Linux:
```bash
# Clone with git (if you have it)
git clone <repository-url>
cd BLOCKCHAIN-BIMBO-MAKEOVER

# Or download ZIP from GitHub and extract it
```

#### On Windows:
1. Download the ZIP file from GitHub
2. Right-click → Extract All
3. Open Command Prompt and navigate to the folder:
```cmd
cd C:\path\to\BLOCKCHAIN-BIMBO-MAKEOVER
```

### Step 3: Install Dependencies

#### On macOS/Linux:
```bash
# Quick install with setup script
chmod +x setup.sh
./setup.sh

# Or manual install
pip3 install -r requirements.txt
```

#### On Windows:
```cmd
pip install -r requirements.txt
```

**This will take a few minutes** as it downloads all necessary libraries.

### Step 4: Configure Your Settings

You need to create a file called `.env` that contains your private settings.

#### On macOS/Linux:
```bash
# Copy the example file
cp .env.example .env

# Edit with your preferred editor
nano .env
# or
open .env
```

#### On Windows:
```cmd
copy .env.example .env
notepad .env
```

Now fill in these **required** settings:

```bash
# Your Ethereum wallet private key (starts with 0x, 66 characters total)
ETH_PRIVATE_KEY=0x1234567890abcdef...

# Your ZORA smart contract address (starts with 0x, 42 characters total)
ZORA_CONTRACT_ADDRESS=0xABCD1234...

# Folder(s) to watch for new scans (full path, comma-separated for multiple)
# macOS/Linux example:
WATCH_FOLDERS=/Users/julie/Desktop/scans
# Windows example:
WATCH_FOLDERS=C:\Users\julie\Desktop\scans
```

**⚠️ CRITICAL**: The script will check these settings and refuse to start if anything is wrong. You'll get clear error messages telling you exactly what to fix.

---

## Getting Your Blockchain Setup

### 1. Create an Ethereum Wallet

If you don't have one:
- Install [MetaMask](https://metamask.io) browser extension
- Create a new wallet
- **Save your seed phrase safely!**
- Go to Settings → Security & Privacy → Show Private Key
- Copy your private key (starts with `0x`)

### 2. Get a ZORA Smart Contract

You need an NFT contract deployed on ZORA chain.

**Option A: Use ZORA's UI** (Easiest)
1. Go to [zora.co/create](https://zora.co/create)
2. Connect your wallet
3. Create a new collection
4. Copy the contract address

**Option B: Deploy Your Own** (Technical)
- See `QUICKSTART.md` for the smart contract code
- Deploy using Remix or Hardhat
- Make sure it has a `safeMint(address, tokenId, uri)` function

### 3. Fund Your Wallet

#### For Arweave uploads:
You need USDC or ETH on Ethereum mainnet.
- Buy on any exchange (Coinbase, Kraken, etc.)
- Send to your wallet address
- About $10-20 covers 50-200 images

#### For ZORA minting:
You need ETH on ZORA blockchain (chain ID: 7777777).

**On macOS/Linux/Windows:**
1. Go to [bridge.zora.energy](https://bridge.zora.energy)
2. Connect your wallet
3. Bridge 0.01 ETH from Ethereum mainnet to ZORA
4. Wait ~2 minutes for the transaction

---

## Running the System

### Start the Application

#### On macOS/Linux:
```bash
python3 blockchain_bimbo.py
```

#### On Windows:
```cmd
python blockchain_bimbo.py
```

### What You'll See

If everything is configured correctly:
```
============================================================
🎨 BLOCKCHAIN BIMBO MAKEOVER - DIGITAL RELIC GENERATOR
============================================================

🖥️  Operating System: Darwin
✅ ETH wallet: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
✅ ZORA contract: 0x1234567890123456789012345678901234567890
✅ Watch folders: 1 configured
🖨️  Printer: POS-80
⛓️  ZORA Chain ID: 7777777
🌐 ZORA RPC: https://rpc.zora.energy
💰 Arweave payment: USDC

============================================================
✅ Configuration validated successfully!
============================================================

🚀 Starting file watcher...
   Drop scanned images into watched folders to create relics!
   Press Ctrl+C to stop
```

**If something is wrong**, you'll get a clear error message:
```
❌ CONFIGURATION ERRORS DETECTED
============================================================

The following configuration errors must be fixed:

  1. ETH_PRIVATE_KEY is not set
  2. WATCH_FOLDERS must use absolute paths: 'scans' is relative

============================================================
📝 HOW TO FIX:
...
```

Fix the errors and try again.

### During the Performance

1. **Scan a participant's face**
2. **Save the image** to your watched folder (as `.jpg`, `.jpeg`, or `.png`)
3. **The system automatically**:
   - Displays the image fullscreen
   - Uploads to Arweave (~10-30 seconds)
   - Mints the NFT on ZORA (~5-15 seconds)  
   - Generates a QR code
   - Prints a receipt

The participant receives a receipt with:
- Poetic text about digital relics and value
- QR code to view their NFT
- Relic number and timestamp

### Stop the System

Press `Ctrl+C` (both Mac and Windows)

---

## Setting Up Your Receipt Printer

### Find Your Printer Name

#### On macOS/Linux:
```bash
lpstat -p -d
```

#### On Windows:
1. Open Control Panel
2. Go to "Devices and Printers"
3. Find your thermal printer name

### Update Your Configuration

Edit `.env` and set:
```
RECEIPT_PRINTER_NAME=YourPrinterNameHere
```

### Testing

The script will attempt to print receipts automatically. If printing fails:
- Check printer is connected and turned on
- Verify printer name matches exactly
- Check printer has paper
- Try printing a test page from your OS first

---

## Troubleshooting

### "CONFIGURATION ERRORS DETECTED"

The script found problems with your `.env` file. Read the error messages carefully:

- **"ETH_PRIVATE_KEY is not set"** → Add your private key to `.env`
- **"ETH_PRIVATE_KEY must start with '0x'"** → Your key format is wrong
- **"ETH_PRIVATE_KEY has invalid length"** → Should be 66 characters (0x + 64 hex digits)
- **"ZORA_CONTRACT_ADDRESS is not set"** → Add your contract address to `.env`
- **"WATCH_FOLDERS must use absolute paths"** → Use full paths like `/Users/name/folder` not `~/folder`

### "Arweave upload failed"

**Check your balance:**
- Do you have USDC or ETH in your wallet?
- Visit [everpay.io](https://everpay.io) to check EverPay balance

**Try switching currency:**
In `.env`, change:
```
EVERPAY_CURRENCY=eth
```
instead of `usdc`

### "ZORA mint failed"

**Check your ZORA balance:**
- Go to [explorer.zora.energy](https://explorer.zora.energy)
- Search for your wallet address
- Make sure you have ETH on ZORA chain (not mainnet!)

**Check contract permissions:**
- Is your wallet authorized to mint on this contract?
- Does the contract owner match your wallet?

### Images Not Detected

**Check folder paths:**

#### On macOS/Linux:
```bash
# Get full path to a folder
cd ~/Desktop/scans
pwd
# Copy this full path to .env
```

#### On Windows:
```cmd
# In File Explorer:
1. Navigate to your folder
2. Click the address bar
3. Copy the full path (e.g., C:\Users\julie\scans)
4. Paste into .env
```

**Check file formats:**
- Only `.jpg`, `.jpeg`, and `.png` are detected
- Files must be newly created/copied (not already there when script starts)

### Printer Not Working

**Test printer manually:**

#### On macOS/Linux:
```bash
echo "Test print" > test.txt
lpr -P YourPrinterName test.txt
```

#### On Windows:
1. Right-click the test file
2. Select "Print"
3. Choose your thermal printer

If manual printing doesn't work, fix your printer setup in your OS first.

---

## Understanding the Process

### What Happens to Each Image?

1. **Arweave Upload** (Permanent Storage)
   - Your image is uploaded to Arweave, a permanent decentralized storage network
   - It gets a unique URL like `https://arweave.net/abc123...`
   - This image will exist forever – it cannot be deleted or modified
   - Cost: ~$0.01-0.10 per image

2. **Metadata Creation**
   - A JSON file is created with:
     - NFT name: "Blockchain Bimbo Relic #001"
     - Description
     - Link to the Arweave image
     - Attributes (relic number, date, artist)
   - This metadata is also uploaded to Arweave permanently

3. **NFT Minting** (ZORA Blockchain)
   - A transaction is sent to your smart contract
   - The `safeMint` function creates a new token
   - The token points to your metadata on Arweave
   - Cost: ~$0.001-0.01 in gas fees

4. **QR Code & Receipt**
   - A QR code is generated linking to: `https://zora.co/collect/zora:0xYourContract/1`
   - Anyone can scan this to view the NFT
   - The receipt is printed for the participant to keep

### Total Cost Per Relic

- Arweave storage: $0.01-0.10
- ZORA gas: $0.001-0.01
- **Total: $0.02-0.15 per participant**

For a performance with 50 participants: ~$1-7.50 total

---

## For Technical Users

If you're comfortable with code and want to customize the system, see:

- **`QUICKSTART.md`** - Technical reference and advanced configuration
- **`blockchain_bimbo.py`** - Main application code
- **`requirements.txt`** - Python dependencies

### Customization Options

**Change the receipt text:**
Edit the `create_receipt()` function

**Modify NFT metadata:**
Edit the `metadata` dictionary in `upload_to_arweave()`

**Use a different mint function:**
If your contract uses a different signature (e.g., `mint(to, uri)` with auto-incrementing IDs), modify the `ERC721_ABI` and `mint_on_zora()` function

---

## Project Structure

```
BLOCKCHAIN-BIMBO-MAKEOVER/
├── blockchain_bimbo.py                 ← Main application
├── requirements.txt                    ← Dependencies list
├── setup.sh                            ← Auto-installer (Mac/Linux)
├── .env.example                        ← Configuration template
├── .env                                ← Your settings (create this!)
├── README.md                           ← This file (for everyone)
├── QUICKSTART.md                       ← Technical reference
├── index.html                          ← Web gallery view
└── static/
    ├── profile.jpg
    └── relics/                         ← Example relic images
```

---

## Safety & Security

### Protecting Your Private Key

⚠️ **CRITICAL SECURITY WARNINGS**:

1. **Never share your private key** with anyone
2. **Never commit `.env` to git** (it's in `.gitignore` for safety)
3. **Use a dedicated wallet** for this project, not your main wallet
4. **Keep backups** of your private key in a safe place
5. **For production**, consider using a hardware wallet

### What Can Go Wrong?

**If someone gets your private key:**
- They can steal all funds from that wallet
- They can mint NFTs using your contract
- They can impersonate you on the blockchain

**Stay safe:**
- Only put as much money in the wallet as you need for the performance
- After the performance, move any remaining funds to a secure wallet

---

## Credits

**Artist & Concept**: Julie van Essen  
**Project**: Blockchain Bimbo Makeover  
**Medium**: Performance Art, Blockchain Art  
**Technical Implementation**: This open-source system  

**Technologies Used**:
- Arweave (permanent storage)
- ZORA (NFT blockchain)
- Ethereum (payment layer)
- Python (automation)

---

## Philosophy

*From the receipt:*

> "This relic is minted without value.  
> It is a record of your presence,  
> a smudge of light archived in code.
>
> And yet—  
> the blockchain refuses valuelessness.  
> It waits to assign a price,  
> to drag this relic into markets."

This project exists in the tension between art and commerce, permanence and ephemerality, presence and absence. By participating, you become part of this ongoing conversation about what we value, what we preserve, and who we become in digital spaces.

---

## License

[Specify your license here]

## Questions?

- Technical issues? Check `QUICKSTART.md` for detailed troubleshooting
- Artistic inquiries? Contact Julie van Essen
- Want to contribute? Submit a pull request!

---

**Ready to create digital relics.** 🎨✨
