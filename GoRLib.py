# GoRLib.py
import argparse, copy, threading, time
import sys  # Added 'sys' for clean error logging
from operator import itemgetter
import rtmidi
from rtmidi.midiutil import open_midiinput, open_midioutput

# --- SysEx and Device Constants (Retained from original file) ---
SETUP = 0x01000000
SYS_COMMON = 0x02000000
SYS_CTRL = 0x02004000

TMP_PERF_BASE = 0x10000000
PART_OFFSET = 0x2000
ZONE_OFFSET = 0x5000
PART_ADDRESS_BASE = TMP_PERF_BASE + PART_OFFSET
ZONE_ADDRESS_BASE = TMP_PERF_BASE + ZONE_OFFSET
PATCH_ADDRESS_BASE = 0x11000000
SOUND_DEMO_SWITCH = 0x0F002000  # set to 0x00 for turning off, 0x01 1st layer etc.

RQ1 = 0x11
DT1 = 0x12
IDENTITY_REQUEST = [0xF0, 0x7E, 0x10, 0x06, 0x01, 0xF7]
IDENTITY_REPLY_START = [0xF0, 0x7E, 0x10, 0x06, 0x02, 0x41]

MODEL_IDS = {
    "GK": '0000003C',  # Model IDs
    "GP": '0000003D'
}
MODEL_ID_AUX = '00000028'

# --- CORRECTED MIDI PROTOCOL CONSTANTS ---
CONTROL_CHANGE_STATUS = 0xB0
PROGRAM_CHANGE_STATUS = 0xC0

CC_BANK_MSB = 0x00
CC_BANK_LSB = 0x20

# --- Global State ---
_midi_manager_instance = None

# --- Custom exception
class GoRLibMIDIError(RuntimeError):
    """Raised for MIDI-related errors in GoRLib"""
    pass

# --- MidiManager Class ---
class MidiManager:
    """Handles MIDI connection, sending, receiving, and SysEx communication."""

    def __init__(self, port_name=None):
        self.port_name = port_name
        self.midiout = rtmidi.MidiOut()
        self.midiin = None
        self.midiin_port_index = -1
        self.midiout_port_index = -1
        self.is_connected = False

    def get_ports(self):
        """Helper to get available output ports."""
        return self.midiout.get_ports()

    def open_port(self):
        """Opens the MIDI output and optionally input port."""
        if self.is_connected:
            self.close_port()

        port_names = self.midiout.get_ports()

        if self.port_name:
            try:
                self.midiout_port_index = port_names.index(self.port_name)
            except ValueError:
                raise GoRLibMIDIError(f"Output port '{self.port_name}' not found.")
        else:
            if not port_names:
                raise GoRLibMIDIError("No MIDI output ports found.")
            self.midiout_port_index = 0
            self.port_name = port_names[0]

        try:
            self.midiout.open_port(self.midiout_port_index)
            self.is_connected = True

            input_ports = rtmidi.MidiIn().get_ports()
            if self.port_name in input_ports:
                try:
                    self.midiin, port_name = open_midiinput(self.port_name, client_name="GoRLib MIDI RX", api=rtmidi.API_UNSPECIFIED)
                    self.midiin.set_callback(self.midi_callback)
                except Exception as e:
                    raise GoRLibMIDIError(f"Could not open MIDI Input port: {e}")

            return True

        except Exception as e:
            self.is_connected = False
            raise GoRLibMIDIError(f"Failed to open MIDI port {self.port_name}: {e}")

    def close_port(self):
        """Closes the MIDI ports."""
        if self.midiout.is_port_open():
            self.midiout.close_port()
        if self.midiin:
            self.midiin.close_port()
            self.midiin = None
        self.is_connected = False

    def send_message(self, message):
        """Sends a raw MIDI message."""
        if self.midiout.is_port_open():
            self.midiout.send_message(message)
        else:
            raise IOError("MIDI output port is not open.")

    def midi_callback(self, message, data=None):
        """Callback function for incoming MIDI messages."""
        pass

    def send_identity_request(self):
        """Sends the Universal System Exclusive Identity Request."""
        if self.is_connected:
            self.send_message(IDENTITY_REQUEST)
        else:
            raise GoRLibMIDIError("Cannot send SysEx, MIDI not connected.")


# --- Wrapper Functions ---
def get_output_ports():
    """Returns a list of available MIDI output port names."""
    try:
        midi_out = rtmidi.MidiOut()
        return midi_out.get_ports()
    except Exception as e:
        raise GoRLibMIDIError(f"Failed to list MIDI ports: {e}")

def enable_multi_zone_mode() -> None:
    """Legacy — not needed on GO:PIANO, kept for compatibility."""
    pass

def init_midi_connection(port_name):
    """
    Initializes and opens the MIDI connection using the MidiManager class.
    """
    global _midi_manager_instance

    if _midi_manager_instance:
        try:
            _midi_manager_instance.close_port()
        except Exception:
            pass
        _midi_manager_instance = None

    try:
        manager = MidiManager(port_name)
        if manager.open_port():
            _midi_manager_instance = manager
            return True
        else:
            _midi_manager_instance = None
            return False

    except Exception as e:
        _midi_manager_instance = None
        raise GoRLibMIDIError(f"MidiManager connection failed: {e}")


# ===================================================================
# ZONE API — Standard CC-based (for reference / other keyboards)
# ===================================================================

def zone_enable(zone: int, on: bool = True) -> None:
    if not _midi_manager_instance or not _midi_manager_instance.is_connected:
        raise GoRLibMIDIError("MIDI not connected")
    if not 1 <= zone <= 16:
        raise ValueError(f"Zone must be 1–16, got {zone}")

    channel = zone - 1
    value = 127 if on else 0
    _midi_manager_instance.send_message([0xB0 | channel, 85, value])

def zone_patch(zone: int, bank_msb: int, bank_lsb: int = 0, pc: int = 0) -> None:
    if not _midi_manager_instance or not _midi_manager_instance.is_connected:
        raise GoRLibMIDIError("MIDI not connected")
    if not 1 <= zone <= 16:
        raise ValueError(f"Zone must be 1–16, got {zone}")

    channel = zone - 1
    bank_msb &= 0x7F
    bank_lsb &= 0x7F
    pc &= 0x7F

    _midi_manager_instance.send_message([0xB0 | channel, 0, bank_msb])
    _midi_manager_instance.send_message([0xB0 | channel, 32, bank_lsb])
    _midi_manager_instance.send_message([0xC0 | channel, pc])

def zone_octave(zone: int, shift: int) -> None:
    if not _midi_manager_instance or not _midi_manager_instance.is_connected:
        raise GoRLibMIDIError("MIDI not connected")
    if not 1 <= zone <= 16:
        raise ValueError(f"Zone must be 1–16, got {zone}")
    if not -4 <= shift <= 4:
        raise ValueError(f"Octave shift must be -4 to +4, got {shift}")

    channel = zone - 1
    _midi_manager_instance.send_message([0xB0 | channel, 86, shift + 64])

def zone_key_range(zone: int, low: int | None = None, high: int | None = None) -> None:
    if not _midi_manager_instance or not _midi_manager_instance.is_connected:
        raise GoRLibMIDIError("MIDI not connected")
    if not 1 <= zone <= 16:
        raise ValueError(f"Zone must be 1–16, got {zone}")

    channel = zone - 1
    if low is not None:
        low = max(0, min(127, low))
        _midi_manager_instance.send_message([0xB0 | channel, 87, low])
    if high is not None:
        high = max(0, min(127, high))
        _midi_manager_instance.send_message([0xB0 | channel, 88, high])


# ===================================================================
# SYSEx ZONE/PART CONTROL FOR GO:PIANO (61/88) & GO:KEYS <<<--- CURRENTLY UNTESTED AND STILL IN DEVELOPMENT!!!
# ===================================================================

# --- Addresses and Offsets (Exact Match from Original goplus.py) ---
TMP_PERF_BASE = 0x10000000
PART_OFFSET = 0x2000
ZONE_OFFSET = 0x5000
PART_BASE = TMP_PERF_BASE + PART_OFFSET
ZONE_BASE = TMP_PERF_BASE + ZONE_OFFSET

# Part Offsets
OFF_PART_RX_CHAN = 0x0000
OFF_PART_RX_SW = 0x0001
OFF_PART_BANK_MSB = 0x0004
OFF_PART_BANK_LSB = 0x0005
OFF_PART_PC = 0x0006

# Zone Offsets
OFF_ZONE_SW = 0x0000
OFF_ZONE_OCTAVE = 0x0001
OFF_ZONE_LOW = 0x0004
OFF_ZONE_HIGH = 0x0005

# Block Sizes
PART_BLOCK_SIZE = 0x0200  # 512 bytes
ZONE_BLOCK_SIZE = 0x0080  # 128 bytes

# --- Fixed SysEx Sender ---
def _send_sysex_fixed(self, address: int, data: bytes):
    if not self.is_connected:
        raise GoRLibMIDIError("MIDI not connected")

    addr_bytes = address.to_bytes(4, 'big')
    payload = addr_bytes + data
    checksum = (128 - sum(payload) % 128) & 0x7F

    model_id = bytes.fromhex('0000003D')  # GO:PIANO
    sysex = [0xF0, 0x41, 0x10] + list(model_id) + [0x12] + list(payload) + [checksum, 0xF7]

    self.send_message(sysex)
    time.sleep(0.05)  # Safe delay

MidiManager._send_sysex_fixed = _send_sysex_fixed

# --- Part Functions ---
def part_receive_channel_SysEx(part: int, channel: int) -> None:
    if not 1 <= part <= 16 or not 1 <= channel <= 16:
        raise ValueError("Part/channel 1–16")
    addr = PART_BASE + (part - 1) * PART_BLOCK_SIZE + OFF_PART_RX_CHAN
    value = channel - 1  # 0 for ch1, 1 for ch2, etc.
    _midi_manager_instance._send_sysex_fixed(addr, bytes([value]))

def part_enable_SysEx(part: int, on: bool = True) -> None:
    if not 1 <= part <= 16:
        raise ValueError("Part must be 1–16")
    addr = PART_BASE + (part - 1) * PART_BLOCK_SIZE + OFF_PART_RX_SW
    value = 1 if on else 0
    _midi_manager_instance._send_sysex_fixed(addr, bytes([value]))

def part_patch_SysEx(part: int, bank_msb: int, bank_lsb: int = 0, pc: int = 0) -> None:
    if not 1 <= part <= 16:
        raise ValueError("Part must be 1–16")
    base = PART_BASE + (part - 1) * PART_BLOCK_SIZE
    bank_msb &= 0x7F
    bank_lsb &= 0x7F
    pc &= 0x7F

    _midi_manager_instance._send_sysex_fixed(base + OFF_PART_BANK_MSB, bytes([bank_msb]))
    _midi_manager_instance._send_sysex_fixed(base + OFF_PART_BANK_LSB, bytes([bank_lsb]))
    _midi_manager_instance._send_sysex_fixed(base + OFF_PART_PC, bytes([pc]))
    time.sleep(0.1)  # Allow tone to load

# --- Zone Functions ---
def zone_enable_SysEx(zone: int, on: bool = True) -> None:
    if not 1 <= zone <= 16:
        raise ValueError("Zone must be 1–16")
    addr = ZONE_BASE + (zone - 1) * ZONE_BLOCK_SIZE + OFF_ZONE_SW
    value = 1 if on else 0
    _midi_manager_instance._send_sysex_fixed(addr, bytes([value]))

def zone_octave_SysEx(zone: int, shift: int) -> None:
    if not -3 <= shift <= 3:
        raise ValueError("Octave shift -3 to +3")
    addr = ZONE_BASE + (zone - 1) * ZONE_BLOCK_SIZE + OFF_ZONE_OCTAVE
    value = shift + 64  # Correct: 61 for -3, 64 for 0, 67 for +3
    _midi_manager_instance._send_sysex_fixed(addr, bytes([value]))

def zone_key_range_SysEx(zone: int, low: int | None = None, high: int | None = None) -> None:
    if not 1 <= zone <= 16:
        raise ValueError("Zone must be 1–16")
    base = ZONE_BASE + (zone - 1) * ZONE_BLOCK_SIZE
    if low is not None:
        low = max(0, min(127, low))
        _midi_manager_instance._send_sysex_fixed(base + OFF_ZONE_LOW, bytes([low]))
    if high is not None:
        high = max(0, min(127, high))
        _midi_manager_instance._send_sysex_fixed(base + OFF_ZONE_HIGH, bytes([high]))

def reset_to_default_SysEx() -> None:
    """Reset to factory-like state (all zones full, default patches) - optional"""
    for i in range(1, 17):
        part_enable_SysEx(i, True)
        zone_enable_SysEx(i, True)
        zone_octave_SysEx(i, 0)
        zone_key_range_SysEx(i, low=0, high=127)
    time.sleep(1)

def setup_split_SysEx(lower_patch: tuple = (87, 66, 71), upper_patch: tuple = (87, 71, 40), split_point: int = 60, lower_octave: int = -1) -> None:
    """Clean split without disabling everything (avoids no-sound)"""
    # Ensure the used parts/zones are enabled
    # Lower
    part_receive_channel_SysEx(1,1)
    part_enable_SysEx(1, True)
    part_patch_SysEx(1, *lower_patch)
    zone_enable_SysEx(1, True)
    #zone_octave_SysEx(1, lower_octave)
    zone_key_range_SysEx(1, low=0, high=split_point)

    # Upper
    part_receive_channel_SysEx(2,1)
    part_enable_SysEx(2, True)
    part_patch_SysEx(2, *upper_patch)
    zone_enable_SysEx(2, True)
    zone_key_range_SysEx(2, low=split_point + 1, high=127)

    # Optional: disable a few extra if layering from defaults
    for i in range(3, 17):
        zone_enable_SysEx(i, False)  # Disable extra zones to reduce potential layering

    time.sleep(0.5)

# Optional: full enable if you want all zones active
def enable_all_zones_SysEx() -> None:
    for i in range(1, 17):
        part_enable_SysEx(i, True)
        zone_enable_SysEx(i, True)
        zone_octave_SysEx(i, 0)
        zone_key_range_SysEx(i, low=0, high=127)