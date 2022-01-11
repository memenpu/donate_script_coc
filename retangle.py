
from random import Random
random = Random()


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def x2(self):
        return self.x+self.width

    @property
    def y2(self):
        return self.y+self.height

    @property
    def x_y_w_h(self):
        return self.x, self.y, self.width, self.height

    def shrink_x_y_w_h(self, number=5):
        return self.x+number, self.y+number, self.width-number, self.height-number

    def x1_y1_x2_y2(self, plus_x=0):
        return self.x+plus_x, self.y, self.x + self.width+plus_x, self.y + self.height

    @property
    def x1_y1_center(self):
        return (self.x + self.width+self.x)/2, (self.y + self.height+self.y)/2

    def shrink_x1_y1_x2_y2(self, number=5):
        return self.x+number, self.y+number, self.x + self.width-number, self.y + self.height-number

    def random_point(self, shrink_pixel=5):
        """

        :rtype: x, y
        """
        return random.randrange(self.x + shrink_pixel, self.x2 - shrink_pixel, 2), random.randrange(self.y + shrink_pixel, self.y2 - shrink_pixel, 2)

    def __str__(self):
        return f"{self.x}, {self.y}"
