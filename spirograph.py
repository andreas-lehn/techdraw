#!/usr/env python3

import math
import argparse
import svghelper as svg

def ggt(a: int, b: int) -> int:
    if b == 0: return 1
    if a > b:  return ggt(a - b, b)
    if a < b:  return ggt(a, b - a)
    return a

def kgv(a: int, b: int) -> int:
    return int(a * b / ggt(a, b))

class Spirograph:
    '''draws spirographs'''

    def __init__(self, n_stator: int, n_rotator: int, excenter=0.8, offset=0):
        self.n_stator = n_stator
        self.n_rotator = n_rotator
        self.excenter = excenter
        self.offset = offset
        self.modul = 1

    def r_stator(self):
        return self.modul * self.n_stator / 2

    def r_rotator(self):
        return self.modul * self.n_rotator / 2

    def r_excenter(self):
        return self.excenter * self.r_rotator()

    def r_max(self):
        return self.r_stator() + 2 * self.r_rotator()

    def step_count(self):
        if self.n_rotator == 0: return self.n_stator
        return kgv(abs(self.n_rotator), abs(self.n_stator))

    def tooth_angle(self, n):
        if self.n_stator == 0: return 0
        return n / self.n_stator * 2 * math.pi

    def tooth_pose(self, n):
        '''return x, y, alpha of a tooth'''
        r, alpha = self.r_stator(), self.tooth_angle(n)
        return r * math.sin(alpha), r * math.cos(alpha), alpha

    def center_pose(self, n):
        '''returns the position of rotators center'''
        x, y, alpha = self.tooth_pose(n)
        r = self.r_rotator()
        return x + r * math.sin(alpha), y + r * math.cos(alpha), alpha

    def excenter_pos(self, n, m):
        cx, cy, alpha = self.center_pose(n)
        r = self.r_excenter()
        beta = alpha + m / self.n_rotator * 2 * math.pi
        return cx + r * math.sin(beta), cy + r * math.cos(beta)

    def pen_pos(self, step: int):
        return self.excenter_pos(step, step + self.offset)

    def points(self):
        result = []
        for i in range(self.step_count()):
            result.append(self.pen_pos(i))
        return result

    def svg_path(self):
        points = self.points()
        return svg.PathCreator(points[0]).line_to(*points[1:]).close().path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates an SVG image with a gear wheel.')
    parser.add_argument('filename', type=str, help='file name')
    parser.add_argument('-s', '--stator', type=int, help='number of teeth of the stator', default=20)
    parser.add_argument('-r', '--rotator', type=int, help='number of teeth of the rotator', default=12)
    parser.add_argument('-e', '--excenter', type=float, help='excenter', default=0.8)
    parser.add_argument('-o', '--offset', type=int, help='offset of rotator', default=0)
    args = parser.parse_args()

    spirograph = Spirograph(args.stator, args.rotator, args.excenter, args.offset)

    M = (0, 0)
    c = int(spirograph.r_max() + 2)
    w = c * 2
    img = svg.Image((w, w), (c, c))
    img.desc.text = f'Spirograph: stator teeth = {spirograph.n_stator}, rotator teeth = {spirograph.n_rotator}, excenter = {spirograph.excenter}, offset = {spirograph.offset}'
    svg.Path(img.content, spirograph.svg_path(), { 'stroke-width': '0.5', 'stroke': 'black', 'fill': 'none'})
    svg.Circle(img.content, M, spirograph.r_stator(), svg.sym_stroke, fill='none')
    img.write(args.filename)
