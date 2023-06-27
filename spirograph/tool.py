#!/usr/env python3

import argparse
import svghelper as svg
import json
from spirograph import Spirograph
import sys
import os

def get_value(data: dict, key: str, default=None):
    if key in data.keys():
        result = data[key]
        del data[key]
    else:
        if default == None:
            raise KeyError(f'Missing key: {key}')
        result = default
    return result

def parse_hook(data: dict):
    ring = get_value(data, 'ring')
    wheel = get_value(data, 'wheel')
    excenter = get_value(data, 'excenter', 0.8)
    offset = get_value(data, 'offset', 0)
    samples = get_value(data, 'samples', 1)
    return Spirograph(ring, wheel, excenter, offset, samples), data

if __name__ == "__main__":
    prog = 'spirograph.tool'
    description = 'A simple command line tool to generate spirograph SVG files form .spiro files.'
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument('filename', type=str, help='file name')
    args = parser.parse_args()
    base, ext = os.path.splitext(args.filename)
    outfile = base + '.svg' if ext == '.spiro' else args.filename + '.svg'

    try:
        with open(args.filename) as f:
            data = json.load(f, object_hook=parse_hook)
    except Exception as error:
        print(prog + ':', error, file=sys.stderr)
        sys.exit(-1)
    
    r_max = 0
    for spirograph, _ in data:
        if spirograph.r_max() > r_max:
            r_max = spirograph.r_max()

    r_max = int(r_max + 2)
    width = 2 * r_max
    img = svg.Image((width, width), (r_max, r_max))
    img.desc.text = f'Spirograph from file: {args.filename}'
    for spirograph, attrib in data:
        svg.Path(img.content, spirograph.svg_path(), { 'stroke-width': '0.5', 'stroke': 'black', 'fill': 'none', **attrib })
    
    img.write(outfile)
