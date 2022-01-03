from typing import List, Tuple

from pygame import image, surfarray, Surface, draw
import os
import glob
import json
class PacmanMap:
    START_COLOUR = 255
    END_COLOUR = 255 << 16
    FOOD_COLOUR = 255 << 8
    POWER_COLOUR = 255 << 16 | 255 << 8 | 255
    DRAW_SCALE = 8
    def __init__(self, other_map = None):
        self.start = other_map.start if other_map else None
        self.end = other_map.end if other_map else None
        self.food = set(other_map.food) if other_map else set()
        self.power_pellets = set(other_map.power_pellets) if other_map else set()
        self.width = other_map.width if other_map else None
        self.height = other_map.height if other_map else None
        self.digits = other_map.digits if other_map else [None for i in range(10)]
        self.digit_positions = other_map.digit_positions if other_map else [(0, 0) for i in range(4)]


    def load(self, map_file):
        map_image = surfarray.pixels2d(image.load(os.path.join(map_file, 'pacman_numbers.png'))) & 0xFFFFFF
        self.width = map_image.shape[0]
        self.height = map_image.shape[1]
        for x, column in enumerate(map_image):
            for y, value in enumerate(column):
                if value == self.START_COLOUR:
                    self.start = (x, y)
                elif value == self.END_COLOUR:
                    self.end = (x, y)
                elif value == self.FOOD_COLOUR:
                    self.food.add((x, y))
                elif value == self.POWER_COLOUR:
                    self.power_pellets.add((x, y))

        digit_paths = glob.glob(os.path.join(map_file, 'digits', '*.png'))
        for digit_path in digit_paths:
            digit_number = int(os.path.basename(digit_path).split('.')[0])
            new_digit = PacmanClockDigit()
            new_digit.load(digit_path, digit_number)
            self.digits[digit_number] = new_digit

        with open(os.path.join(map_file, 'digit_positions.json'), 'r') as f:
            digit_positions = json.load(f)
            self.digit_positions = [(position['x'], position['y']) for position in digit_positions]

    def get_render_dimensions(self) -> (int, int):
        return (self.width + 2)*self.DRAW_SCALE, (self.height+2)*self.DRAW_SCALE

    def draw(self, current_time_digits: Tuple[int]) -> Surface:
        out_surface = Surface(self.get_render_dimensions())
        out_surface.fill((0, 0, 0))
        food_pellets = self.food.union(self.power_pellets)
        for x, y in food_pellets:
            if (x, y) in self.food:
                draw.circle(out_surface, (255, 255, 255), (x*self.DRAW_SCALE+self.DRAW_SCALE//2, y*self.DRAW_SCALE + self.DRAW_SCALE+self.DRAW_SCALE//2), 1)
            else:
                draw.circle(out_surface, (255, 255, 255),
                            (x * self.DRAW_SCALE + self.DRAW_SCALE // 2, y * self.DRAW_SCALE+ self.DRAW_SCALE + self.DRAW_SCALE // 2), 4)

            if (x, y-1) not in food_pellets:
                if (x-1, y-1) not in food_pellets:
                    draw.line(out_surface, (0, 0, 255), (x*self.DRAW_SCALE+self.DRAW_SCALE//2, y*self.DRAW_SCALE + self.DRAW_SCALE-self.DRAW_SCALE//2), (x*self.DRAW_SCALE-self.DRAW_SCALE//2, y*self.DRAW_SCALE + self.DRAW_SCALE-self.DRAW_SCALE//2), 1)
                if (x+1, y-1) not in food_pellets:
                    draw.line(out_surface, (0, 0, 255), (x*self.DRAW_SCALE+self.DRAW_SCALE//2, y*self.DRAW_SCALE + self.DRAW_SCALE-self.DRAW_SCALE//2), (x*self.DRAW_SCALE+self.DRAW_SCALE+ self.DRAW_SCALE//2, y*self.DRAW_SCALE + self.DRAW_SCALE-self.DRAW_SCALE//2), 1)
            if (x, y+1) not in food_pellets:
                if (x-1, y+1) not in food_pellets:
                    draw.line(out_surface, (0, 0, 255), (x*self.DRAW_SCALE+self.DRAW_SCALE//2, y*self.DRAW_SCALE + self.DRAW_SCALE+self.DRAW_SCALE+2), (x*self.DRAW_SCALE-self.DRAW_SCALE//2, y*self.DRAW_SCALE + self.DRAW_SCALE+self.DRAW_SCALE+2), 1)
                if (x+1, y+1) not in food_pellets:
                    draw.line(out_surface, (0, 0, 255), (x*self.DRAW_SCALE+self.DRAW_SCALE//2, y*self.DRAW_SCALE + self.DRAW_SCALE+self.DRAW_SCALE+2), (x*self.DRAW_SCALE+self.DRAW_SCALE+ self.DRAW_SCALE//2, y*self.DRAW_SCALE + self.DRAW_SCALE+self.DRAW_SCALE+2), 1)

            if (x+1, y) not in food_pellets:
                if (x+1, y-1) not in food_pellets:
                    draw.line(out_surface, (0, 0, 255), (x*self.DRAW_SCALE+ self.DRAW_SCALE+ self.DRAW_SCALE//2, y*self.DRAW_SCALE +self.DRAW_SCALE +self.DRAW_SCALE//2), (x*self.DRAW_SCALE+ self.DRAW_SCALE+ self.DRAW_SCALE//2, y*self.DRAW_SCALE+ self.DRAW_SCALE -self.DRAW_SCALE//2), 1)
                if (x+1, y+1) not in food_pellets:
                    draw.line(out_surface, (0, 0, 255), (x*self.DRAW_SCALE+ self.DRAW_SCALE+ self.DRAW_SCALE//2, y*self.DRAW_SCALE +self.DRAW_SCALE +self.DRAW_SCALE//2), (x*self.DRAW_SCALE+ self.DRAW_SCALE+ self.DRAW_SCALE//2, y*self.DRAW_SCALE+ self.DRAW_SCALE +self.DRAW_SCALE), 1)
            if (x - 1, y) not in food_pellets:
                if (x - 1, y - 1) not in food_pellets:
                    draw.line(out_surface, (0, 0, 255), (x * self.DRAW_SCALE - self.DRAW_SCALE + self.DRAW_SCALE//2,
                                                         y * self.DRAW_SCALE + self.DRAW_SCALE + self.DRAW_SCALE // 2),
                              (x * self.DRAW_SCALE - self.DRAW_SCALE + self.DRAW_SCALE//2,
                               y * self.DRAW_SCALE + self.DRAW_SCALE - self.DRAW_SCALE // 2), 1)
                if (x - 1, y + 1) not in food_pellets:
                    draw.line(out_surface, (0, 0, 255), (x * self.DRAW_SCALE - self.DRAW_SCALE + self.DRAW_SCALE//2,
                                                         y * self.DRAW_SCALE + self.DRAW_SCALE + self.DRAW_SCALE // 2),
                              (x * self.DRAW_SCALE - self.DRAW_SCALE + self.DRAW_SCALE//2,
                               y * self.DRAW_SCALE + self.DRAW_SCALE + self.DRAW_SCALE), 1)

        #draw.circle(out_surface, (255, 0, 0), (self.start[0] * self.DRAW_SCALE+self.DRAW_SCALE//2, self.start[1] * self.DRAW_SCALE+self.DRAW_SCALE//2), 2)
        #draw.circle(out_surface, (0, 0, 255), (self.end[0] * self.DRAW_SCALE+self.DRAW_SCALE//2, self.end[1] * self.DRAW_SCALE+self.DRAW_SCALE//2), 2)

        # for position, digit in zip(self.digit_positions, current_time_digits):
        #     draw_positions = self.digits[digit]
        #     for draw_position in draw_positions.positions:
        #         draw.circle(out_surface, (255, 0, 0), (position[0]*self.DRAW_SCALE+self.DRAW_SCALE//2+draw_position[0]*self.DRAW_SCALE, position[1]*self.DRAW_SCALE+self.DRAW_SCALE+self.DRAW_SCALE//2+draw_position[1]*self.DRAW_SCALE), 2)
        return out_surface

    def __str__(self) -> str:
        return f"Start: {self.start}\nEnd: {self.end}\nFood: {self.food}\nPower Pellets: {self.power_pellets}"

class PacmanClockDigit:
    def __init__(self, digit=None):
        self.positions = set()
        self.digit = None

    def load(self, clock_digit_path, digit):
        clock_digit = surfarray.pixels2d(image.load(clock_digit_path)) & 0xFFFFFF
        self.digit = digit
        for x, column in enumerate(clock_digit):
            for y, value in enumerate(column):
                if value == 0xFFFFFF:
                    self.positions.add((x, y))
