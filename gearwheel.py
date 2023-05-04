#!/usr/env python3

import getopt
import sys

def gear_wheel_ctrl_points(m, z):
    return []

def usage():
    print(sys.argv[0] + " usage:")
    print("    -n, --n-teeth <int> number of teeth")
    print("    -m, --modul <float> modul of gear wheel in mm")

def main():
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'm:t:', ['modul=', 'teeth='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    
    m = 2.0
    t = 24
    n = 2
    output = sys.stdout
    for o, a in optlist:
        if (o in ("-m", "--modul")):
            m = float(a)
        elif (o in ("-t", "--teeth")):
            n = int(a)
        else:
            assert False, "unhandled option"
    if len(args) > 0:
        output = open(args[0], 'w')

    print(f'modul [mm]      = {m}')
    print(f'number of teeth = {t}')
    print("args = ", args)
    
    print('These are the gear wheel control points: ...', file = output)
    
if __name__ == "__main__":
    main()
