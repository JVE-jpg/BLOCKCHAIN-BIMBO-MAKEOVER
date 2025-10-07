
import os
import sys
import time
import json
import tempfile
import platform
from datetime import datetime
import pygame
import qrcode
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Web3 and Arweave imports
from web3 import Web3
from eth_account import Account
import arseeding
import everpay

# Platform-specific imports
if platform.system() == 'Windows':
    import win32api

# Load environment variables
load_dotenv()

# === Config ===
WATCH_FOLDERS = os.getenv('WATCH_FOLDERS', '').split(',') if os.getenv('WATCH_FOLDERS') else []
RECEIPT_PRINTER_NAME = os.getenv('RECEIPT_PRINTER_NAME', 'POS-80')

# Ethereum/Arweave Config
ETH_PRIVATE_KEY = os.getenv('ETH_PRIVATE_KEY', '')
EVERPAY_CURRENCY = os.getenv('EVERPAY_CURRENCY', 'usdc')

# ZORA Config
ZORA_CONTRACT_ADDRESS = os.getenv('ZORA_CONTRACT_ADDRESS', '')
ZORA_RPC_URL = os.getenv('ZORA_RPC_URL', 'https://rpc.zora.energy')
ZORA_CHAIN_ID = int(os.getenv('ZORA_CHAIN_ID', '7777777'))

# NFT Metadata Config
NFT_NAME_PREFIX = os.getenv('NFT_NAME_PREFIX', 'Blockchain Bimbo Relic')
NFT_DESCRIPTION = os.getenv('NFT_DESCRIPTION', 'A digital relic from the Blockchain Bimbo Makeover performance')
NFT_ARTIST_NAME = os.getenv('NFT_ARTIST_NAME', 'Blockchain Bimbo Makeover')
ZORA_BASE_URL = os.getenv('ZORA_BASE_URL', 'https://zora.co/collect/zora')

# ERC-721 ABI for safeMint function
ERC721_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
            {"internalType": "string", "name": "uri", "type": "string"}
        ],
        "name": "safeMint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# === Display Setup ===
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

def display_image(path):
    screen.fill((0, 0, 0))
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, screen.get_size())
    screen.blit(img, (0, 0))
    pygame.display.flip()
    pygame.event.pump()

# === Arweave Upload ===
def upload_to_arweave(image_path, relic_id):
    """Upload image and metadata to Arweave using arseeding."""
    try:
        print(f"🌐 Starting Arweave upload for relic {relic_id}...")
        
        # Initialize EverPay signer
        signer = everpay.ETHSigner(ETH_PRIVATE_KEY)
        
        # 1) Upload image
        with open(image_path, "rb") as f:
            img_bytes = f.read()
        
        print(f"  📤 Uploading image ({len(img_bytes)} bytes)...")
        img_res = arseeding.send_and_pay(
            signer, 
            EVERPAY_CURRENCY, 
            img_bytes, 
            content_type="image/jpeg"
        )
        img_id = img_res["itemId"]
        img_url = f"https://arweave.net/{img_id}"
        print(f"  ✅ Image uploaded: {img_url}")
        
        # 2) Build and upload metadata.json
        metadata = {
            "name": f"{NFT_NAME_PREFIX} #{relic_id}",
            "description": NFT_DESCRIPTION,
            "image": img_url,
            "attributes": [
                {"trait_type": "Relic Number", "value": relic_id},
                {"trait_type": "Artist", "value": NFT_ARTIST_NAME},
                {"trait_type": "Created", "value": datetime.now().strftime("%Y-%m-%d %H:%M")}
            ]
        }
        
        meta_bytes = json.dumps(metadata, separators=(",", ":")).encode("utf-8")
        print("  📤 Uploading metadata...")
        meta_res = arseeding.send_and_pay(
            signer,
            EVERPAY_CURRENCY,
            meta_bytes,
            content_type="application/json"
        )
        meta_id = meta_res["itemId"]
        token_uri = f"https://arweave.net/{meta_id}"
        print(f"  ✅ Metadata uploaded: {token_uri}")
        
        return img_url, token_uri
    
    except Exception as e:
        print(f"❌ Arweave upload failed: {e}")
        return None, None

# === ZORA Minting ===
def mint_on_zora(token_uri, token_id):
    """Mint NFT on ZORA chain."""
    try:
        print(f"🎨 Starting ZORA mint for token #{token_id}...")
        
        # Initialize Web3
        w3 = Web3(Web3.HTTPProvider(ZORA_RPC_URL))
        if not w3.is_connected():
            raise Exception("Failed to connect to ZORA RPC")
        
        # Load account
        acct = Account.from_key(ETH_PRIVATE_KEY)
        contract = w3.eth.contract(
            address=Web3.to_checksum_address(ZORA_CONTRACT_ADDRESS),
            abi=ERC721_ABI
        )
        
        # Prepare transaction
        to_addr = acct.address
        fn = contract.functions.safeMint(to_addr, token_id, token_uri)
        
        # Estimate gas
        gas = int(fn.estimate_gas({"from": acct.address}) * 1.2)
        base = w3.eth.get_block("latest")["baseFeePerGas"]
        prio = w3.to_wei("0.05", "gwei")
        
        # Build transaction
        tx = fn.build_transaction({
            "from": acct.address,
            "nonce": w3.eth.get_transaction_count(acct.address),
            "chainId": ZORA_CHAIN_ID,
            "gas": gas,
            "maxFeePerGas": int(base * 2 + prio),
            "maxPriorityFeePerGas": prio
        })
        
        # Sign and send
        signed = acct.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        print(f"  ⏳ Transaction sent: {tx_hash.hex()}")
        
        # Wait for receipt
        rcpt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if rcpt.status == 1:
            nft_url = f"{ZORA_BASE_URL}:{ZORA_CONTRACT_ADDRESS}/{token_id}"
            print(f"  ✅ Mint successful! NFT URL: {nft_url}")
            return nft_url, tx_hash.hex()
        else:
            print("  ❌ Transaction failed")
            return None, None
    
    except Exception as e:
        print(f"❌ ZORA mint failed: {e}")
        return None, None

# === QR Code Generation ===
def generate_qr_code(url):
    """Generate QR code image for the NFT URL."""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to temp file
        qr_path = tempfile.mktemp(".png")
        img.save(qr_path)
        return qr_path
    
    except Exception as e:
        print(f"❌ QR code generation failed: {e}")
        return None

# === Cross-Platform Printing ===
def print_file(file_path):
    """Print a file using platform-specific methods."""
    system = platform.system()
    
    try:
        if system == 'Windows':
            win32api.ShellExecute(0, "printto", file_path, f'"{RECEIPT_PRINTER_NAME}"', ".", 0)
        elif system == 'Darwin':  # macOS
            os.system(f'lpr -P "{RECEIPT_PRINTER_NAME}" "{file_path}"')
        elif system == 'Linux':
            os.system(f'lpr -P "{RECEIPT_PRINTER_NAME}" "{file_path}"')
        else:
            print(f"⚠️  Unknown operating system: {system}")
            return False
        
        return True
    
    except Exception as e:
        print(f"❌ Printing failed: {e}")
        return False

# === Receipt Generator ===
def create_receipt(relic_id, timestamp, nft_url=None, qr_code_path=None):
    """Create and print receipt with optional QR code."""
    receipt_text = f"""
༘˚⋆𐙚｡⋆𖦹.✧˚YOU HAVE JUST CREATED YOUR DIGITAL RELIC ༘˚⋆𐙚｡⋆𖦹.✧˚

This relic is minted without value.  
It is a record of your presence,  
a smudge of light archived in code.

And yet—  
the blockchain refuses valuelessness.  
It waits to assign a price,  
to drag this relic into markets.

Scan the QR code below  
to see your relic in the archive.  
Claim it, keep it, ignore it,  
but know: it will always resist  
our wish for no-price.

DIGITAL RELIC NUMBER: {relic_id}  
DATE: {timestamp}  
"""
    
    if nft_url:
        receipt_text += f"\nNFT URL: {nft_url}\n"
    
    receipt_text += """
⠀:¨ ·.· ¨:⠀
⠀ `· . ୨୧⠀ 
"""

    receipt_path = tempfile.mktemp(".txt")
    with open(receipt_path, "w", encoding="utf-8") as f:
        f.write(receipt_text)

    # Print text receipt
    if print_file(receipt_path):
        print(f"🧾 Printed receipt for {relic_id}")
    
    # Print QR code if available
    if qr_code_path and os.path.exists(qr_code_path):
        if print_file(qr_code_path):
            print(f"📱 Printed QR code for {relic_id}")
        
        # Clean up QR code
        try:
            os.remove(qr_code_path)
        except OSError:
            pass
    
    # Clean up receipt
    try:
        os.remove(receipt_path)
    except OSError:
        pass

# === File Watcher ===
class ScanHandler(FileSystemEventHandler):
    counter = 1

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            folder = os.path.dirname(event.src_path)
            filename = os.path.basename(event.src_path)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            relic_id = str(self.counter).zfill(3)

            print(f"\n{'='*60}")
            print(f"📸 New scan detected: {filename}")
            print(f"📂 Source folder: {folder}")
            print(f"🆔 Relic ID: {relic_id}")
            print(f"{'='*60}")
            
            # Display image on screen
            display_image(event.src_path)
            
            # Check if we have the required credentials
            if not ETH_PRIVATE_KEY or not ZORA_CONTRACT_ADDRESS:
                print("⚠️  Missing ETH_PRIVATE_KEY or ZORA_CONTRACT_ADDRESS")
                print("⚠️  Skipping blockchain operations. Check your .env file.")
                create_receipt(relic_id, timestamp)
                self.counter += 1
                return
            
            try:
                # 1) Upload to Arweave
                img_url, token_uri = upload_to_arweave(event.src_path, relic_id)
                
                if not token_uri:
                    print("⚠️  Arweave upload failed, skipping mint")
                    create_receipt(relic_id, timestamp)
                    self.counter += 1
                    return
                
                # 2) Mint on ZORA
                nft_url, tx_hash = mint_on_zora(token_uri, self.counter)
                
                if not nft_url:
                    print("⚠️  ZORA mint failed")
                    create_receipt(relic_id, timestamp)
                    self.counter += 1
                    return
                
                # 3) Generate QR code
                qr_code_path = generate_qr_code(nft_url)
                
                # 4) Print receipt with QR code
                create_receipt(relic_id, timestamp, nft_url, qr_code_path)
                
                print(f"\n✨ Successfully created Digital Relic #{relic_id}")
                print(f"🔗 NFT URL: {nft_url}")
                print(f"📜 Transaction: {tx_hash}")
                print(f"{'='*60}\n")
                
            except Exception as e:
                print(f"❌ Error processing scan: {e}")
                import traceback
                traceback.print_exc()
                create_receipt(relic_id, timestamp)
            
            self.counter += 1

def start_watching():
    """Start watching configured folders for new scan images."""
    if not WATCH_FOLDERS or WATCH_FOLDERS == ['']:
        print("❌ No watch folders configured!")
        print("   Please set WATCH_FOLDERS in your .env file")
        sys.exit(1)
    
    event_handler = ScanHandler()
    observer = Observer()
    
    for folder in WATCH_FOLDERS:
        folder = folder.strip()
        if not folder:
            continue
        
        os.makedirs(folder, exist_ok=True)
        observer.schedule(event_handler, path=folder, recursive=False)
        print(f"🔍 Watching for new scans in: {folder}")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        observer.stop()
    observer.join()

def validate_config():
    """Validate configuration and fail fast if critical settings are missing."""
    print("\n" + "="*60)
    print("🎨 BLOCKCHAIN BIMBO MAKEOVER - DIGITAL RELIC GENERATOR")
    print("="*60)
    
    print(f"\n🖥️  Operating System: {platform.system()}")
    
    errors = []
    
    # Critical validations - these MUST be set
    if not ETH_PRIVATE_KEY or ETH_PRIVATE_KEY == '':
        errors.append("ETH_PRIVATE_KEY is not set")
    else:
        # Validate private key format
        try:
            if not ETH_PRIVATE_KEY.startswith('0x'):
                errors.append("ETH_PRIVATE_KEY must start with '0x'")
            elif len(ETH_PRIVATE_KEY) != 66:
                errors.append(f"ETH_PRIVATE_KEY has invalid length ({len(ETH_PRIVATE_KEY)} chars, expected 66)")
            else:
                acct = Account.from_key(ETH_PRIVATE_KEY)
                print(f"✅ ETH wallet: {acct.address}")
        except Exception as e:
            errors.append(f"ETH_PRIVATE_KEY is invalid: {str(e)}")
    
    if not ZORA_CONTRACT_ADDRESS or ZORA_CONTRACT_ADDRESS == '':
        errors.append("ZORA_CONTRACT_ADDRESS is not set")
    else:
        # Validate contract address format
        if not ZORA_CONTRACT_ADDRESS.startswith('0x'):
            errors.append("ZORA_CONTRACT_ADDRESS must start with '0x'")
        elif len(ZORA_CONTRACT_ADDRESS) != 42:
            errors.append(f"ZORA_CONTRACT_ADDRESS has invalid length ({len(ZORA_CONTRACT_ADDRESS)} chars, expected 42)")
        else:
            print(f"✅ ZORA contract: {ZORA_CONTRACT_ADDRESS}")
    
    if not WATCH_FOLDERS or WATCH_FOLDERS == [''] or all(not f.strip() for f in WATCH_FOLDERS):
        errors.append("WATCH_FOLDERS is not set or empty")
    else:
        valid_folders = [f.strip() for f in WATCH_FOLDERS if f.strip()]
        print(f"✅ Watch folders: {len(valid_folders)} configured")
        for folder in valid_folders:
            if not os.path.isabs(folder):
                errors.append(f"WATCH_FOLDERS must use absolute paths: '{folder}' is relative")
    
    # Display non-critical config
    print(f"🖨️  Printer: {RECEIPT_PRINTER_NAME}")
    print(f"⛓️  ZORA Chain ID: {ZORA_CHAIN_ID}")
    print(f"🌐 ZORA RPC: {ZORA_RPC_URL}")
    print(f"💰 Arweave payment: {EVERPAY_CURRENCY.upper()}")
    
    # If there are errors, print them and exit
    if errors:
        print("\n" + "="*60)
        print("❌ CONFIGURATION ERRORS DETECTED")
        print("="*60)
        print("\nThe following configuration errors must be fixed:\n")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        
        print("\n" + "="*60)
        print("📝 HOW TO FIX:")
        print("="*60)
        print("\n1. Make sure you have a .env file in the project directory")
        print("2. Copy from .env.example if needed:")
        print("   cp .env.example .env")
        print("\n3. Edit the .env file and set these required variables:")
        print("   - ETH_PRIVATE_KEY=0x... (66 characters, starts with 0x)")
        print("   - ZORA_CONTRACT_ADDRESS=0x... (42 characters, starts with 0x)")
        print("   - WATCH_FOLDERS=/absolute/path/to/folder")
        print("\n4. Run the script again")
        print("\n" + "="*60 + "\n")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ Configuration validated successfully!")
    print("="*60 + "\n")

# === Main Execution ===
if __name__ == "__main__":
    validate_config()
    
    # Initialize pygame display
    screen.fill((0, 0, 0))  # Start with black screen
    pygame.display.flip()
    
    print("🚀 Starting file watcher...")
    print("   Drop scanned images into watched folders to create relics!")
    print("   Press Ctrl+C to stop\n")
    
    start_watching()
