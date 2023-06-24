#!/usr/env python3

import math
import argparse
import svghelper as svg
import sys

def ggt(a: int, b: int) -> int:
    if b == 0: return 1
    if a > b:  return ggt(a - b, b)
    if a < b:  return ggt(a, b - a)
    return a

def kgv(a: int, b: int) -> int:
    return int(a * b / ggt(a, b))

class Spirograph:
    '''draws spirographs'''

    def __init__(self, ring: int, wheel: int, excenter=0.8, offset=0, samples=1):
        self.ring = ring
        self.wheel = wheel
        self.excenter = excenter
        self.offset = offset * 2 * math.pi / self.wheel
        self.modul = 1
        self.samples = samples

    def r_ring(self):
        return self.modul * self.ring / 2

    def r_wheel(self):
        return self.modul * self.wheel / 2

    def r_excenter(self):
        return self.excenter * self.r_wheel()

    def r_max(self):
        result = self.r_ring()
        if self.wheel < 0:
            result -= 2 * self.r_wheel()
        return result
    
    def revolutions(self):
        return int(self.step_count() / self.ring)
    
    def step_size(self):
        return 2 * math.pi / self.ring / self.samples
    
    def step_count(self):
        if self.wheel == 0: return self.ring
        return kgv(abs(self.wheel), abs(self.ring))

    def tooth_pos(self, alpha):
        '''return x, y of a tooth'''
        r = self.r_ring()
        return r * math.sin(alpha), r * math.cos(alpha)

    def center_pos(self, alpha):
        '''returns the position of the wheels center'''
        x, y = self.tooth_pos(alpha)
        r = self.r_wheel()
        return x - r * math.sin(alpha), y - r * math.cos(alpha)

    def excenter_pos(self, alpha):
        cx, cy = self.center_pos(alpha)
        r = self.r_excenter()
        beta = alpha - alpha / self.wheel * self.ring + self.offset
        return cx + r * math.sin(beta), cy + r * math.cos(beta)

    def pen_pos(self, alpha):
        return self.excenter_pos(alpha)

    def points(self):
        result = []
        alpha, beta, delta = 0, self.revolutions() * 2 * math.pi, self.step_size()
        while alpha < beta:
            result.append(self.pen_pos(alpha))
            alpha += delta
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
    parser.add_argument('-s', '--samples', type=int, help='samples per teeth step.', default=1)
    args = parser.parse_args()

    args.ring = abs(args.ring)
    args.excenter = abs(args.excenter)

    if args.ring <= args.wheel:
        print(f'{sys.argv[0]}: Wheel must be smaller than ring! No spriograph generated.', file=sys.stderr)
        sys.exit(-1)

    if args.wheel == 0:
        print(f'{sys.argv[0]}: Wheel must not be zero! No spriograph generated.', file=sys.stderr)
        sys.exit(-1)

    if args.excenter > 0.9:
        args.excenter = 0.9
        print(f'{sys.argv[0]}: Excenter limited to {args.excenter}', file=sys.stderr)
    
    if args.samples < 1:
        print(f'{sys.argv[0]}: Number of samples must be > 0 but is {args.samples}. Value set to 1.', file=sys.stderr)
        args.samples = 1

    spirograph = Spirograph(args.ring, args.wheel, args.excenter, args.offset, args.samples)

    M = (0, 0)
    c = int(spirograph.r_max() + 2)
    w = c * 2
    img = svg.Image((w, w), (c, c))
    img.desc.text = f'Spirograph: ring = {args.ring}, wheel = {args.wheel}, excenter = {args.excenter}, offset = {args.offset}, samples = {args.samples}'
    svg.Path(img.content, spirograph.svg_path(), { 'stroke-width': '0.5', 'stroke': 'black', 'fill': 'none'})
    svg.Circle(img.content, M, spirograph.r_ring(), svg.dot_stroke, fill='none')
    svg.Circle(img.content, M, spirograph.r_ring() - spirograph.r_wheel(), svg.sym_stroke, fill='none')
    img.write(args.filename)
