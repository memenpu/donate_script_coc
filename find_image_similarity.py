import cv2
import numpy as np
from typing import List
from retangle import Rectangle
import datetime
from  PIL import Image


def find_similar_images(img, template, filter_function=None, exist_image=None) -> List[Rectangle]:
    gray_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    if exist_image is not None:
        template1 = exist_image
        result1 = cv2.matchTemplate(gray_img, template1, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result1 >= .8)
        if not len(loc):
            return []
    w, h = template.shape[::-1]
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >=0.8)
    found_templates = []
    # filter same spots
    filtered_loc = set()
    for a, b in zip(*loc[::-1]):
        if any([a - 15 <= c < a + 15 and b - 15 <= d < b + 15 for c, d in filtered_loc]):
            continue
        filtered_loc.add((a, b))
    for pt in filtered_loc:
        cv2.rectangle(gray_img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
        if filter_function and filter_function(*pt):
            found_templates.append(Rectangle(*pt, w, h))
            continue
        found_templates.append(Rectangle(*pt, w, h))
    return found_templates


def test_find_similar_images(image_path, detect_image_path="rage_donate.png", show=False):
    img =  cv2.cvtColor(np.array(Image.open(image_path)), cv2.COLOR_RGB2GRAY)
    # img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(detect_image_path, 0)
    w, h = template.shape[::-1]
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.75)
    found_templates = []
    # filter same spots
    filtered_loc = set()
    for a, b in zip(*loc[::-1]):
        if any([a - 15 <= c < a +  15 and b -  15 <= d < b +  15 for c, d in filtered_loc]):
            continue
        filtered_loc.add((a, b))
    for pt in filtered_loc:
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
        found_templates.append((*pt, w, h))
    print(found_templates)

    if show:
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return found_templates


if __name__ == '__main__':
    # test_find_similar_images(r"screen.png", r"buttons/close_chat.png",show=True)
    # test_find_similar_images(r"full.png", r"donate/lightning_spell.png",show=True)
    # test_find_similar_images(r"full.png", r"donate/hog_rider.png",show=True)
    # test_find_similar_images(r"siege_machines.png", r"donate/lightning_spell.png", show=True)
    # test_find_similar_images(r"full.png", r"buttons/not_enough_space.png", show=True)
    # test_find_similar_images(r"screenshot.png", r"donate/balloon.png", show=True)
    # test_find_similar_images(r"screenshot.png", r"buttons/donate_button.png", show=True)
    # test_find_similar_images(r"temp.png", r"buttons/donate_button.png", show=True)
    test_find_similar_images(r"why.png", r"buttons/open_chat.png", show=True)
    # test_find_similar_images(r"unread.png", r"buttons/unread_down.png", show=True)
    # test_find_similar_images(r"train_troops.png", r"barbarian.png", show=False)
    # test_find_similar_images(r"train_troops.png", r"archer.png", show=False)
    # test_find_similar_images(r"train_troops.png", r"giant.png", show=True)
