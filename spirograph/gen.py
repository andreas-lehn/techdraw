
import argparse
import svghelper as svg
import sys
from spirograph import Spirograph

if __name__ == "__main__":
    prog = 'spirograph.gen'
    description = 'Command line tool to generate spirographs as SVG files'
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument('filename', type=str, help='name of output SVG file')
    parser.add_argument('-r', '--ring', type=int, help='number of teeth of the ring', default=105)
    parser.add_argument('-w', '--wheel', type=int, help='number of teeth of the wheel', default=50)
    parser.add_argument('-e', '--excenter', type=float, help='excenter', default=0.8)
    parser.add_argument('-o', '--offset', type=int, help='offset of rotator', default=0)
    parser.add_argument('-s', '--samples', type=int, help='samples per teeth step.', default=1)
    args = parser.parse_args()

    args.ring = abs(args.ring)
    args.excenter = abs(args.excenter)

    if args.ring <= args.wheel:
        print(f'{prog}: Wheel must be smaller than ring! No spriograph generated.', file=sys.stderr)
        sys.exit(-1)

    if args.wheel == 0:
        print(f'{prog}: Wheel must not be zero! No spriograph generated.', file=sys.stderr)
        sys.exit(-1)

    if args.excenter > 0.9:
        args.excenter = 0.9
        print(f'{prog}: Excenter limited to {args.excenter}', file=sys.stderr)
    
    if args.samples < 1:
        print(f'{prog}: Number of samples must be > 0 but is {args.samples}. Value set to 1.', file=sys.stderr)
        args.samples = 1

    spirograph = Spirograph(args.ring, args.wheel, args.excenter, args.offset, args.samples)

    M = (0, 0)
    c = int(spirograph.r_max() + 2)
    w = c * 2
    img = svg.Image((w, w), (c, c))
    img.desc.text = f'Spirograph: ring = {args.ring}, wheel = {args.wheel}, excenter = {args.excenter}, offset = {args.offset}, samples = {args.samples}'
    svg.Path(img.content, spirograph.svg_path(), { 'stroke-width': '0.5', 'stroke': 'black', 'fill': 'none'})
    img.write(args.filename)
