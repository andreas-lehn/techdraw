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
        self.ring = int(ring)
        if self.ring < 1:
            raise ValueError('ring must be > 0')

        self.wheel = int(wheel)
        if self.wheel == 0:
            raise ValueError('wheel must not be zero')

        self.excenter = excenter
        if self.excenter < 0.0 or excenter > 1.0:
            raise ValueError('excenter value out of range (0.0 .. 1.0)')

        self.offset = int(offset) * 2 * math.pi / self.wheel

        self.samples = int(samples)
        if samples < 1:
            raise ValueError('samples must be > 0')

        self.modul = 1

    def r_ring(self):
        return self.modul * self.ring / 2

    def r_wheel(self):
        return self.modul * self.wheel / 2

    def r_excenter(self):
        return self.excenter * self.r_wheel()

    def r_max(self):
        result = self.r_ring() - (1.0 - self.excenter) * self.r_wheel()
        if self.wheel < 0:
            result -= (1.0 + self.excenter) * self.r_wheel()
        return result
    
    def revolutions(self):
        return int(self.step_count() / self.ring / self.samples)
    
    def step_size(self):
        return 2 * math.pi / self.ring / self.samples
    
    def step_count(self):
        return kgv(abs(self.wheel), abs(self.ring)) * self.samples

    def tooth_pos(self, alpha):
        '''return x, y of a tooth'''
        r = self.r_ring()
        return r * math.sin(alpha), r * math.cos(alpha)

    def center_pos(self, alpha):
        '''returns the position of the wheels center'''
        x, y = self.tooth_pos(alpha)
        r = self.r_wheel()
        return x - r * math.sin(alpha), y - r * math.cos(alpha)

    def pen_pos(self, alpha):
        cx, cy = self.center_pos(alpha)
        r = self.r_excenter()
        beta = alpha - alpha / self.wheel * self.ring + self.offset
        return cx + r * math.sin(beta), cy + r * math.cos(beta)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(len(self)))]
        elif isinstance(key, int):
            if key < 0: # Handle negative indices
                key += len(self)
            if key < 0 or key >= len(self):
                raise IndexError(f'Spirograph index {key} is out of range.')
            return self.pen_pos(key * self.step_size())
        else:
            raise TypeError(f'Spirograph indices must be integers or slices, not {type(key)}')
    
    def __len__(self):
        return self.step_count()
    
    def points(self):
        return self[:]

    def svg_path(self):
        return svg.PathCreator(self[0]).line_to(*self[1:]).close().path

    class Iterator:
        def __init__(self, spiro):
            self.index = -1
            self.spiro = spiro
    
        def __next__(self):
            self.index += 1
            if self.index == len(self.spiro):
                raise StopIteration()
            return self.spiro[self.index]

    def __iter__(self):
        return self.Iterator(self)

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
