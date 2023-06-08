#!/usr/env python3

import argparse
import math
from gearwheel import GearWheel
import svghelper as svg

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates an SVG image with a gear wheel.')
    parser.add_argument('filename', type=str, help='file name')
    parser.add_argument('-m', '--modul', type=float, help='modul in mm', default=2.0)
    parser.add_argument('-t', '--teeth', type=int, help='number of teeth', default=30)
    parser.add_argument('-a', '--alpha', type=float, help='Eingriffswinkel', default=20.0)
    args = parser.parse_args()

    gear_wheel = GearWheel(args.modul, args.teeth, args.alpha * math.pi / 180)

    M = (0, 0)
    c = int(gear_wheel.r_head() + 1)
    w = c * 2
    img = svg.Image((w, w), (c, c))
    svg.Path(img.content, gear_wheel.svg_path())
    svg.Circle(img.content, M, gear_wheel.r_head(), svg.dash_stroke, fill='none')
    svg.Circle(img.content, M, gear_wheel.r_0(), svg.sym_stroke, fill='none')
    svg.Circle(img.content, M, gear_wheel.r_base(), svg.dot_stroke, fill='none')
    svg.Circle(img.content, M, gear_wheel.r_foot(), svg.dash_stroke, fill='none')
    img.write(args.filename)
