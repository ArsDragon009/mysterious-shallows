# Imports
import pyperclip, string
import pygame, sys, shelve, colorsys, math, os
from random import *

# Main settings
WIDTH = 1100
HEIGHT = 600
FPS = 60
_dev = False

# Init Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
pygame.display.set_icon(pygame.image.load("images/icon.png"))
clock = pygame.time.Clock()
running = True

# Sprites
unknown_item = pygame.image.load("images/items/unknown_item.png").convert_alpha()
map_world = pygame.image.load("images/map.png").convert_alpha()
spritesets = {
    "player": {
        "normal": {
            "idle": pygame.image.load("images/glav.png").convert_alpha(),
            "left": pygame.image.load("images/glav_left.png").convert_alpha(),
            "right": pygame.image.load("images/glav_right.png").convert_alpha(),
        }
    },
    "slash": {
        "normal": {
            0: pygame.image.load("images/slash_1.png").convert_alpha(),
            1: pygame.image.load("images/slash_2.png").convert_alpha(),
            2: pygame.image.load("images/slash_3.png").convert_alpha(),
            3: pygame.image.load("images/slash_4.png").convert_alpha(),
            4: pygame.image.load("images/slash_5.png").convert_alpha(),
        },
        "red": {
            0: pygame.image.load("images/red_slash_1.png").convert_alpha(),
            1: pygame.image.load("images/red_slash_2.png").convert_alpha(),
            2: pygame.image.load("images/red_slash_3.png").convert_alpha(),
            3: pygame.image.load("images/red_slash_4.png").convert_alpha(),
            4: pygame.image.load("images/red_slash_5.png").convert_alpha(),
        }
    }
}

bg_menu_1 = pygame.image.load("images/menu.png").convert_alpha()
bg_menu = pygame.image.load("images/fonmenu.png").convert_alpha()
bg_menu_8 = pygame.image.load("images/menubg_8.png").convert_alpha()
bg_menu_7 = pygame.image.load("images/menubg_7.png").convert_alpha()
glav = pygame.image.load("images/glav.png").convert_alpha()
wood1 = pygame.image.load("images/wood1.png").convert_alpha()
bg_fon1izmen = pygame.image.load("images/fon1izmen.png").convert_alpha()
bg_fon1izmen_rect = bg_fon1izmen.get_rect()

bg = bg_fon1izmen

bgs = [
    bg_menu,
    bg_fon1izmen,
    bg_menu_1,
    bg_menu_7,
    bg_menu_8
]
menu_bg = bgs[0]

bg_rect = pygame.Rect(0, 0, WIDTH, HEIGHT) 

# Functions
def c_index_set(s):
    global c_index
    if s < 0: s = len(console)
    elif s > len(console): s = 0
    c_index = s

def clear():
    global console_log
    console_log = []

def log(text):
    console_log.append(str(text))
def print(text):
    console_log.append(str(text))

def input():
    console_log.append("no")

def help():
    global help_i
    if help_i == 0:
        log("Bro, you can change EVEREYHING why do you call for help?")
        log('Just type p.x = 999 or p.inv[0]["amount"] = 999')
    if help_i == 1:
        log("Bro, just type something cool in console and watch how it works")
    if help_i == 2:
        log("Bruh please stop")
    if help_i > 2 and help_i != 5 and help_i != 15:
        log("...")
    if help_i == 5:
        log("Just type sys.exit()")
    if help_i == 15:
        raise Exception("HelpException: So many help")
    help_i+=1

def text(text, x, y, size, col):
    font = pygame.font.Font("slkscr.ttf", size)
    rendertext = font.render(str(text), True, col) 
    textRect = rendertext.get_rect()
    textRect.left, textRect.top = x, y 
    return (rendertext, textRect)

def text_ru_en(text, x, y, size, col):
    font = pygame.font.Font("joystix.monospace-regular.ttf", size)
    rendertext = font.render(str(text), True, col) 
    textRect = rendertext.get_rect()
    textRect.left, textRect.top = x, y 
    return (rendertext, textRect)

def text_ru_en_lh(text, x, y, size, col):
    font = pygame.font.Font("PressStart2P-Regular.ttf", size)
    rendertext = font.render(str(text), True, col) 
    textRect = rendertext.get_rect()
    textRect.left, textRect.top = x, y 
    return (rendertext, textRect)



# Variables -----

# - Console
console_log = []
console_title = "Console"
console = ""
last_command = ""
alt = False
inConsole = False
c_index = 0
console_blocked = [pygame.K_RETURN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_ESCAPE, pygame.K_DELETE, pygame.K_BACKSPACE, pygame.K_TAB, pygame.K_RSHIFT, pygame.K_LSHIFT, pygame.K_RCTRL, pygame.K_LCTRL, pygame.K_LALT, pygame.K_RALT, pygame.K_CAPSLOCK, pygame.K_UP, pygame.K_DOWN]

# - Dialoge
dialoge = []
inDialoge = False
dialoge_draw_from = 0
dialoge_draw_to = 5

# - Other lists
itemsCollect = []
NPCs = []
objects = []

# - Time
curTime = 300
timeAdd = 1
timeMode = 1
day = 30000

# - Colors
TFColors = {
    False: (255,0,0),
    True: (123,255,123)
}

# - Biomes
biomes_map = {
    0: {"text": "Поляна", "biome": "", "rect": pygame.Rect(850,480,240,110)},
    1: {"text": "Деревня", "biome": "", "rect": pygame.Rect(700,70,380,120)},
    2: {"text": "Пещера", "biome": "", "rect": pygame.Rect(350,10,150,75)},
}

# - Unsoted
all_letters = string.printable+"АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
showfps = False
autoload = False
s = pygame.Surface((WIDTH,HEIGHT))
s.set_alpha(128)
s.fill((0,0,0))
s2 = pygame.Surface((WIDTH,HEIGHT))
s2.set_alpha(0)
s2.fill((0,0,0))
help_i = 0
rgb_temp = 0
mode = "menu"
inMap = True


# - Items System

# items ид предмета обозначается цифрой
# например 1: {"name":"Доски", "max": 0,
# 1 - ид предмета, name - имя, max - максимальное кол-во стака
# 
# когда добавляешь предмет не делай ид как у других, иначе заменится
# 5: {"name":"Ничего", "max": 0},
# 5: {"name":"Ничего", "max": 0},
# 5: {"name":"Ничего", "max": 0},
# 5: {"name":"Ничего", "max": 0},
# так не делай ^^^^
# это индивидуально значение предмета, как твой discord id
items = {
    0: {"name":"", "rarity": 0, "max": 0, "attributes": ["empty_sprite"], "sprite": None, "script": ""},
    1: {"name":"Доски", "rarity": 0, "max": 5, "attributes": [], "sprite": None, "script": ""},
    2: {"name":"Булыжник", "rarity": 0, "max": 5, "attributes": [], "sprite": None, "script": ""},
    3: {"name":"Яблоко", "rarity": 0, "max": 15, "attributes": [], "sprite": pygame.image.load("images/items/apple.png").convert_alpha(), "script": "p.hp += 2"},
    4: {"name":"Железный меч", "rarity": 1, "max": 1, "attributes": ["inf"], "sprite": pygame.image.load("images/items/sword1.png").convert_alpha(), "script": "objects.append(Slash(p.x+((['left', 'right'].index(p.lastDir)*100)+-50), p.y+50, 10, p.lastDir, 2))"},
    5: {"name":"Золотой мечь", "rarity": 1, "max": 1, "attributes": ["inf"], "sprite": pygame.image.load("images/items/sword2.png").convert_alpha(), "script": "objects.append(Slash(p.x+((['left', 'right'].index(p.lastDir)*100)+-50), p.y+50, 10, p.lastDir, 4))"},
    6: {"name":"Мечь смерти", "rarity": 4, "max": 1, "attributes": ["inf"], "sprite": pygame.image.load("images/items/death_sword.png").convert_alpha(), "script": "objects.append(Slash(p.x+((['left', 'right'].index(p.lastDir)*100)+-50), p.y+50, 10, p.lastDir, 100, 'red'))"},
    7: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    8: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    9: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    10: {"name":"Common", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    11: {"name":"Uncommon", "rarity": 1, "max": 999, "attributes": [], "sprite": None, "script": ""},
    12: {"name":"Rare", "rarity": 2, "max": 999, "attributes": [], "sprite": None, "script": ""},
    13: {"name":"Mythin", "rarity": 3, "max": 999, "attributes": [], "sprite": None, "script": ""},
    14: {"name":"Legendary", "rarity": 4, "max": 999, "attributes": [], "sprite": None, "script": ""},
    15: {"name":"DEV", "rarity": 5, "max": 999, "attributes": [], "sprite": None, "script": ""},
    16: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    17: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    18: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    19: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    20: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    21: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    22: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    23: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    24: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    25: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    26: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    27: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    28: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    29: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    30: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    31: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    32: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    33: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    34: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    35: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    36: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    37: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    38: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    39: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    40: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    41: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    42: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    43: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    44: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    45: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    46: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    47: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    48: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    49: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    40: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    41: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    42: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    43: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    44: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    45: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    46: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    47: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    48: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    49: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    50: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    51: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    52: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    53: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    54: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    55: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    56: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    57: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    58: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    59: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    50: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    51: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    52: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    53: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    54: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    55: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    56: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    57: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    58: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    59: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    60: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    61: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    62: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    63: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    64: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    65: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    66: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    67: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    68: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    69: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    70: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    71: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    72: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    73: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    74: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    75: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    76: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    77: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    78: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    79: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    80: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    81: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    82: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    83: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    84: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    85: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    86: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    87: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    88: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    89: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    90: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    91: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    92: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    93: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    94: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    95: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    96: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    97: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    98: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""},
    99: {"name":"Неназначеный предмет", "rarity": 0, "max": 999, "attributes": [], "sprite": None, "script": ""}  
}

rare = {
    0: (200,200,200),
    1: (255,255,255),
    2: (255,255,123),
    3: (130,0,130),
    4: (255,123,40),
    5: (-1,-1,-1)
}

inv = {
    0: {"id":0,"amount":0},
    1: {"id":0,"amount":0},
    2: {"id":0,"amount":0},
    3: {"id":0,"amount":0},
    4: {"id":0,"amount":0},
    5: {"id":0,"amount":0},
    6: {"id":0,"amount":0},
    7: {"id":0,"amount":0},
    8: {"id":0,"amount":0},
}





# Classes

class Camera(object):
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h, self.rect = x, y, w, h, pygame.Rect(x,y,w,h)
    def update(self):
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        
        if p.x < self.x + 250: self.x -= 5
        if p.x > self.w - 250: self.x += 5

class Menu(object):
    def __init__(self):
        self.options = {}
        self.option = 0
        self.index = 0
    def add_option(self, id_, name):
        self.options[id_] = {}
        self.options[id_]["name"] = name
        self.options[id_]["options"] = {}
    def add_suboption(self, option, name, id_, script, color = (255,255,255), arg1 = None, arg2 = None, arg3 = None):
        self.options[option]["options"][id_] = {}
        self.options[option]["options"][id_]["name"] = name
        self.options[option]["options"][id_]["color"] = color
        self.options[option]["options"][id_]["script"] = script
        self.options[option]["options"][id_]["arg1"] = arg1
        self.options[option]["options"][id_]["arg2"] = arg2
        self.options[option]["options"][id_]["arg3"] = arg3
    def draw(self):
        totalText = text_ru_en(self.options[self.option]["name"], 55, 55, 25, (255,255,255))
        screen.blit(totalText[0], totalText[1])
        for i in self.options[self.option]["options"]:
            totalText = text_ru_en(self.options[self.option]["options"][i]["name"], 75, 125+(30*i), 15, self.options[self.option]["options"][i]["color"])
            screen.blit(totalText[0], totalText[1])
        totalText = text(">", 55, 122+(30*self.index), 25, (255,255,0))
        screen.blit(totalText[0], totalText[1])
    def set_index(self, i):
        l = len(self.options[self.option]["options"])-1
        if i < 0: i = l
        elif i > l: i = 0
        self.index = i
    def interact(self):
        s = self.options[self.option]["options"][self.index]["script"]
        a1 = self.options[self.option]["options"][self.index]["arg1"]
        a2 = self.options[self.option]["options"][self.index]["arg2"]
        a3 = self.options[self.option]["options"][self.index]["arg3"]
        if s == "options": 
            self.option = a1
            self.index = 0
        elif s == "exit":
            if a1 != "nosave":
                with shelve.open("save/save") as f:
                    try:
                        f["p"] = p
                        f["itemsCollect"] = itemsCollect
                    except: pass
            pygame.quit()
            sys.exit()
        elif s == "setvar":
            t = ""
            if a3 == "global": t = f"global {a1}; "
            exec(f"{t}{a1} = {a2}")
        elif s == "addvar":
            t = ""
            if a3 == "global": t = f"global {a1}; "
            exec(f"{t}{a1} += {a2}")
        elif s == "nvar":
            t = ""
            if a3 == "global": t = f"global {a1}; "
            exec(f"{t}{a1} = not {a1}")
        elif s == "custom":
            exec(a1)

class CollectItem(object):
    def __init__(self, x, y, itemid):
        self.x, self.y, self.itemid = x, y, itemid
        self.acc = 0
        self.onGround = True
        if items[self.itemid]["sprite"] != None:
            t = items[self.itemid]["sprite"].get_rect()
        else: t = unknown_item.get_rect()
        self.rect = pygame.Rect(self.x, self.y, t.width, t.height)
        self.drawrect = pygame.Rect(self.rect.x-c.x, self.rect.y-c.y, self.rect.width, self.rect.height)
    def update(self):
        if self.y > 425: self.onGround = True
        else: self.onGround = False
        if items[self.itemid]["sprite"] != None:
            t = items[self.itemid]["sprite"].get_rect()
        else: t = unknown_item.get_rect()
        if not self.onGround:
            self.y += self.acc
            self.acc += 0.3
        else: self.acc = 0
        self.rect = pygame.Rect(self.x, self.y, t.width, t.height)
        self.drawrect = pygame.Rect(self.rect.x-c.x, self.rect.y-c.y, self.rect.width, self.rect.height)
    def draw(self):
        if items[self.itemid]["sprite"] != None:
            screen.blit(items[self.itemid]["sprite"], self.drawrect)
        else: screen.blit(unknown_item, self.drawrect)

class Slash(object):
    def __init__(self, x, y, lt, dirr, damage, spriteset = "normal"):
        self.x,self.y,self.lt,self.ltm = x,y,0,lt
        self.spriteset = spriteset
        self.damage = damage
        self.dirr = dirr
        self.w = self.ltm/len(spritesets["slash"][self.spriteset])
        self.l = 0
        self.sprite = 0
        t = spritesets["slash"][self.spriteset][self.sprite].get_rect()
        self.rect = pygame.Rect(self.x, self.y, t.width, t.height)
        self.drawrect = pygame.Rect(self.x, self.y, t.width, t.height)
    def update(self):
        global objects, NPCs
        if self.lt >= self.ltm:
            objects.remove(self)
        self.l+=1
        self.lt+=1
        if self.sprite < len(spritesets["slash"][self.spriteset]):
            t = spritesets["slash"][self.spriteset][self.sprite].get_rect()
            self.rect = pygame.Rect(self.x, self.y, t.width, t.height)
            self.drawrect = pygame.Rect(self.x, self.y, t.width, t.height)
        if self.l >= self.w:
            self.sprite+=1
            self.l = 0
        for n in NPCs:
            if isinstance(n, NPC):
                if pygame.Rect.colliderect(self.rect, n.rect):
                    if n.imune <= 0 and n.hp != "inf":
                        try:
                            n.hp-=self.damage
                            n.imune = 60
                            if n.hp <= 0:
                                NPCs.remove(n)
                            NPCs.remove(self)
                        except: pass
    def draw(self):
        if self.sprite < len(spritesets["slash"][self.spriteset]):
            if self.dirr != "left": screen.blit(spritesets["slash"][self.spriteset][self.sprite], self.drawrect)
            else: screen.blit(pygame.transform.flip(spritesets["slash"][self.spriteset][self.sprite], True, False), self.drawrect)


class Player(object):
    def __init__(self, x, y, hp, inv):
        self.x, self.y, self.hp, self.maxhp, self.inv = x, y, hp, hp, inv
        self.speed = 3
        self.jumpForce = 5
        self.acc = 0
        self.accAdd = 0.3
        self.sprite = "idle"
        t = spritesets["player"]["normal"][self.sprite].get_rect()
        self.rect = pygame.Rect(self.x, self.y, t.width, t.height)
        self.drawrect = pygame.Rect(self.rect.x-c.x, self.rect.y-c.y, self.rect.width, self.rect.height)
        self.canJump = True
        self.onGround = True
        self.lastDir = "left"
        self.jumpCount = 0
        self.curSlot = 0
        self.inv_draw_from = 0
        self.inv_draw_to = 17
    def draw(self):
        if self.curSlot > len(self.inv)-1: self.curSlot = len(self.inv)-1
        if self.curSlot > self.inv_draw_to:
            self.inv_draw_to = self.curSlot
            self.inv_draw_from = self.curSlot - 17
        if self.curSlot < self.inv_draw_from:
            self.inv_draw_to = self.curSlot + 17
            self.inv_draw_from = self.curSlot
        drawinv = [i for i in range(len(self.inv)) if i >= self.inv_draw_from and i <= self.inv_draw_to] #log([i for i in range(len(p.inv)) if i >= p.inv_draw_from and i <= p.inv_draw_to])
        for j, i in zip(range(len(drawinv)), drawinv):
            if i == self.curSlot: c = (135,135,135)
            else: c = (100,100,100)
            pygame.draw.rect(screen, c, pygame.Rect(50+(j*55), 540, 50, 50))
            if "empty_sprite" not in items[inv[i]["id"]]["attributes"]:
                if items[self.inv[i]["id"]]["sprite"] != None:
                    screen.blit(items[self.inv[i]["id"]]["sprite"],(55+(j*55),545))
                elif self.inv[i]["id"] != 0: screen.blit(unknown_item,(55+(j*55),545))
                if self.inv[i]["amount"] > 1:
                    totalText = text(str(self.inv[i]["amount"]), 55+(15+(j*55)), 575, 15, (255,255,255))
                    screen.blit(totalText[0], totalText[1])
        if self.inv_draw_to < len(self.inv)-1:
            totalText = text(f">", 1042, 540, 55, (255,255,0))
            screen.blit(totalText[0], totalText[1])
        if self.inv_draw_from > 0:
            totalText = text(f"<", 10, 540, 55, (255,255,0))
            screen.blit(totalText[0], totalText[1])
        temp = ""
        if self.inv[self.curSlot]["amount"] > 1: temp = f"x{self.inv[self.curSlot]['amount']}"
        c2 = rare[items[inv[self.curSlot]["id"]]["rarity"]]
        if c2 == (-1,-1,-1): 
            (r, g, b) = colorsys.hsv_to_rgb(rgb_temp, 1.0, 1.0)
            c2 = (int(255 * r), int(255 * g), int(255 * b))
        totalText = text_ru_en(f"{self.curSlot+1}/{len(inv)} {items[self.inv[self.curSlot]['id']]['name']} {temp}", 55, 505, 25, c2)
        screen.blit(totalText[0], totalText[1])
        screen.blit(spritesets["player"]["normal"][self.sprite], self.drawrect)
        if len(self.inv) > 15: pygame.draw.rect(screen, (100,100,100), pygame.Rect(60+(55*15), 500, 204, 24))
        else: pygame.draw.rect(screen, (100,100,100), pygame.Rect(60+(55*len(self.inv)), 555, 204, 24))
        if self.hp != "inf":
            if len(self.inv) > 15: pygame.draw.rect(screen, (123,255,123), pygame.Rect(60+(55*15), 502, (self.hp/self.maxhp)*200, 20))
            else: pygame.draw.rect(screen, (123,255,123), pygame.Rect(62+(55*len(self.inv)), 557, (self.hp/self.maxhp)*200, 20))
        else:
            if len(self.inv) > 15: 
                pygame.draw.rect(screen, (255,255,0), pygame.Rect(60+(55*15), 502, 200, 20))
                totalText = text("inf", (55*17), 502, 20, (0,0,0))
                screen.blit(totalText[0], totalText[1])
                totalText = text("inf", 1+(55*17), 503, 20, (255,255,255))
                screen.blit(totalText[0], totalText[1])
            else:
                pygame.draw.rect(screen, (255,255,0), pygame.Rect(62+(55*len(self.inv)), 557, 200, 20))
                totalText = text("inf", 162+(55*len(self.inv)), 556, 20, (0,0,0))
                screen.blit(totalText[0], totalText[1])
                totalText = text("inf", 162+(55*len(self.inv)), 557, 20, (255,255,255))
                screen.blit(totalText[0], totalText[1])
    def update(self):
        t = spritesets["player"]["normal"]["idle"].get_rect()
        if self.hp != "inf":
            if self.hp > self.maxhp: self.hp = self.maxhp
            if self.hp < 0: self.hp = 0

        if self.y >= 305: self.onGround = True
        else: self.onGround = False
        if self.jumpCount > 0:
            self.y -= self.jumpCount // self.jumpForce
            self.jumpCount -= 1
        
        if not self.onGround and not self.jumpCount:
            self.y += self.acc
            self.acc += self.accAdd
        else: self.acc = 0
        
        self.drawrect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)    
        self.rect = pygame.Rect(self.x, self.y, t.width, t.height)
    def move(self, dirr):
        if dirr == "left":# and self.x > 5:
            if self.sprite != "left": self.sprite = "left"
            self.x -= self.speed
            self.lastDir = "left"
        elif dirr == "right":# and self.x < 1030:
            if self.sprite != "right": self.sprite = "right"
            self.x += self.speed
            self.lastDir = "right"
        else: 
            if self.sprite != "idle": self.sprite = "idle"
    def jump(self):
        if self.onGround:
            self.jumpCount = 35
    def use(self, slot):
        itemSCR = items[inv[slot]["id"]]["script"]
        if "inf" not in items[inv[slot]["id"]]["attributes"]:
            self.inv[slot]["amount"]-=1
            if self.inv[slot]["amount"] <= 0: self.inv[slot]["id"] = 0
        if items[inv[slot]["id"]]["script"] != "":
            try:
                exec(itemSCR)
            except Exception as e:
                log(str(e))
    def slot(self, s):
        if s < 0: s = len(self.inv)-1
        elif s > len(self.inv)-1: s = 0
        self.curSlot = s
    def drop(self, s):
        global itemsCollect
        if "empty_sprite" not in items[self.inv[s]["id"]]["attributes"]:
            if self.lastDir == "left": itemsCollect.append(CollectItem(self.x-50, self.y+40, self.inv[s]["id"]))
            elif self.lastDir == "right": itemsCollect.append(CollectItem(self.x+90, self.y+40, self.inv[s]["id"]))
            self.inv[s]["amount"]-=1
            if self.inv[s]["amount"] <= 0: self.inv[s]["id"] = 0
    def set_slot(self, slot: int, id_ = 0, amount = 0):
        self.inv[slot] = {}
        self.inv[slot]["id"] = id_
        self.inv[slot]["amount"] = amount
    def tp(self, x: int, y: int, add = False):
        if not add: self.x, self.y = x, y
        else:
            self.x += x
            self.y += y
    def give(self, id_ = 0, amount = 0):
        for i in range(amount):
            smode = 0
            slotid = -1
            for slot in self.inv:
                if self.inv[slot]["id"] == id_ and self.inv[slot]["amount"] < items[self.inv[slot]["id"]]["max"]:
                    smode = 1
                    slotid = slot
                    break
            if smode == 0:
                for slot in self.inv:
                    if "empty_sprite" in items[self.inv[slot]["id"]]["attributes"]:
                        smode = 2 
                        slotid = slot
                        break
            if smode == 1:
                self.inv[slotid]["amount"] += 1
                return True
            elif smode == 2:
                self.inv[slotid]["amount"] += 1
                self.inv[slotid]["id"] = id_
                return True
            return False
            
class NPC(object):
    def __init__(self, x, y, hp, name, script = None, showHp = False):
        self.x,self.y,self.hp,self.script = x,y,hp,script
        self.maxhp = hp
        self.showHp = showHp
        self.name = name
        self.goCounter = 0
        self.imune = 0
        self.wait = randint(50, 150)
        self.going = None
        self.sprite = "idle"
        t = spritesets["player"]["normal"][self.sprite].get_rect()
        self.rect = pygame.Rect(self.x, self.y, t.width, t.height)
        self.drawrect = pygame.Rect(self.x, self.y, t.width, t.height)
    def update(self):
        if self.imune > 0: self.imune-=1
        if self.going != None:
            if self.going >= self.x: 
                self.x+=2
                self.sprite = "right"
            if self.going <= self.x: 
                self.x-=2
                self.sprite = "left"
            if self.going in [self.x, self.x+1, self.x+2, self.x+3, self.x-1, self.x-2, self.x-3]: 
                self.going = None
                self.sprite = "idle"
        if self.goCounter >= self.wait:
            self.goCounter = 0
            self.going = choice([None, self.x+randint(-150, 150)])
            self.wait = randint(50, 150)
        self.goCounter+=1
        t = spritesets["player"]["normal"][self.sprite].get_rect()
        self.rect = pygame.Rect(self.x, self.y, t.width, t.height)
        self.drawrect = pygame.Rect(self.x, self.y, t.width, t.height)
    def draw(self):
        screen.blit(spritesets["player"]["normal"][self.sprite], self.drawrect)
        totalText = text_ru_en_lh(self.name, self.x, self.y-25, 20, (255,255,255))
        screen.blit(totalText[0], totalText[1])
        if self.showHp or self.hp < self.maxhp and self.hp != "inf":
            pygame.draw.rect(screen, (100,100,100), pygame.Rect(self.x, self.y+20, 82, 12))
            pygame.draw.rect(screen, (123,255,123), pygame.Rect(self.x+1, self.y+21, (self.hp/self.maxhp)*80, 8))
    def interact(self):
        if self.script != None:
            try:
                exec(self.script)
            except Exception as e:
                console_log.append(str(e))











# Finaly
menu = Menu()
menu.add_option(0, "Главное меню")
menu.add_suboption(0, "Продолжить", 0, "setvar", arg1 = "mode", arg2 = "'game'",  arg3 = "global", color = (123,255,123))
menu.add_suboption(0, "Настройки", 1, "options", arg1 = 1)
menu.add_suboption(0, "Выйти", 2, "exit", color = (255,0,0))
menu.add_option(1, "Настройки")
menu.add_suboption(1, "Назад", 0, "options", arg1 = 0)
menu.add_suboption(1, "Музыка и звуки", 1, "options", arg1 = 2)
menu.add_suboption(1, "Показывать FPS", 2, "custom", arg1 = "global showfps; showfps, menu.options[menu.option]['options'][menu.index]['color'] = not showfps, TFColors[not showfps]", color = (255,0,0))
menu.add_suboption(1, f"Фон меню {bgs.index(menu_bg)+1}/{len(bgs)}", 3, "custom", arg1 = compile("""
global menu_bg, bgs
g = bgs.index(menu_bg)
g+=1
if g > len(bgs)-1: g = 0
menu_bg, menu.options[menu.option]['options'][menu.index]['name'] = bgs[g], 'Фон меню '+str(g+1)+'/'+str(len(bgs))
""", 'mulstring', 'exec'))
menu.add_option(2, "Музыка и звуки")
menu.add_suboption(2, "Назад", 0, "options", arg1 = 1)

c = Camera(0,0,WIDTH,HEIGHT)
p = Player(400, 311, 20, inv)
NPCs.append(NPC(500, 311, 20, "Вася", "global inDialoge; inDialoge = True; dialoge.append('Привет')"))


# Load save
if autoload:
    with shelve.open("save/save") as f:
        try:
            p = f["p"]
            itemsCollect = f["itemsCollect"]
        except: pass



  

p.give(4, 1)

# Load mods
for filename in os.listdir('mods/'):
    if filename.endswith(".mod.py"):
        try:
            exec(open("mods/"+filename, encoding = "utf_8").read())
            log(f"{filename} loaded")
        except Exception as e: log(f"{filename} mod error: {e}")



while running:
    tc = int(((day-curTime)/60)/2)
    screen.fill((int(tc/2),tc,tc))
    if mode == "menu":
        screen.blit(menu_bg, bg_rect)
        menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with shelve.open("save/save") as f:
                    try:
                        f["p"] = p
                        f["itemsCollect"] = itemsCollect
                    except: pass
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not inConsole:
                if event.button == 4: menu.set_index(menu.index-1)
                elif event.button == 5: menu.set_index(menu.index+1)
            if event.type == pygame.KEYDOWN:
                if not inConsole:
                    if event.unicode == 'w' or event.unicode == 'ц': menu.set_index(menu.index-1)
                    if event.unicode == 's' or event.unicode == 'ы': menu.set_index(menu.index+1)
                    if event.key == pygame.K_UP: menu.set_index(menu.index-1)
                    if event.key == pygame.K_DOWN: menu.set_index(menu.index+1)
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN: menu.interact()
                    if event.key == pygame.K_TAB and _dev: inConsole = not inConsole
                elif inConsole:
                    if event.key == pygame.K_TAB: inConsole = not inConsole
                    if event.key == pygame.K_LEFT: c_index_set(c_index-1)
                    if event.key == pygame.K_RIGHT: c_index_set(c_index+1)
                    if event.key == pygame.K_UP: console, c_index = last_command, len(last_command)
                    if event.key == pygame.K_RALT or event.key == pygame.K_LALT: alt = not alt
                    if alt and event.key == pygame.K_BACKSPACE: console, c_index = "", 0
                    if alt and event.key == pygame.K_c: pyperclip.copy(console)
                    elif alt and event.key == pygame.K_v: 
                        h = pyperclip.paste()
                        if c_index == len(console):
                            console+=h
                            c_index+=len(h)
                        else:
                            console = list(console)
                            console.insert(c_index, h)
                            console = "".join(console)
                            c_index+=len(h)
                    elif event.key not in console_blocked and event.unicode in all_letters and not alt:
                        if c_index == len(console):
                            console+=event.unicode
                            c_index+=1
                        else:
                            console = list(console)
                            console.insert(c_index, event.unicode)
                            console = "".join(console)
                            c_index+=1
                        
                    elif event.key == pygame.K_BACKSPACE and len(console[:c_index]) > 0 and not alt: 
                        if c_index < len(console):
                            console = list(console)
                            console[c_index-1] = ""
                            console = "".join(console)
                        else: console = console[:c_index-1]
                        c_index-=1

                    elif event.key == pygame.K_RETURN and not alt:
                        try:
                            exec(console)
                            console_log.append(str(console))
                            last_command = console
                            console = ""
                            c_index = 0
                        except Exception as e:
                            console_log.append(str(e))
    elif mode == "game":
        screen.blit(bg, bg_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with shelve.open("save/save") as f:
                    try:
                        f["p"] = p
                        f["itemsCollect"] = itemsCollect
                    except: pass
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not inConsole and not inDialoge and not inMap:
                if event.button == 4: p.slot(p.curSlot-1)
                elif event.button == 5: p.slot(p.curSlot+1)
                elif event.button == 1: p.use(p.curSlot)
            elif event.type == pygame.MOUSEBUTTONDOWN and not inConsole and inDialoge and not inMap:
                if event.button == 4:
                    if dialoge_draw_to > len(dialoge)-1:
                        dialoge_draw_from+=1
                        dialoge_draw_to+=1
                elif event.button == 5:
                    if dialoge_draw_from > 0:
                        dialoge_draw_from-=1
                        dialoge_draw_to-=1
            if event.type == pygame.KEYDOWN:
                if not inConsole:
                    if not inMap:
                        if event.unicode == '1': p.slot(0)
                        if event.unicode == '2': p.slot(1)
                        if event.unicode == '3': p.slot(2)
                        if event.unicode == '4': p.slot(3)
                        if event.unicode == '5': p.slot(4)
                        if event.unicode == '6': p.slot(5)
                        if event.unicode == '7': p.slot(6)
                        if event.unicode == '8': p.slot(7)
                        if event.unicode == '9': p.slot(8)
                        if event.unicode == 'q' or event.unicode == 'й': p.drop(p.curSlot)
                    if event.key == pygame.K_TAB and _dev: inConsole = not inConsole
                    if event.key == pygame.K_ESCAPE and not inDialoge: mode = "menu"
                    if event.key == pygame.K_m: inMap = not inMap
                    elif event.key == pygame.K_RETURN:
                        if inDialoge:
                            inDialoge = False
                            dialoge = []
                        else:
                            for n in NPCs:
                                if pygame.Rect.colliderect(p.rect, n.rect):
                                    n.interact()
                else:
                    if event.key == pygame.K_TAB: inConsole = not inConsole
                    if event.key == pygame.K_LEFT: c_index_set(c_index-1)
                    if event.key == pygame.K_RIGHT: c_index_set(c_index+1)
                    if event.key == pygame.K_UP: console, c_index = last_command, len(last_command)
                    if event.key == pygame.K_RALT or event.key == pygame.K_LALT: alt = not alt
                    if alt and event.key == pygame.K_BACKSPACE: console, c_index = "", 0
                    if alt and event.key == pygame.K_c: pyperclip.copy(console)
                    elif alt and event.key == pygame.K_v: 
                        h = pyperclip.paste()
                        if c_index == len(console):
                            console+=h
                            c_index+=len(h)
                        else:
                            console = list(console)
                            console.insert(c_index, h)
                            console = "".join(console)
                            c_index+=len(h)
                    elif event.key not in console_blocked and event.unicode in all_letters and not alt:
                        if c_index == len(console):
                            console+=event.unicode
                            c_index+=1
                        else:
                            console = list(console)
                            console.insert(c_index, event.unicode)
                            console = "".join(console)
                            c_index+=1
                        
                    elif event.key == pygame.K_BACKSPACE and len(console[:c_index]) > 0 and not alt: 
                        if c_index < len(console):
                            console = list(console)
                            console[c_index-1] = ""
                            console = "".join(console)
                        else: console = console[:c_index-1]
                        c_index-=1

                    elif event.key == pygame.K_RETURN and not alt:
                        try:
                            exec(console)
                            console_log.append(str(console))
                            last_command = console
                            console = ""
                            c_index = 0
                        except Exception as e:
                            console_log.append(str(e))
        if not inConsole:
            pressed = pygame.key.get_pressed() 
            if pressed[pygame.K_a]: p.move("left")
            elif pressed[pygame.K_d]: p.move("right")
            else: p.move("none")
            if pressed[pygame.K_SPACE]: p.jump()
        iposses = []
        for item in itemsCollect:
            if (item.x, item.y) not in iposses:
                item.draw()
                iposses.append((item.x, item.y))
            item.update()
            if pygame.Rect.colliderect(p.rect, item.rect):
                if p.give(item.itemid, 1): itemsCollect.remove(item)
        for n in NPCs:
            n.update()
            n.draw()
        for o in objects:
            o.update()
            o.draw()
        s2.set_alpha(abs((((day-curTime)/60)/5)-100))
        screen.blit(s2, (0,0))
        p.update()
        p.draw()
        drawtext = [i for i in range(len(dialoge)) if i >= dialoge_draw_from and i <= dialoge_draw_to]
        if inDialoge:
            pygame.draw.rect(screen, (90,90,90), pygame.Rect(100, 50, 900, 200))
            pygame.draw.rect(screen, (120,120,120), pygame.Rect(110, 60, 880, 180))
            j=0
            for i in drawtext:
                totalText = text_ru_en_lh(dialoge[i], 120, 70+(j*30), 25, (255,255,255))
                screen.blit(totalText[0], totalText[1])
                j+=1
        if inMap:
            screen.blit(map_world, (0,0))
            for i in range(len(biomes_map)):
                b = pygame.Surface((biomes_map[i]["rect"].width,biomes_map[i]["rect"].height))
                b.fill((123,255,123))
                b.set_alpha(128)
                screen.blit(b, biomes_map[i]["rect"])
                totalText = text_ru_en_lh(biomes_map[i]["text"], 30, 30, 15, (255,255,255))
                totalText[1].center = (biomes_map[i]["rect"].x+(biomes_map[i]["rect"].width/2), biomes_map[i]["rect"].y+10)
                screen.blit(totalText[0], totalText[1])
                

        if timeMode == 1:
            curTime+=timeAdd
            if curTime >= day:
                timeMode = 2
        elif timeMode == 2:
            curTime-=timeAdd
            if curTime <= 0:
                timeMode = 1
    if showfps:
        totalText = text(f"{clock.get_fps():2.0f} FPS", 60, 30, 20, (255,255,255))
        screen.blit(totalText[0], totalText[1])
        
    if inConsole:
        screen.blit(s, (0,0))
        totalText = text(str(console_title), 30, 30, 30, (255,255,255))
        screen.blit(totalText[0], totalText[1])
        totalText = text_ru_en_lh(console[:c_index] + "|" + console[c_index:], 20, 550, 10, (255,255,255))
        screen.blit(totalText[0], totalText[1])
        if alt:
            totalText = text("ALT", 900, 570, 20, (255,255,255))
            screen.blit(totalText[0], totalText[1])
        i = 1
        for j in console_log:
            if i == 20: break
            totalText = text_ru_en_lh(console_log[-i], 20, 500-(15*i), 10, (255,255,255))
            screen.blit(totalText[0], totalText[1])
            i+=1
    if _dev:
        (r, g, b) = colorsys.hsv_to_rgb(rgb_temp, 1.0, 1.0)
        (r2, g2, b2) = colorsys.hsv_to_rgb(rgb_temp+0.03, 1.0, 1.0)
        (r3, g3, b3) = colorsys.hsv_to_rgb(rgb_temp+0.06, 1.0, 1.0)
        totalText = text("D", 978, 30, 20, (int(255 * r), int(255 * g), int(255 * b)))
        screen.blit(totalText[0], totalText[1])
        totalText = text("E", 990, 30, 20, (int(255 * r2), int(255 * g2), int(255 * b2)))
        screen.blit(totalText[0], totalText[1])
        totalText = text("V", 1000, 30, 20, (int(255 * r3), int(255 * g3), int(255 * b3)))
        screen.blit(totalText[0], totalText[1])
    rgb_temp += 0.005
    clock.tick(FPS) 
    pygame.display.flip()
