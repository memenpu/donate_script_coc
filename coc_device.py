import io
import time
import collections

import cv2
from PIL import Image
from ppadb.device import Device
import constants as c
from find_image_similarity import find_similar_images
from ppadb.client import Client as AdbClient
from retangle import Rectangle
from typing import List
import numpy as np


class DonateState:
    def __init__(self, troop: c.Troop):
        self.troop = troop
        self.number_of_donate = 0

    def __str__(self):
        return f"{self.troop.name}: {self.number_of_donate}"


class Grayscale(DonateState):
    def __init__(self, troop: c.Troop):
        DonateState.__init__(self, troop)

    def __str__(self):
        return f"{self.troop.name}: {self.number_of_donate} is grayscale not tappable."


class TroopDonateFinished(DonateState):
    def __init__(self, troop: c.Troop):
        DonateState.__init__(self, troop)

    def __str__(self):
        return f"{self.troop.name}: {self.number_of_donate} is not found."


class Donated(DonateState):
    def __init__(self, troop: c.Troop, number_of_donate):
        DonateState.__init__(self, troop)
        self.number_of_donate = number_of_donate

    def __str__(self):
        return f"{self.troop.name} is donated {self.number_of_donate}."


class COCDevice(Device):

    def donate_troop(self, troop: c.Troop, take_new_screenshot=True) -> DonateState:
        """
        will donate a type troops until the cc fill up or no enough this type of troops
        :param troop:
        :param take_new_screenshot:
        :return:
        :rtype: number of donation
        """
        donate_state = DonateState(troop)
        while True:
            if not take_new_screenshot:
                state = self.find_donate_troop_and_tap_on_it(troop, take_new_screenshot)
                take_new_screenshot = not take_new_screenshot
            else:
                state = self.find_donate_troop_and_tap_on_it(troop, take_new_screenshot)
            if type(state) is Donated:
                donate_state.number_of_donate += 1
            else:
                print(state)
                donate_state.number_of_donate += state.number_of_donate
                return donate_state

    def find_donate_troop_and_tap_on_it(self, troop: c.Troop, take_new_screenshot) -> DonateState:
        """
        will try to donate a type of troop
        :param troop:
        :param take_new_screenshot:
        :return:
        """
        time.sleep(.5)
        image = self.screencap()
            # with open(c.screenshot_path, 'wb') as f:
            #     f.write(image)
        image = Image.open(io.BytesIO(image))
        if found := find_similar_images(image, troop.donate_image,
                                        filter_function=lambda x, y: x > 200, exist_image=c.CLOSE_BUTTON):
            found = found[0].x_y_w_h
            img = image.crop(
                (found[0] + 4, found[1] + 4, found[0] + found[2] - 8, found[1] + found[3] - 8))
            img = img.convert("RGB")
            if c.is_grey_scale_img(img):
                return Grayscale(troop)
            self.tap_on_rectangle(Rectangle(*found))
            return Donated(troop, 1)
        return TroopDonateFinished(troop)

    def find_control(self, control, filter_function=None, tap_on_it=True) -> List[Rectangle]:
        time.sleep(.5)
        image = self.screencap()
        # with open(c.screenshot_path, 'wb') as f:
        #     f.write(image)
        if not filter_function:
            if found := find_similar_images(Image.open(io.BytesIO(image)), control):
                if tap_on_it:
                    self.tap_on_rectangle(found[0])
                return found
            return []

        if found := find_similar_images(Image.open(io.BytesIO(image)), control,
                                        filter_function=filter_function):
            if tap_on_it:
                self.tap_on_rectangle(found[0])
            return found
        return []

    def donate_finished(self):
        """
        see if the donate window closed automatically or not
        :return:
        """
        image = self.screencap()
        # with open(c.screenshot_path, 'wb') as f:
        #     f.write(image)
        if not find_similar_images(Image.open(io.BytesIO(image)), c.CLOSE_BUTTON):
            return True
        else:
            return False

    def train_donated_troops(self, donated_troops: collections.Counter):
        # will_donate_troop_spell = False
        will_donate_troop_spell = True

        self.find_control(c.TRAIN_BUTTON)
        # train troops
        troops = {a: b for a, b in donated_troops.items() if a.troop_type is c.TroopType.NORMAL and b > 0}
        self.find_control(c.TRAIN_TROOPS)
        # no need swipe
        troops1 = {a: b for a, b in troops.items() if not a.swipe}
        if will_donate_troop_spell:
            print("train ", "; ".join([f"{x.name}: {y}" for x, y in troops1.items()]))
            for x, donated_count in troops1.items():
                if found := self.find_control(x.queue_image, tap_on_it=False):
                    for i in range(donated_count):
                        self.tap_on_rectangle_x_y2(found[0])
                        time.sleep(.25)

        troops1 = {a: b for a, b in troops.items() if a.swipe}
        if will_donate_troop_spell:
            print("train ", "; ".join([f"{x.name}: {y}" for x, y in troops1.items()]))
            # self.find_control(c.TRAIN_TROOPS_PATH)~~
            self.input_swipe(925, 807, 50, 807, 500)
            time.sleep(0.5)
            for x, donated_count in troops1.items():
                if found := self.find_control(x.queue_image, tap_on_it=False):
                    for i in range(donated_count):
                        self.tap_on_rectangle_x_y2(found[0])
                        time.sleep(.25)
        # train spells
        # if len(troops):
        troops = {a: b for a, b in donated_troops.items() if a.troop_type is c.TroopType.SPELL and b > 0}
        self.find_control(c.BREW_SPELLS)
        print("train ",len(troops), "; ".join([f"{x.name}: {y}" for x, y in troops.items()]))
        if will_donate_troop_spell:
            for x, donated_count in troops.items():
                if found := self.find_control(x.queue_image, tap_on_it=False):
                    for i in range(donated_count):
                        self.tap_on_rectangle_x_y2(found[0])
                        time.sleep(.25)

        # train siege machines
        troops = {a: b for a, b in donated_troops.items() if
                  a.troop_type is c.TroopType.SIEGE_MACHINE and b > 0}
        self.find_control(c.BUILD_SIEGE_MACHINES)
        print("train ", "; ".join([f"{x.name}: {y}" for x, y in troops.items()]))
        for x, donated_count in troops.items():
            if found := self.find_control(x.queue_image, tap_on_it=False):
                for i in range(donated_count):
                    self.tap_on_rectangle_x_y2(found[0])
                    time.sleep(.25)
        self.find_control(c.TRAIN_BUTTON)

    def tap_on_rectangle(self, rectangle_area: Rectangle):
        self.input_tap(*rectangle_area.x1_y1_center)

    def tap_on_rectangle_x_y2(self, rectangle_area: Rectangle):
        self.input_tap(rectangle_area.x, rectangle_area.y2)

    def control_exist_at(self, source_image_path, rectangle_area):
        time.sleep(.5)
        image = self.screencap()
        # with open(c.screenshot_path, 'wb') as f:
        #     f.write(image)

        if find_similar_images(Image.open(io.BytesIO(image)), cv2.cvtColor(np.array(image.crop((rectangle_area.shrink_x1_y1_x2_y2(-5)))), 0)):
            return True


def get_device(index) -> COCDevice:
    client = AdbClient(host="127.0.0.1", port=5037)
    print(client.devices())
    print(client.version())
    return client.devices()[0]


# cd C:\Users\JiangKan\ng-on-meeting
# npm run packagr
# cd ./dist
# npm pack
# cd C:\Users\JiangKan\Downloads\OTBMeetingsManagement.UI
# npm install C:\Users\JiangKan\ng-on-meeting\dist\ng-on-meeting-0.0.83.tgz --force

