'''Compiles spirograph file to SVG file

A spirograph file is a JSON file that describes one or more spirographs.
All spirographs in the file are drawn in one SVG file.
That means that the generated SVG file may contain more than one spirographs.

Each spirograph is described as a JSON object with its parameters:

+----------+-------+--------------------------------------------------------+
| Name     | Type  | Description                                            |
+----------+-------+--------------------------------------------------------+
| ring     | int   | number of teeth of the ring                            |
+----------+-------+--------------------------------------------------------+
| wheel    | int   | number of teeth of the wheel                           |
+----------+-------+--------------------------------------------------------+
| excenter | float | measure of how much the pen is outside wheeks center   |
+----------+-------|--------------------------------------------------------+
| offset   | int   | rotation of the wheel at start position                |
+----------+-------+--------------------------------------------------------+
| samples  | int   | number of points calculated for each teeth of the ring |
+----------+-------+--------------------------------------------------------+

By default the wheel runs inside the ring.
If the teeth count or the wheel is negative it will run outside of the ring.

At least ``ring`` and ``wheel`` must be specified.

Example for a spirograph:

    {"ring": 104, "wheel": 52, "excenter": 0.6, "offset": 12, "samples": 2}

If the file contains more than one spirograph,
these spirographs must be defined inside a JSON array.

Example for multiple spirographs in one file:

    [{"ring": 104, "wheel": 52}, {"ring": 104, "wheel": 48}]

Each spirograph object may contain attributes.
These attributes are treated as SVG attributes of a path element.
With these attributes the appearance of the spirograph may be controlled.

Example for a spriograph object with additional SVG attributes:

    {"ring": 104, "wheel": 52, "fill": "blue", "stroke": "red", "stroke-width": "0.2"}

The spirograph compiler accepts a file name for the input file.
If no file name is provided, it will read from ``sys.stdin``.

It generates a file named after the input file
but replaces the extension ``.spiro`` by ``.svg``.
If no input file is specified it will write to ``sys.stdout``
'''

import os
import sys
import json
import argparse
import techdraw as svg
from . import Spirograph

def get_value(data: dict, key: str, default=None):
    '''Reads a value from dict'''
    if key in data.keys():
        result = data[key]
        del data[key]
    else:
        if default is None:
            raise KeyError(f'Missing key: {key}')
        result = default
    return result

def parse_hook(data: dict):
    '''Transforms a JSON object to a Spirograph object'''
    ring = get_value(data, 'ring')
    wheel = get_value(data, 'wheel')
    excenter = get_value(data, 'excenter', 0.8)
    offset = get_value(data, 'offset', 0)
    samples = get_value(data, 'samples', 1)
    return Spirograph(ring, wheel, excenter, offset, samples), data

if __name__ == "__main__":
    PROG = 'spirograph.compile'
    DESCRIPTION = 'Command line tool to generate SVG files form spirograph files.'
    parser = argparse.ArgumentParser(prog=PROG, description=DESCRIPTION)
    parser.add_argument('filename', nargs='?', type=str, help='name of input file', default=sys.stdin)
    args = parser.parse_args()

    try:
        if args.filename is sys.stdin:
            outfile = sys.stdout
            data = json.load(sys.stdin, object_hook=parse_hook)
            args.filename = 'stdin'
        else:
            with open(args.filename) as f:
                data = json.load(f, object_hook=parse_hook)
            base, ext = os.path.splitext(args.filename)
            outfile = base + '.svg' if ext == '.spiro' else args.filename + '.svg'
    except Exception as error:
        print(PROG + ':', error, file=sys.stderr)
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
