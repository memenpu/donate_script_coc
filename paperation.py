import io

from ppadb.client import Client as AdbClient

from PIL import Image
from retangle import Rectangle
import constants as c
import numpy
import time
import find_image_similarity

temp_img = f"temp.png"


def main(img_path=r'full.png'):
    # Default is "127.0.0.1" and 5037
    client = AdbClient(host="127.0.0.1", port=5037)
    print(client.devices())
    print(client.version())
    device = client.devices()[0]
    image = device.screencap()
    Image.open(io.BytesIO(image)).save(img_path)
    # print(image)
    # screenshot = img_path
    # save_screenshot = screenshot.split(".")[0]+"_25.png"
    # with open(screenshot, 'wb') as f:
    #     f.write(image)
    # Image.frombytes('RGBA', (1920,1080), bytes(image), 'raw').save(img_path)
    return Image.open(img_path)


def crop_queue_troops(image_path):
    image = Image.open(image_path)
    rectangle1 = Rectangle(250, 670, 111, 80)
    rectangle2 = Rectangle(250, 860, 111, 80)
    hg = 433-250
    # row_1_start_point = (rectangle1.x, rectangle1.y)
    # row_2_start_point = (rectangle2.x, rectangle2.y)
    # row_1_troops = [c.barbarian, c.giant, c.wall_breaker, c.wizard, c.healer, c.pekka, c.miner, c.yeti]
    # row_2_troops = [c.archer, c.super_giant, c.balloon, c.super_wizard, c.dragon, c.baby_dragon, c.electro_dragon, c.unknown]
    row_1_troops = [c.unknown for i in range(10)]
    # row_2_troops = [c.heal_spell, c.jump_spell, c.clone_spell, c.unknown, c.earthquake_spell, c.skeleton_spell, c.unknown, c.unknown]
    row_2_troops = [c.unknown for i in range(10)]
    row_2_troops.insert(3, c.dragon)
    # 8 × 2
    for i in range(8):
        image.crop(rectangle1.x1_y1_x2_y2(plus_x=i*hg)).save(row_1_troops[i].queue)
        image.crop(rectangle2.x1_y1_x2_y2(plus_x=i*hg)).save(row_2_troops[i].queue)


def crop_queue_troops2(image_path):
    image = Image.open(image_path)
    rectangle1 = Rectangle(252, 670, 111, 80)
    rectangle2 = Rectangle(252, 860, 111, 80)
    hg = 433-250
    # row_1_start_point = (rectangle1.x, rectangle1.y)
    # row_2_start_point = (rectangle2.x, rectangle2.y)
    row_1_troops = [c.healer, c.pekka, c.miner, c.yeti, c.minion, c.valkyrie, c.witch, c.bowler]
    row_2_troops = [c.dragon, c.baby_dragon, c.electro_dragon, c.unknown, c.hog_rider,c.golem, c.lava_hound, c.ice_golem]
    # 8 × 2
    for i in range(8):
        image.crop(rectangle1.x1_y1_x2_y2(plus_x=i*hg)).save(row_1_troops[i].queue)
        image.crop(rectangle2.x1_y1_x2_y2(plus_x=i*hg)).save(row_2_troops[i].queue)


def crop_queue_spell(image_path):
    image = Image.open(image_path)
    rectangle1 = Rectangle(250, 670, 111, 80)
    rectangle2 = Rectangle(250, 860, 111, 80)
    hg = 434 - 250
    # row_1_start_point = (rectangle1.x, rectangle1.y)
    # row_2_start_point = (rectangle2.x, rectangle2.y)
    # row_1_troops = [c.lightning_spell, c.rage_spell, c.freeze_spell, c.invisibility_spell, c.poision_spell, c.hast_spell, c.bat_spell]
    row_1_troops = [c.unknown for i in range(10)]
    row_1_troops.insert(2, c.super_giant)
    # row_2_troops = [c.heal_spell, c.jump_spell, c.clone_spell, c.unknown, c.earthquake_spell, c.skeleton_spell, c.unknown, c.unknown]
    row_2_troops =  [c.unknown for i in range(10)]
    # 8 × 2
    for i in range(7):
        image.crop(rectangle1.x1_y1_x2_y2(plus_x=i * hg)).save(row_1_troops[i].queue)
        image.crop(rectangle2.x1_y1_x2_y2(plus_x=i* hg)).save(row_2_troops[i].queue)


def crop_donate_troops(image_path):
    image = Image.open(image_path)
    # (636, 357, 118, 151)
    # left top right bottom
    # x1, y1, x2, y2
    # (636, 357, 636+118,357+151)  (391,797)
    # 383-209 = 174 width
    width = 118 - 50
    # 797-621 = 176 height
    height = 108
    # horizontal gap: 391-383 = 7,
    hg = 8.5 + 50
    # vertical gap: 811-797 = 14,
    vg = 54
    x_start = 638 + 44
    y_start = 360
    # row_1_troops = [c.balloon, c.archer, c.super_giant, c.unknown, c.unknown, c.unknown,c.unknown,c.unknown, c.unknown]
    row_1_troops = [c.unknown for i in range(9)]
    row_1_troops.insert(4, c.dragon)
    row_2_troops = [c.unknown for i in range(9)]
    row_3_spells = [c.unknown for x in range(9)]
        # row_3_spells = [c.lightning_spell, c.rage_spell, c.freeze_spell, c.invisibility_spell, c.hast_spell,  c.skeleton_spell, c.unknown,
    #                 c.unknown]
    row_1_start_point = (x_start, y_start)
    row_2_start_point = (x_start, y_start + height + vg)
    # spell (638, 743, 119, 153)
    r3_vg = 384
    row_3_start_point = (x_start, row_1_start_point[1] + r3_vg)
    # 8 × 2
    for i in range(8):
        image.crop((*row_1_start_point, row_1_start_point[0] + width, row_1_start_point[1] + height)).save(
            row_1_troops[i].donate)
        row_1_start_point = (row_1_start_point[0] + width + hg, row_1_start_point[1])
        image.crop((*row_2_start_point, row_2_start_point[0] + width, row_2_start_point[1] + height)).save(
            row_2_troops[i].donate)
        row_2_start_point = (row_2_start_point[0] + width + hg, row_2_start_point[1])
        image.crop((*row_3_start_point, row_3_start_point[0] + width, row_3_start_point[1] + height)).save(
            row_3_spells[i].donate)
        row_3_start_point = (row_3_start_point[0] + width + hg, row_3_start_point[1])


def crop_queue_spells(image):
    # left top right bottom
    # x1, y1, x2, y2
    # (209, 621, 383,797)  (391,797)
    # 383-209 = 174 width
    width = 174
    # 797-621 = 176 height
    height = 176
    # horizontal gap: 391-383 = 7,
    hg = 9
    # vertical gap: 811-797 = 14,
    vg = 14
    row_1_start_point = (207, 621)
    row_2_start_point = (207, 621 + height + vg)
    # 8 × 2
    set_once = True
    for i in range(8):
        if i > 3 and set_once:
            row_1_start_point = (row_1_start_point[0] + hg, 621)
            row_2_start_point = (row_2_start_point[0] + hg, row_2_start_point[1])
            set_once = False
        image.crop((*row_1_start_point, row_1_start_point[0] + width, 797)).save(f"queue/r1s{i}.png")
        row_1_start_point = (row_1_start_point[0] + width + hg, 621)
        image.crop((*row_2_start_point, row_2_start_point[0] + width, row_2_start_point[1] + height)).save(
            f"queue/r2s{i}.png")
        row_2_start_point = (row_2_start_point[0] + width + hg, row_2_start_point[1])


def crop_request_troops(image, request_max=False):
    width = 47
    height = 88
    hg = 0.2
    # left most 65 right most 160
    row_1_start_point = (62 + width, 884 + height / 2)
    # 8 × 2

    for i in range(4):
        image.crop((*row_1_start_point, row_1_start_point[0] + width, 896 + height)).save(f"request/r1{i}.png")
        row_1_start_point = (row_1_start_point[0] + width * 2 + hg, row_1_start_point[1])


# def queue_is_full(image):
#     image.crop((315, 220, 318+56, 220+25)).save(temp_img)
#     same_images = find_image_similarity.find_similar_images(screenshot, temp_img)
#     return len([x[1] for x in same_images if x[1] == 220]) == 2


def train(troops):
    pass


if __name__ == '__main__':
    main('super_dragon.png')
    # image_path = r"default.png"
    # screenshot = main(image_path)
    # print(queue_is_full(screenshot))
    # crop_queue_spells(screenshot)
    # crop_donate_troops(image_path)
    # crop_queue_troops(image_path)
    # crop_queue_troops2(r"train_troops1.png")
    # crop_queue_spell(r"brew_spells.png")
