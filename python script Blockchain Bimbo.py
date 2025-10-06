
import os
import time
import tempfile
from datetime import datetime
from PIL import Image
import pygame
import win32api
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === Config ===
WATCH_FOLDERS = [
    r"C:\Users\julie\OneDrive\Pictures",
    r"C:\Users\julie\Downloads\blockchain_bimbo_laptop_version\blockchain_bimbo_laptop_version\scans"
]
RECEIPT_PRINTER_NAME = "POS-80"  # Adjust to your actual printer name

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

# === Receipt Generator ===
def create_receipt(relic_id, timestamp, filename, folder):
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

⠀:¨ ·.· ¨:⠀
⠀ `· . ୨୧⠀ 
"""

    receipt_path = tempfile.mktemp(".txt")
    with open(receipt_path, "w", encoding="utf-8") as f:
        f.write(receipt_text)

    try:
        win32api.ShellExecute(0, "printto", receipt_path, f'"{RECEIPT_PRINTER_NAME}"', ".", 0)
        print(f"🧾 Printed receipt for {relic_id} to {RECEIPT_PRINTER_NAME}")
    except Exception as e:
        print("❌ Printing failed:", e)

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

            print(f"\n📸 New scan detected: {filename}")
            print(f"📂 Source folder: {folder}")
            display_image(event.src_path)
            create_receipt(relic_id, timestamp, filename, folder)

            self.counter += 1

def start_watching():
    event_handler = ScanHandler()
    observer = Observer()
    for folder in WATCH_FOLDERS:
        os.makedirs(folder, exist_ok=True)
        observer.schedule(event_handler, path=folder, recursive=False)
        print(f"🔍 Watching for new scans in: {folder}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# === Main Execution ===
if __name__ == "__main__":
    screen.fill((0, 0, 0))  # Start with black screen
    pygame.display.flip()
    start_watching()
