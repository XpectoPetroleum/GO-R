# GO:R - Handheld Roland GO:PIANO and GO:KEYS MIDI Patch Selector

A lightweight, full-screen MIDI patch selector and sender for **Roland GO: series** keyboards (GO:PIANO, GO:KEYS, etc.). Built with **Pygame** for a clean, responsive UI that's especially suited for small touchscreens or gamepad controls on retro handhelds.

This tool runs best on **retro handhelds** running **KNULLI OS** — turning your device into a portable, dedicated MIDI patch browser/controller for live performance or studio use.

<img width="40%" height="40%" alt="IMG_9612" src="https://github.com/user-attachments/assets/c6a8fe73-f47e-460b-86fe-3e40d6134442" />

## Features

- Full graphical user interface with dedicated screen and hardware buttons
- Provides access to many hidden Roland patches
- Browse Roland patches by category (Piano, EP, Organ, Synth, etc.) 
- Send patches to specific zones (1–16) via SysEx / CC **(In development, see below!)**
- Layering and splits **(In development, see below!)**
- Quick shortcuts: Zone 1 (X button), Zone 2 (Y button)
- Gamepad-first navigation (optimized for handhelds)
- Debug overlay for troubleshooting raw inputs

## Future Improvements and Features

- Bluetooth MIDI support
- Zones/Splits/Layers (partly developed but I dont have a GO:Keys to test it with. My GO:Piano only supports zone 1. If I can get my hands on a GO:Keys I can develop this further).
- Ability to run this code on other platforms and devices

## ❤️ Donations / Support

Thank you for considering a donation to support this project!  
All funds go directly toward development, maintenance, and keeping the lights on ☕.  
**If your preferred blockchain / token is not listed here, just ask and I'll add it!**

| <img src="https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=035" width="32" alt="Bitcoin"> **Bitcoin (BTC)**<br>`bc1qyourbitcoinaddresshere`<br><img src="https://api.qrserver.com/v1/create-qr-code/?data=bitcoin:bc1qyourbitcoinaddresshere?label=YourProjectName&message=GitHub%20donation&size=140x140" width="140" alt="Bitcoin QR"> | <img src="https://cryptologos.cc/logos/ethereum-eth-logo.png?v=035" width="32" alt="Ethereum"> **Ethereum (ETH) + ERC-20 (USDT, USDC, etc.)**<br>`0xYourEthereumAddressHere`<br><img src="https://api.qrserver.com/v1/create-qr-code/?data=ethereum:0xYourEthereumAddressHere?label=YourProjectName&message=GitHub%20donation%20(ETH/USDT/USDC)&size=140x140" width="140" alt="Ethereum QR"> | <img src="https://cryptologos.cc/logos/solana-sol-logo.png?v=035" width="32" alt="Solana"> **Solana (SOL)**<br>`YourSolanaAddressHere`<br><img src="https://api.qrserver.com/v1/create-qr-code/?data=solana:YourSolanaAddressHere?label=YourProjectName&message=GitHub%20donation&size=140x140" width="140" alt="Solana QR"> |
| :-: | :-: | :-: |
| <img src="https://cryptologos.cc/logos/xrp-xrp-logo.png?v=035" width="32" alt="XRP"> **XRP (Ripple)**<br>`yourxrpaddresshere`<br><img src="https://api.qrserver.com/v1/create-qr-code/?data=yourxrpaddresshere?label=YourProjectName&message=GitHub%20XRP%20donation&size=140x140" width="140" alt="XRP QR"><br>*(No destination tag needed — direct to cold wallet)* | <img src="https://cryptologos.cc/logos/dogecoin-doge-logo.png?v=035" width="32" alt="Dogecoin"> **Dogecoin (DOGE)**<br>`DYourDogecoinAddressHere`<br><img src="https://api.qrserver.com/v1/create-qr-code/?data=dogecoin:DYourDogecoinAddressHere?label=YourProjectName&message=GitHub%20donation&size=140x140" width="140" alt="Dogecoin QR"> | <img src="https://cryptologos.cc/logos/cardano-ada-logo.png?v=035" width="32" alt="Cardano"> **Cardano (ADA)**<br>`YourCardanoAddressHere`<br><img src="https://api.qrserver.com/v1/create-qr-code/?data=YourCardanoAddressHere?label=YourProjectName&message=GitHub%20donation&size=140x140" width="140" alt="Cardano QR"> |
| <img src="https://cryptologos.cc/logos/bitcoin-cash-bch-logo.png?v=035" width="32" alt="Bitcoin Cash"> **Bitcoin Cash (BCH)**<br>`bitcoincash:qzYourBCHAddressHere`<br><img src="https://api.qrserver.com/v1/create-qr-code/?data=bitcoincash:qzYourBCHAddressHere?label=YourProjectName&message=GitHub%20donation&size=140x140" width="140" alt="Bitcoin Cash QR"> | <img src="https://cryptologos.cc/logos/litecoin-ltc-logo.png?v=035" width="32" alt="Litecoin"> **Litecoin (LTC)**<br>`LYourLitecoinAddressHere`<br><img src="https://api.qrserver.com/v1/create-qr-code/?data=litecoin:LYourLitecoinAddressHere?label=YourProjectName&message=GitHub%20donation&size=140x140" width="140" alt="Litecoin QR"> | <img src="https://cryptologos.cc/logos/zcash-zec-logo.png?v=035" width="32" alt="Zcash"> **Zcash (ZEC)** – prefer shielded<br>`zsYourZcashShieldedAddressHere`<br><img src="https://api.qrserver.com/v1/create-qr-code/?data=zcash:zsYourZcashShieldedAddressHere?label=YourProjectName&message=GitHub%20donation&size=140x140" width="140" alt="Zcash QR"> |
| <img src="https://cryptologos.cc/logos/sui-sui-logo.png?v=035" width="32" alt="Sui"> **Sui (SUI)**<br>`YourSuiAddressHere`<br><img src="https://api.qrserver.com/v1/create-qr-code/?data=YourSuiAddressHere?label=YourProjectName&message=GitHub%20donation&size=140x140" width="140" alt="Sui QR"> |   |   |


## Screenshots

<img width="40%" height="40%" alt="IMG_9606" src="https://github.com/user-attachments/assets/d9b7c828-6fab-46e3-9418-e1284ad7d6cf" />
<img width="40%" height="40%" alt="IMG_9611" src="https://github.com/user-attachments/assets/cba9245d-7077-450a-ba37-a65bb57050ac" />
<img width="40%" height="40%" alt="IMG_9607" src="https://github.com/user-attachments/assets/610c6d54-c23d-407c-be0a-91f8f3d5c8cf" />
<img width="40%" height="40%" alt="IMG_9608" src="https://github.com/user-attachments/assets/69115c87-1092-4d1d-aa71-5eb8208c6de2" />
<img width="40%" height="40%" alt="IMG_9610" src="https://github.com/user-attachments/assets/be207d62-0983-43b1-bcb8-98568373f896" />

## Important: Platform & Requirements

- **Operating System**: Requires **KNULLI OS** (custom firmware for retro handhelds, forked from Batocera).  
  Desktop Linux / Windows / macOS versions are technically possible but **not optimized** — the UI and controls are tuned for handheld gamepad navigation and small screens.

- **Supported Handhelds** (check latest KNULLI releases for exact support):  
  - see [KNULLI Wiki Supported Devices](https://knulli.org/devices))
  - I have tested this code with the Ambernix RG35XXSP and Roland GO:Piano only. Other Knulli supported handhelds should work if they have USB OTG. We need to get more variants.

- **Why KNULLI?**  
  USB MIDI support, Excellent touchscreen/gamepad support, Python + Pygame support, wireless file transfer (SMB), OTA updates, and strong community for these low-power ARM devices.

- **Hardware Needed** (beyond the handheld):  
  - MIDI-capable Roland GO: series keyboard/piano  
  - USB cable (Bluetooth MIDI in future updates)  
  - MicroSD card

## Installation on KNULLI Handheld

1. Flash the latest **KNULLI OS** image to a microSD card following the official guide:  
   → [KNULLI Wiki – Installation](https://knulli.org/play/install/)

2. Insert the card into your handheld and boot it up for the first time.

3. **Initial Setup (must be done once after first boot)**

   - **Connect to Wi-Fi** (required for Samba, package installs, etc.):  
     - Press **Start** to open the main menu  
     - Go to **Network settings**  
     - Enable Wi-Fi and connect to your network  
     - Note your device's IP address (shown in Network settings)
       
   - **Enable Samba (SMB) network sharing** (for easy file transfer from PC/Mac):  
     - Main Menu → **System Settings → Services**  
     - Find and **enable SAMBA** (disabled by default in recent builds)  
     - Once enabled, access the device as a network share:  
       - **Windows**: `\\<device-ip>` in File Explorer  
       - **macOS**: Finder → Go → Connect to Server… → `smb://<device-ip>`  
       - **Linux**: `smb://<device-ip>` in your file manager  
     - Default access: username `guest`, password blank (or set a real user/password in **System Settings → Security**)

   - **SSH access** (enabled by default – no toggle needed):  
     - Username: `root`  
     - Default password: `linux` (strongly recommended to change it in **System Settings → Security**)  
     - Full connection guide (PuTTY, terminal, Mac/Linux/Windows clients, etc.):  
       → [Official KNULLI SSH Guide](https://knulli.org/configure/ssh)  
     - Quick example (from your computer's terminal):  ssh root@<device-ip>

	- **Transfer project files over the network**:  
    -  Use Samba (recommended for drag-and-drop) to copy `GO - R.sh` and the GO - R folder (includes: `ui.py`, `GoRLib.py`, and `patches.json`) to: `/share/roms/ports` 
    - Alternative: Use SCP/SFTP via SSH (e.g. WinSCP, FileZilla) or a card reader.

4. **Install Python dependencies** (via SSH or built-in terminal)

	- Connect via SSH (see above) or use the on-device terminal (Applications → Terminal), then run the following commands:
      
	      python3 -m ensurepip --upgrade
	      
	      pip3 install --upgrade pip
	      
	      pip3 install mido python-rtmidi
	      
	  **Note**:
	  - If pip3 fails, use `python3 -m pip install` instead.

5. **Run the application**

	- From the main knulli screen, go to "Ports" and then select "GO - R".

	<img width="40%" height="40%" alt="IMG_9600" src="https://github.com/user-attachments/assets/28d07e42-538c-4e1c-9e78-30597449d671" />
	<img width="40%" height="40%" alt="IMG_9605" src="https://github.com/user-attachments/assets/4502a02b-d3ce-4b63-af28-f964d162e764" />

## Troubleshooting

- **No MIDI ports shown** → Check USB MIDI connection; verify `python-rtmidi` installed correctly

## Credits

- Inspired heavily by [GO:Plus](https://github.com/waldt/goplus)
- Built with [Pygame](https://www.pygame.org/) & [python-rtmidi](https://spotlightkid.github.io/python-rtmidi/)
- Patch list based on Roland GO: series GM/GS/XG banks
- Optimized for the **KNULLI OS** retro handheld community

## License

MIT License — feel free to fork, modify, and port to other handhelds!

## ⚠️ Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

Project by **Teknotronix** (@teknotronix)  
Contributions are very welcome!
