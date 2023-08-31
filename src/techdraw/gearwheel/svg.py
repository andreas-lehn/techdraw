#!/usr/env python3

import argparse
from . import GearWheel
import techdraw as svg

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='python -m techdraw.gearwheel.svg', description='Generates an SVG image with a gear wheel.')
    parser.add_argument('filename', type=str, help='file name')
    parser.add_argument('-m', '--modul', type=float, help='modul in mm', default=2.0)
    parser.add_argument('-t', '--teeth', type=int, help='number of teeth', default=30)
    parser.add_argument('-p', '--pitch', type=float, help='pitch angle', default=20.0)
    args = parser.parse_args()

    gear_wheel = GearWheel(args.modul, args.teeth, svg.radians(args.pitch))

    M = (0, 0)
    c = int(gear_wheel.r_head() + 1)
    w = c * 2
    img = svg.Image((w, w), (c, c))
    img.desc.text = f'Gear wheel: modul = {gear_wheel.modul}, teeth = {gear_wheel.n_teeth}, alpha = {svg.degrees(gear_wheel.alpha)}, d = {svg.fmt_f(2 * gear_wheel.r_0())}'
    svg.Path(img.content, gear_wheel.svg_path())
    svg.Circle(img.content, M, gear_wheel.r_head(), svg.DASH_STROKE, fill='none')
    svg.Circle(img.content, M, gear_wheel.r_0(), svg.SYM_STROKE, fill='none')
    svg.Circle(img.content, M, gear_wheel.r_base(), svg.DOT_STROKE, fill='none')
    svg.Circle(img.content, M, gear_wheel.r_foot(), svg.DASH_STROKE, fill='none')
    img.write(args.filename)
