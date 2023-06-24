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

    def __init__(self, ring: int, wheel: int, excenter=0.8, offset=0):
        self.ring = ring
        self.wheeel = wheel
        self.excenter = excenter
        self.offset = offset
        self.modul = 1

    def r_ring(self):
        return self.modul * self.ring / 2

    def r_wheel(self):
        return self.modul * self.wheeel / 2

    def r_excenter(self):
        return self.excenter * self.r_wheel()

    def step_count(self):
        if self.wheeel == 0: return self.ring
        return kgv(abs(self.wheeel), abs(self.ring))

    def tooth_angle(self, n):
        if self.ring == 0: return 0
        return n / self.ring * 2 * math.pi

    def tooth_pose(self, n):
        '''return x, y, alpha of a tooth'''
        r, alpha = self.r_ring(), self.tooth_angle(n)
        return r * math.sin(alpha), r * math.cos(alpha), alpha

    def center_pose(self, n):
        '''returns the position of the wheels center'''
        x, y, alpha = self.tooth_pose(n)
        r = self.r_wheel()
        return x - r * math.sin(alpha), y - r * math.cos(alpha), alpha

    def excenter_pos(self, n, m):
        cx, cy, alpha = self.center_pose(n)
        r = self.r_excenter()
        beta = alpha - m / self.wheeel * 2 * math.pi
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
    parser = argparse.ArgumentParser(description='Generates an SVG image with a spirograph.')
    parser.add_argument('filename', type=str, help='file name')
    parser.add_argument('-r', '--ring', type=int, help='number of teeth of the ring', default=150)
    parser.add_argument('-w', '--wheel', type=int, help='number of teeth of the wheel', default=52)
    parser.add_argument('-e', '--excenter', type=float, help='excenter', default=0.8)
    parser.add_argument('-o', '--offset', type=int, help='offset of rotator', default=0)
    args = parser.parse_args()

    spirograph = Spirograph(args.ring, args.wheel, args.excenter, args.offset)

    M = (0, 0)
    c = int(spirograph.r_ring() + 2)
    w = c * 2
    img = svg.Image((w, w), (c, c))
    img.desc.text = f'Spirograph: ring = {spirograph.ring}, wheel = {spirograph.wheeel}, excenter = {spirograph.excenter}, offset = {spirograph.offset}'
    svg.Path(img.content, spirograph.svg_path(), { 'stroke-width': '0.5', 'stroke': 'black', 'fill': 'none'})
    svg.Circle(img.content, M, spirograph.r_ring(), svg.dot_stroke, fill='none')
    svg.Circle(img.content, M, spirograph.r_ring() - spirograph.r_wheel(), svg.sym_stroke, fill='none')
    img.write(args.filename)
