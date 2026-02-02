# GO:R - Roland GO:PIANO and GO:KEYS MIDI Selector

A lightweight, full-screen MIDI patch selector and sender for **Roland GO: series** keyboards (GO:PIANO, GO:KEYS, etc.). Built with **Pygame** for a clean, responsive UI that's especially suited for small touchscreens or gamepad controls on retro handhelds.

This tool runs best on **retro handhelds** running **KNULLI OS** — turning your device into a portable, dedicated MIDI patch browser/controller for live performance or studio use.

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

## Important: Platform & Requirements

- **Operating System**: Requires **KNULLI OS** (custom firmware for retro handhelds, forked from Batocera).  
  Desktop Linux / Windows / macOS versions are technically possible but **not optimized** — the UI and controls are tuned for handheld gamepad navigation and small screens.

- **Supported Handhelds** (check latest KNULLI releases for exact support):  
  - see [KNULLI Wiki Supported Devices](https://knulli.org/devices))
  - I have tested this code with the Ambernix RG35XXSP and Roland GO:Piano only. Other Knulli supported handhelds should work if they have USB OTG. We need to get more variants.

- **Why KNULLI?**  
  Excellent touchscreen/gamepad support, EmulationStation frontend, Python + Pygame usually available or easily added, wireless file transfer (SMB), OTA updates, and strong community for these low-power ARM devices.

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
	  - If `pip3` fails, use `python3 -m pip install ...` instead.

5. **Run the application**

	- From the main knulli screen, go to "Ports" and then select "GO - R".

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
Contributions, handheld screenshots, and KNULLI-specific improvements very welcome!
