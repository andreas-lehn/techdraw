'''Generate a spirograph

This tool generates an SVG file with a spirograph.
The parameters of the spirograph are determined by the command line parameters.

Use:
    python -m spirograph.gen --help

for details about the parameters.
'''

import argparse
import techdraw as svg
import sys
from . import Spirograph

if __name__ == "__main__":
    PROG = 'python3 -m spirograph.gen'
    DESCRIPTION = 'Generate spirographs SVG files.'
    parser = argparse.ArgumentParser(prog=PROG, description=DESCRIPTION)
    #parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('filename', type=str, help='name of output SVG file', nargs='?', default=sys.stdout)
    parser.add_argument('-r', '--ring', type=int, help='number of teeth of the ring', default=105)
    parser.add_argument('-w', '--wheel', type=int, help='number of teeth of the wheel', default=50)
    parser.add_argument('-e', '--excenter', type=float, help='excenter value of the pen', default=0.8)
    parser.add_argument('-o', '--offset', type=int, help='offset of the wheel at its start position', default=0)
    parser.add_argument('-s', '--samples', type=int, help='samples per tooth step', default=1)
    args = parser.parse_args()

    args.ring = abs(args.ring)
    args.excenter = abs(args.excenter)

    if args.ring <= args.wheel:
        print(f'{PROG}: Wheel must be smaller than ring! No spriograph generated.', file=sys.stderr)
        sys.exit(-1)

    if args.wheel == 0:
        print(f'{PROG}: Wheel must not be zero! No spriograph generated.', file=sys.stderr)
        sys.exit(-1)

    if args.excenter > 0.9:
        args.excenter = 0.9
        print(f'{PROG}: Excenter limited to {args.excenter}', file=sys.stderr)
    
    if args.samples < 1:
        print(f'{PROG}: Number of samples must be > 0 but is {args.samples}. Value set to 1.', file=sys.stderr)
        args.samples = 1

    spirograph = Spirograph(args.ring, args.wheel, args.excenter, args.offset, args.samples)

    M = (0, 0)
    c = int(spirograph.r_max() + 2)
    w = c * 2
    img = svg.Image((w, w), (c, c))
    img.desc.text = f'Spirograph: ring = {args.ring}, wheel = {args.wheel}, excenter = {args.excenter}, offset = {args.offset}, samples = {args.samples}'
    svg.Path(img.content, spirograph.svg_path(), { 'stroke-width': '0.5', 'stroke': 'black', 'fill': 'none'})
    img.write(args.filename)
