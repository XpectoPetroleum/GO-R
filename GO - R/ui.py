# ui.py — FINAL PERFECT VERSION: GREEN SUCCESS, RED ERRORS, CORRECT NUMBERS
import sys, os, time, json, pygame
from enum import Enum

# ==================== MIDI ====================
try:
    import GoRLib
    connect_midi = GoRLib.init_midi_connection
    send_patch = GoRLib.zone_patch
    get_ports = GoRLib.get_output_ports
    enable_zone = GoRLib.zone_enable
    MIDI_AVAILABLE = True
except:
    MIDI_AVAILABLE = False
    def connect_midi(p): return False
    def send_patch(*a): pass
    def get_ports(): return ["MOCK_PORT_1", "MOCK_PORT_2"]

# ==================== PATCHES ====================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(SCRIPT_DIR, 'patches.json')) as f:
    data = json.load(f).get("FULL_LIST", [])
PATCHES_BY_CATEGORY = {}
CATEGORY_LIST = []
for patch in data:
    cat = patch.get("category", "OTHER")
    if cat not in CATEGORY_LIST:
        CATEGORY_LIST.append(cat)   
    PATCHES_BY_CATEGORY.setdefault(cat, []).append(patch)

# ==================== PYGAME ====================
pygame.init()
GScreenWidth, GScreenHeight = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((GScreenWidth, GScreenHeight))
pygame.display.set_caption('GO:R MIDI Selector')

FONT_PATH = pygame.font.match_font('dejavusansmono')
FONT_LARGE = pygame.font.Font(FONT_PATH, 36)
FONT_MEDIUM = pygame.font.Font(FONT_PATH, 24)
FONT_SMALL = pygame.font.Font(FONT_PATH, 18)
FONT_DEBUG = pygame.font.Font(FONT_PATH, 14)

COLOR_BG = (10, 10, 20)
COLOR_ACCENT = (0, 150, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_SELECTED = (50, 50, 100)
COLOR_STATUS_OK = (0, 255, 0)
COLOR_STATUS_FAIL = (255, 50, 50)
COLOR_DEBUG = (255, 255, 0)

HEADER_HEIGHT = 85
CLOCK = pygame.time.Clock()

pygame.joystick.init()
joystick = pygame.joystick.Joystick(0) if pygame.joystick.get_count() > 0 else None
if joystick: joystick.init()

# ==================== GLOBALS ====================

midi_status = "Disconnected"
CURRENT_MIDI_PORT_NAME = "None Selected"
GLastPatchSent = "None"
message_text = ""
message_timer = 0
SHOW_DEBUG = True
DEBUG_MESSAGE = "Ready"


# ==================== UTILITY FUNCTIONS ====================

def set_debug(msg):
    global DEBUG_MESSAGE
    DEBUG_MESSAGE = msg

class InputAction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    START = 5
    SELECT = 6      
    BACK = 6     #B     
    ACTION_1 = 8 #A      
    ACTION_2 = 9   #X
    ACTION_3 = 10  #Y  
    EXIT = 11          

def decode_keystroke(e):
    """Convert pygame event → InputAction. Shows raw button numbers in debug overlay."""

    # Show raw input so you can verify mapping
    if e.type == pygame.JOYBUTTONDOWN:
        set_debug(f"RAW BUTTON: {e.button} pressed")
    if e.type == pygame.JOYHATMOTION:
        set_debug(f"RAW HAT: {e.value}")
    if e.type == pygame.JOYAXISMOTION:
        set_debug(f"RAW AXIS: {e.axis} = {e.value:.3f}")

    # Keyboard fallback
    if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_ESCAPE:
            pygame.quit(); sys.exit()
        if e.key == pygame.K_UP:        return InputAction.UP
        if e.key == pygame.K_DOWN:      return InputAction.DOWN
        if e.key == pygame.K_LEFT:      return InputAction.LEFT
        if e.key == pygame.K_RIGHT:     return InputAction.RIGHT
        if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER): 
            return InputAction.ACTION_1
        if e.key == pygame.K_BACKSPACE:
            return InputAction.BACK

    # Gamepad — using YOUR exact mapping
    if joystick:
        if e.type == pygame.JOYBUTTONDOWN:
            if e.button == 3:   return InputAction.ACTION_1    # A
            if e.button == 4:   return InputAction.BACK        # B
            if e.button == 6:   return InputAction.ACTION_2    # X 
            if e.button == 5:  return InputAction.ACTION_3    # Y 
            if e.button == 10:  pygame.quit(); sys.exit()      # Start

        if e.type == pygame.JOYHATMOTION:
            x, y = e.value
            if y ==  1: return InputAction.UP
            if y == -1: return InputAction.DOWN
            if x == -1: return InputAction.LEFT
            if x ==  1: return InputAction.RIGHT

        # D-pad via AXES
        if e.type == pygame.JOYAXISMOTION:
            if e.axis == 0:  # Horizontal (left/right)
                if e.value < -0.5: return InputAction.LEFT
                if e.value >  0.5: return InputAction.RIGHT
            if e.axis == 1:  # Vertical (up/down) — sometimes inverted!
                if e.value < -0.5: return InputAction.UP   # test this direction
                if e.value >  0.5: return InputAction.DOWN

    return None

# ==================== SCREEN DRAWING AND RENDER FUNCTIONS ====================

def draw_text(text, font, color, x, y, align='left'):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if align == 'center': rect.centerx = x; rect.centery = y
    elif align == 'right': rect.right = x; rect.top = y
    else: rect.topleft = (x, y)
    screen.blit(surf, rect)

def draw_header():
    pygame.draw.rect(screen, COLOR_SELECTED, (0, 0, GScreenWidth, HEADER_HEIGHT))
    draw_text("G O : R", FONT_LARGE, COLOR_WHITE, GScreenWidth//2, 20, 'center')
    status_color = COLOR_STATUS_OK if midi_status == "Connected" else COLOR_STATUS_FAIL
    name = CURRENT_MIDI_PORT_NAME.split(":", 1)[1].strip() if ":" in CURRENT_MIDI_PORT_NAME else CURRENT_MIDI_PORT_NAME
    draw_text(f"{midi_status} - {name}", FONT_SMALL, status_color, 20, 40)
    draw_text(f"Current Patch: {GLastPatchSent}", FONT_SMALL, COLOR_WHITE, 20, 60)

def draw_button_helper(text):
    draw_text(text, FONT_SMALL, COLOR_ACCENT, GScreenWidth//2, GScreenHeight-10, 'center')

def draw_debug_overlay():
    if not SHOW_DEBUG: return
    pygame.draw.rect(screen, COLOR_BG, (0, GScreenHeight-55, GScreenWidth, 20))
    draw_text(f"DEBUG: {DEBUG_MESSAGE}", FONT_DEBUG, COLOR_DEBUG, 5, GScreenHeight-35)

def draw_show_message():
    # PERFECT MESSAGE COLORS
    if message_text and time.time() < message_timer:
        overlay = pygame.Surface((GScreenWidth, 50), pygame.SRCALPHA)
        overlay.fill((50,50,50,180))
        screen.blit(overlay, (0, GScreenHeight//2-25))

        msg_upper = message_text.upper()
        if any(error in msg_upper for error in ["ERROR", "FAILED", "FIRST"]):
            color = COLOR_STATUS_FAIL    # RED
        elif any(success in msg_upper for success in ["SENT", "CONNECTED", "ON"]):
            color = COLOR_STATUS_OK      # GREEN        
        else:
            color = COLOR_STATUS_OK

        draw_text(message_text, FONT_SMALL, color, GScreenWidth//2, GScreenHeight//2, 'center')

def show_message(text, duration=2):
    global message_text, message_timer
    message_text = text
    message_timer = time.time() + duration

def render_screen():
    screen.fill(COLOR_BG)
    draw_header()
    current.draw()

    draw_show_message()

    draw_debug_overlay()

    pygame.display.flip()
    CLOCK.tick(30) #FPS

# ==================== MENU BASE ====================

class MenuScreen:
    def __init__(self): self.selected_menu_index = 0
    def handle(self, k): return self
    def draw(self): draw_header()
    def on_enter(self): pass

# ==================== SCREENS ====================

class MainMenu(MenuScreen):
    
    OPTIONS = ["Select MIDI Port", "Patches", "Zones", "Performances", "Settings", "Exit"]
    
    def handle(self, action):
        set_debug(f"MainMenu | sel:{self.selected_menu_index} | key:{action}")

        if action==InputAction.UP:   self.selected_menu_index = max(0, self.selected_menu_index-1)
        if action==InputAction.DOWN: self.selected_menu_index = min(len(self.OPTIONS)-1, self.selected_menu_index+1)
        if action==InputAction.ACTION_1:
            i = self.selected_menu_index
            if i==0: return MidiSelectionScreen()
            if i==1:
                if midi_status != "Connected":
                    show_message("ERROR: Connect MIDI port first!")
                    return self
                return CategorySelectionScreen()
            if i==2: return ZoneManagementScreen()
            if i==3: return PerformanceMangementScreen()
            if i==4: return SettingsScreen()
            if i==5: return "exit"
        if action==InputAction.BACK: return "exit"

        return self
    
    def draw(self):
        #draw_header()
        
        y = HEADER_HEIGHT + 25
        
        for i, opt in enumerate(self.OPTIONS):
            y_pos = y + i*50
            if i == self.selected_menu_index:
                pygame.draw.rect(screen, COLOR_ACCENT, (50, y_pos-10, GScreenWidth-100, 50), border_radius=5)
                draw_text(f"> {opt} <", FONT_MEDIUM, COLOR_BG, 70, y_pos)
            else:
                draw_text(opt, FONT_MEDIUM, COLOR_WHITE, 70, y_pos)
        
        draw_button_helper("A: Select | B/Esc: Back/Exit | START: Exit")

class MidiSelectionScreen(MenuScreen):

    def on_enter(self):
        self.ports = get_ports()
        self.selected_menu_index = 0
    
    def handle(self, action):
        set_debug(f"MidiMenu | sel:{self.selected_menu_index}/{len(self.ports)} | key:{action}")
        if action==InputAction.UP:   self.selected_menu_index = max(0, self.selected_menu_index-1)
        if action==InputAction.DOWN: self.selected_menu_index = min(len(self.ports)-1, self.selected_menu_index+1)
        if action==InputAction.BACK: return MainMenu()
        if action==InputAction.ACTION_1:
            global midi_status, CURRENT_MIDI_PORT_NAME
            if connect_midi(self.ports[self.selected_menu_index]):
                midi_status = "Connected"
                CURRENT_MIDI_PORT_NAME = self.ports[self.selected_menu_index]
                show_message("Connected!")
            else:
                show_message("Connection FAILED!")
            return MainMenu()
        return self
    
    def draw(self):
        #draw_header()
        draw_text("Select MIDI Output Device:", FONT_MEDIUM, COLOR_WHITE, GScreenWidth//2, 105, 'center')
        if not self.ports:
            draw_text("No MIDI Output Ports Found.", FONT_MEDIUM, COLOR_STATUS_FAIL, GScreenWidth//2, 200, 'center')
        else:
            start = max(0, self.selected_menu_index - 4)
            for i in range(start, min(start+8, len(self.ports))):
                y = 150 + (i-start)*40
                if i == self.selected_menu_index:
                    pygame.draw.rect(screen, COLOR_ACCENT, (50, y-5, GScreenWidth-100, 40), border_radius=5)
                    draw_text(self.ports[i], FONT_MEDIUM, COLOR_BG, 70, y+7)
                else:
                    draw_text(self.ports[i], FONT_MEDIUM, COLOR_WHITE, 70, y+7)
        draw_button_helper("A: Connect | B: Back")

class CategorySelectionScreen(MenuScreen):

    def handle(self, action):
        set_debug(f"CategoryMenu | sel:{self.selected_menu_index}/{len(CATEGORY_LIST)} | key:{action}")
        
        if action==InputAction.UP:   self.selected_menu_index = max(0, self.selected_menu_index-1)
        if action==InputAction.DOWN: self.selected_menu_index = min(len(CATEGORY_LIST)-1, self.selected_menu_index+1)
        if action==InputAction.BACK: return MainMenu()
        if action==InputAction.ACTION_1: return PatchSelectionScreen(CATEGORY_LIST[self.selected_menu_index])

        return self
    
    def draw(self):
        #draw_header()
        draw_text("Select Patch Category:", FONT_MEDIUM, COLOR_WHITE, GScreenWidth//2, 105, 'center')

        start = max(0, self.selected_menu_index - 5)
        for i in range(start, min(start+10, len(CATEGORY_LIST))):
            cat = CATEGORY_LIST[i]
            cnt = len(PATCHES_BY_CATEGORY.get(cat, []))
            y = 140 + (i-start)*26
            if i == self.selected_menu_index:
                pygame.draw.rect(screen, COLOR_ACCENT, (50, y+5, GScreenWidth-100, 31), border_radius=8)
                draw_text(f"{cat}  ({cnt} patches)", FONT_MEDIUM, COLOR_BG, 70, y+8)
            else:
                draw_text(f"{cat}  ({cnt} patches)", FONT_MEDIUM, COLOR_WHITE, 70, y+8)

        draw_button_helper("A: Enter Category | B: Back")

class PatchSelectionScreen(MenuScreen):
    def __init__(self, category):
        super().__init__()
        self.category = category
        self.patches = PATCHES_BY_CATEGORY[category]
        self.zone_input_mode = False
        self.zone_input = ""  

    def send_to_zone(self, patch, zone):
        global GLastPatchSent
        msb, lsb, pc = patch['id']

        try:
            #time.sleep(0.5)

            # Lower split: Bass
            
            #GoRLib.enable_all_zones_SysEx()  # Enables parts + zones
            #time.sleep(1)

            # Lower split: Bass (Part 1 / Zone 1)
            #GoRLib.part_patch_SysEx(1, bank_msb=87, bank_lsb=70, pc=118) 
            #GoRLib.zone_key_range_SysEx(1, low=0, high=60)

            # Upper split: Organ (Part 2 / Zone 2)  
           # GoRLib.part_patch_SysEx(2, bank_msb=87, bank_lsb=66, pc=57)  
            #GoRLib.zone_key_range_SysEx(2, low=61, high=127)



            #possible working layering
            #GoRLib.setup_split_SysEx(
            #    lower_patch=(87, 70, 118),   # Example bass patch (MSB, LSB, PC)
             #   upper_patch=(87, 66, 57),   # Example organ/strings
           #     split_point=59,  # B3 MIDI note is 59, adjust for your split point
            #    lower_octave=3
           # )

            #GoRLib.clean_setup_split_SysEx(split_point=60)



            send_patch(zone, msb, lsb, pc)
            GoRLib.zone_enable(zone, True)
            #if(zone == 1):
            #    GoRLib.zone_key_range(zone, 0, 63)
            #else:
            #   GoRLib.zone_key_range(zone, 64, 127)

            GLastPatchSent = patch['name']
            show_message(f"{patch['name']} → Zone {zone}")
        except Exception as e:
            show_message(f"ERROR: {e}")                   
        

    def handle(self, action):
        patch = self.patches[self.selected_menu_index]
        patch_id = f"{patch['id'][0]:02d},{patch['id'][1]:02d},{patch['id'][2]:03d}"
        #set_debug(f"Patch: {patch_id} | {patch['name']} | {action.name}")

        # — Zone input mode (user typing 1-16) —
        if self.zone_input_mode:
            if action == InputAction.BACK:
                self.zone_input_mode = False
                self.zone_input = ""
                show_message("Cancelled")
                return self
           
            # For simplicity: use UP/DOWN to choose 1-16, A=confirm
            if action == InputAction.UP:
                val = int(self.zone_input or "1") + 1
                self.zone_input = str(min(val, 16))
            elif action == InputAction.DOWN:
                val = int(self.zone_input or "1") - 1
                self.zone_input = str(max(val, 1))

            if action == InputAction.ACTION_1:  # A = Confirm
                zone = int(self.zone_input or "1")
                self.send_to_zone(patch, zone)
                self.zone_input_mode = False
                self.zone_input = ""
                return self

            return self

        # — Normal navigation —
        if action == InputAction.UP:
            self.selected_menu_index = max(0, self.selected_menu_index - 1)
        elif action == InputAction.DOWN:
            self.selected_menu_index = min(len(self.patches) - 1, self.selected_menu_index + 1)
        elif action == InputAction.LEFT:
            self.selected_menu_index = max(0, self.selected_menu_index - 12)
        elif action == InputAction.RIGHT:
            self.selected_menu_index = min(len(self.patches) - 1, self.selected_menu_index + 12)
        elif action == InputAction.BACK:
            return CategorySelectionScreen()

        if midi_status != "Connected":
            return self

        # — A button: Ask for zone 1-16 —
        if action == InputAction.ACTION_1:
            self.zone_input_mode = True
            self.zone_input = "1"  # default
            show_message("Zone Selection Mode use ↑↓ to change zone", 3)

        # — X button: Zone 1 shortcut —
        elif action == InputAction.ACTION_2:
            self.send_to_zone(patch, 1)

        # — Y button: Zone 2 shortcut —
        elif action == InputAction.ACTION_3:
            self.send_to_zone(patch, 2)

        return self

    def draw(self):
        draw_header()
        start = max(0, self.selected_menu_index - 6)
        for i in range(start, min(start+12, len(self.patches))):
            p = self.patches[i]
            actual_idx = start + i
            txt = f"{actual_idx + 1:03d}. [{p['id'][0]:02d},{p['id'][1]:02d},{p['id'][2]:03d}] {p['name']}"
            y = 110 + (i-start)*26
            if i == self.selected_menu_index:
                pygame.draw.rect(screen, COLOR_SELECTED, (20, y, GScreenWidth-40, 26), border_radius=3)
                draw_text(txt, FONT_MEDIUM, COLOR_ACCENT, 40, y+2)
            else:
                draw_text(txt, FONT_MEDIUM, COLOR_WHITE, 40, y+2)

        # Dynamic helper text
        if self.zone_input_mode:
            zone = self.zone_input or "1"
            draw_button_helper(f"Select Zone (1-16): {zone:>2}   ↑↓=Change   A=Send   B=Cancel")
        else:
            draw_button_helper("A: Select Zone | X: To Zone 1 | Y: To Zone 2 | B: Back")

class ZoneManagementScreen(MenuScreen):

    def handle(self, action):
        set_debug(f"ZoneMenu | sel:{self.selected_menu_index} | key:{action}")

        if action==InputAction.BACK: return MainMenu()
        return self
    
    def draw(self):    
        draw_text("Zones feature coming soon!", FONT_MEDIUM, COLOR_WHITE, GScreenWidth//2, GScreenHeight//2, 'center')
        draw_button_helper("B: Back")

class PerformanceMangementScreen(MenuScreen):

    def handle(self, action):
        set_debug(f"PerformanceMenu | sel:{self.selected_menu_index} | key:{action}")
        if action==InputAction.BACK: return MainMenu()
        return self
    
    def draw(self):    
        draw_text("Performances feature coming soon!", FONT_MEDIUM, COLOR_WHITE, GScreenWidth//2, GScreenHeight//2, 'center')
        draw_button_helper("B: Back")

class SettingsScreen(MenuScreen):

    OPTIONS = ["Debug Overlay: OFF", "Back"]

    def on_enter(self):
        self.OPTIONS[0] = f"Debug Overlay: {'ON' if SHOW_DEBUG else 'OFF'}"
    
    def handle(self, action):
        set_debug(f"SettingsMenu | sel:{self.selected_menu_index} | key:{action}")
        if action in (InputAction.UP, InputAction.DOWN): self.selected_menu_index = 1 - self.selected_menu_index
        if action==InputAction.BACK: return MainMenu()
        if action==InputAction.ACTION_1:
            if self.selected_menu_index == 0:
                global SHOW_DEBUG
                SHOW_DEBUG = not SHOW_DEBUG
                self.OPTIONS[0] = f"Debug Overlay: {'ON' if SHOW_DEBUG else 'OFF'}"
                show_message(f"Debug Overlay is now {'ON' if SHOW_DEBUG else 'OFF'}")
            else:
                return MainMenu()
        return self
    
    def draw(self):
        #draw_header()
        draw_text("Settings", FONT_MEDIUM, COLOR_WHITE, GScreenWidth//2, 105, 'center')
        y = 160
        for i, opt in enumerate(self.OPTIONS):
            y_pos = y + i*70
            if i == self.selected_menu_index:
                pygame.draw.rect(screen, COLOR_ACCENT, (50, y_pos-10, GScreenWidth-100, 50), border_radius=5)
                draw_text(f"> {opt} <", FONT_MEDIUM, COLOR_BG, 70, y_pos)
            else:
                draw_text(opt, FONT_MEDIUM, COLOR_WHITE, 70, y_pos)
        draw_button_helper("A: Select | B: Back")

# ==================== MAIN LOOP ====================

current = MainMenu()
current.on_enter()

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        key = decode_keystroke(e)

        if key:
            next_screen = current.handle(key)

            if next_screen == "exit":
                pygame.quit(); sys.exit()
            if next_screen is not current:
                current = next_screen
                current.on_enter()

    render_screen()