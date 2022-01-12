from enum import Enum
import cv2
from PIL import Image


class TroopType(Enum):
    NORMAL = 1
    SPELL = 2
    SIEGE_MACHINE = 3


class Troop:
    def __init__(self, name, troop_type: TroopType = TroopType.NORMAL, swipe: bool = False):
        self.name = name
        # self.request = fr"request/{name}.png"
        self.donate = fr"donate/{name}.png"
        self.queue = fr"queue/{name}.png"
        # self.request_image = cv2.imread(self.request, 0)
        self.donate_image = cv2.imread(self.donate, 0)
        self.queue_image = cv2.imread(self.queue, 0)
        self.troop_type = troop_type
        self.swipe = swipe

    def __str__(self):
        return self.name


barbarian = Troop("barbarian")
giant = Troop("giant")
wall_breaker = Troop("wall_breaker")
balloon = Troop("balloon")
super_wizard = Troop("super_wizard")
dragon = Troop("dragon")
super_dragon = Troop("super_dragon")
baby_dragon = Troop("baby_dragon")
electro_dragon = Troop("electro_dragon")
minion = Troop("minion", swipe=True)
head_hunter = Troop("head_hunter", swipe=True)

archer = Troop("archer")
super_archer = Troop("super_archer")
goblin = Troop("goblin")
super_wall_breaker = Troop("super_wall_breaker")
super_giant = Troop("super_giant")
wizard = Troop("wizard")
healer = Troop("healer")
pekka = Troop("pekka")
miner = Troop("miner")
yeti = Troop("yeti")
bowler = Troop("bowler", swipe=True)
valkyrie = Troop("valkyrie", swipe=True)
witch = Troop("witch", swipe=True)
golem = Troop("golem", swipe=True)
ice_golem = Troop("ice_golem", swipe=True)
lava_hound = Troop("lava_hound", swipe=True)
hog_rider = Troop("hog_rider", swipe=True)

freeze_spell = Troop("freeze_spell", TroopType.SPELL)
rage_spell = Troop("rage_spell", TroopType.SPELL)
invisibility_spell = Troop("invisibility_spell", TroopType.SPELL)
lightning_spell = Troop("lightning_spell", TroopType.SPELL)
poision_spell = Troop("poision_spell", TroopType.SPELL)
hast_spell = Troop("hast_spell", TroopType.SPELL)
bat_spell = Troop("bat_spell", TroopType.SPELL)
heal_spell = Troop("heal_spell", TroopType.SPELL)
jump_spell = Troop("jump_spell", TroopType.SPELL)
clone_spell = Troop("clone_spell", TroopType.SPELL)
earthquake_spell = Troop("earthquake_spell", TroopType.SPELL)
skeleton_spell = Troop("skeleton_spell", TroopType.SPELL)
siege_barracks = Troop("siege_barracks", TroopType.SIEGE_MACHINE)
stone_slammer = Troop("stone_slammer", TroopType.SIEGE_MACHINE)
wall_wrecker = Troop("wall_wrecker", TroopType.SIEGE_MACHINE)
battle_blimp = Troop("battle_blimp", TroopType.SIEGE_MACHINE)
log_launcher = Troop("log_launcher", TroopType.SIEGE_MACHINE)
flame_flinger = Troop("flame_flinger", TroopType.SIEGE_MACHINE, swipe=True)
unknown = Troop("unknown")

# target_images
OPEN_CHAT_IMG = cv2.imread(r"buttons/open_chat.png", 0)
ClOSE_CHAT_IMG = cv2.imread(r"buttons/close_chat.png", 0)
DONATE_IMG = cv2.imread(r"buttons/donate_button.png", 0)
DONATE_PADDING_IMG = cv2.imread(r"buttons/donate_padding.png", 0)
DRAG_CANCEL = cv2.imread(r"buttons/drag_cancel.png", 0)
CLOSE_BUTTON = cv2.imread(r"buttons/close_button.png", 0)
ZERO_TROOP = cv2.imread(r"buttons/zero_troop.png", 0)
JUMP_UP = cv2.imread(r"buttons/unread_up.png", 0)
JUMP_DOWN = cv2.imread(r"buttons/unread_down.png", 0)

TRAIN_BUTTON = cv2.imread(r"buttons/train_button.png", 0)
TRAIN_TROOPS = cv2.imread(r"buttons/train_troops.png", 0)
BREW_SPELLS = cv2.imread(r"buttons/brew_spells.png", 0)
BUILD_SIEGE_MACHINES = cv2.imread(r"buttons/build_siege_machines.png", 0)


def is_grey_scale(img_path):
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            # print([r,g, b])
            color_range = range(g - 20, g + 20)
            if (not (r in color_range and g in color_range and b in color_range)) and r != 255:
                # print([r, g, b])
                return False
    return True


def is_grey_scale_img(im):
    img = im.convert('RGB')

    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            # print([r,g, b])
            color_range = range(g - 50, g + 50)
            if (not (r in color_range and g in color_range and b in color_range)) and r != 255:
                # if r != g != b:
                return False
    return True


def foreach(items, function):
    for i in items:
        function(i)

# print(is_grey_scale(r"donate/rage_spell.png"))
# print(is_grey_scale(r"donate/balloon.png"))
# print(is_grey_scale(r"slammer_train.png"))
# print(is_grey_scale(r"temp.png"))
