import collections
import datetime
import sys
import time

import constants as c
from coc_device import get_device, Grayscale, COCDevice
from retangle import Rectangle


def donate(stop_at):
    """
    donate troops and return troops that are donated
    """
    index = sys.argv[1] if len(sys.argv) > 1 else 0
    device = get_device(index)
    device.__class__ = COCDevice
    donated_troops = collections.Counter()
    # while datetime.datetime.now() < stop_at:
    while True:
        if device.find_control(c.OPEN_CHAT_IMG):
            donated_troops = collections.Counter()
            if donate_buttons := device.find_control(c.DONATE_IMG, tap_on_it=False, filter_function=chat_area):
                print('donate_buttons: ', len(donate_buttons))
                donate_troops_in_screen(device, donate_buttons, donated_troops)
        device.find_control(c.CLOSE_BUTTON)
        device.find_control(c.ClOSE_CHAT_IMG)
        # donated_troops = collections.Counter({x:y for x,y in donated_troops.items() if y>0})
        print("; ".join([f"{x.name}: {y}" for x, y in donated_troops.items()]))
        device.train_donated_troops(donated_troops)
        c.foreach({k: v for k, v in donated_troops.items() if v}, lambda x: print_donated_troop_number(*x))
        device.tap_to_cancel()
        time.sleep(.2)
        device.tap_to_cancel()


def chat_area(x, y):
    return x < 600


def donate_troops_in_screen(device, donate_buttons, donated_troops):
    donate_buttons.sort(key=lambda x: -x.y)

    for index, donate_button in enumerate(donate_buttons):
        device.tap_on_rectangle(donate_button)
        take_new_screenshot = True
        for troop in (
                c.valkyrie, c.hog_rider, c.balloon, c.super_dragon,
                c.electro_dragon, c.super_wizard, c.barbarian, c.wall_breaker, c.yeti,
                c.rage_spell, c.freeze_spell, c.lightning_spell, c.invisibility_spell, c.poision_spell,
                c.log_launcher, c.stone_slammer, c.battle_blimp
        ):
            if not (device.find_control(c.CLOSE_BUTTON, tap_on_it=False)):
                break
            state = device.donate_troop(troop, take_new_screenshot=take_new_screenshot)
            donate_state_actions(state, donated_troops, take_new_screenshot)

        if index + 1 < len(donate_buttons):
            if not device.control_exist_at(c.DONATE_IMG, donate_buttons[index + 1]):
                print("donate button isn't there now")
                break


def print_donated_troop_number(x, y):
    if y > 0:
        print(f"{x.name}: {y}; ", end="")


def donate_state_actions(state, donated_troops, take_new_screenshot):
    if state is Grayscale:
        take_new_screenshot = False
    donated_troops[state.troop] += state.number_of_donate


if __name__ == '__main__':
    stop_at = datetime.datetime.now() + datetime.timedelta(hours=14, )
    donate(stop_at)
