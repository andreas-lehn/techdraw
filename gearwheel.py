#!/usr/env python3

import getopt
import sys
import math
import involute
import svghelper as svg

class GearWheel:
    ''' Involute gear wheel'''

    def __init__(self, modul, n_teeth, alpha = 20 * math.pi / 180):
        self.modul = modul
        self.n_teeth = n_teeth
        self.alpha = alpha

    def r_0(self):
        '''returns the radius of the gear wheel (Teilkreisradius)'''
        return self.modul * self.n_teeth / 2

    def r_head(self):
        '''returns the radius of the tooth heads (Kopfkreisradius)'''
        return self.r_0() + self.modul

    def r_foot(self):
        '''returns the radius of the tooth foot (Fußkreisradius)'''
        c = 0.167 # Magische Konstante, siehe: https://www.tec-science.com/de/getriebe-technik/evolventenverzahnung/evolventen-zahnrad-geometrie/
        return min(self.r_0() - self.modul, self.r_base()) - c * self.modul

    def r_base(self):
        '''returns the radius of the base circle'''
        return self.r_0() * math.cos(self.alpha)

    def theta(self):
        '''returns the angle between two teeth'''
        return 2 * math.pi / self.n_teeth

    def beta_0(self):
        '''returns the angle offsets of the intesection of the tooth with the Teilkreis'''
        return self.theta() / 4
    
    def beta_base(self):
        '''returns the angle offsets of the tooth base point'''
        return self.beta_0() + involute.gamma(self.alpha)

    def beta_head(self):
        '''returns the angle offsets of the tooths head point'''
        return self.beta_base() - involute.gamma(involute.inverse(self.r_head() / self.r_base()))
    
    def svg_path(self):
        r_0, r_h, r_b, r_f = self.r_0(), self.r_head(), self.r_base(), self.r_foot()
        b_0, b_h, b_b = self.beta_0(), self.beta_head(), self.beta_base()

        path = svg.Path(involute.polar2xy(r_f, -self.theta() / 2), - self.theta() / 2 + math.pi / 2)
        for i in range(self.n_teeth):
            offset = i * self.theta()
            path.bezierTo(involute.polar2xy(r_b, offset - b_b), offset - b_b)
            path.bezierTo(involute.polar2xy(r_0, offset - b_0), offset - b_0 + self.alpha)
            path.bezierTo(involute.polar2xy(r_h, offset - b_h), offset - b_h + involute.inverse(r_h / r_b))
            path.arcTo(involute.polar2xy(r_h, offset + b_h), r_h)
            path.alpha = offset + b_h - involute.inverse(r_h / r_b)
            path.bezierTo(involute.polar2xy(r_0, offset + b_0), offset + b_0 - self.alpha)
            path.bezierTo(involute.polar2xy(r_b, offset + b_b), offset + b_b)
            path.bezierTo(involute.polar2xy(r_f, offset + self.theta() / 2), offset + self.theta() / 2 + math.pi / 2)
        path.close()
        return path.d

def usage():
    print("usage:", sys.argv[0])
    print("    -a, --alpha <float> Eingriffswinkel in grad")
    print("    -h, --help          displays help")
    print("    -m, --modul <float> modul of gear wheel in mm")
    print("    -t, --teeth <int>   number of teeth")

if __name__ == "__main__":
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'm:t:a:h', ['modul=', 'teeth=', 'alpha=', 'help'])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    
    modul = 2.0
    teeth = 30
    alpha = 20
    for o, a in optlist:
        if (o in ("-m", "--modul")):
            modul = float(a)
        elif (o in ("-t", "--teeth")):
            teeth = int(a)
        elif (o in ("-a", "--alpha")):
            alpha = float(a)
        elif (o in ("-h", "--help")):
            usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"

    gear_wheel = GearWheel(modul, teeth, alpha * math.pi / 180)
    r_max = int(gear_wheel.r_head() * 1.1)
    size = r_max * 2
    print(f'<svg width="{size}mm" height="{size}mm" viewBox="{-size / 2} {-size / 2} {size} {size}" xmlns="http://www.w3.org/2000/svg" version="1.1" baseProfile="full">')
    print( '    <style>')
    print( '        .gearwheel { fill: lightgrey; stroke: black; stroke-width: 0.2}')
    print( '        .helpline  { fill: none; stroke: black; stroke-width: 0.05; stroke-dasharray: 1 0.8 }')
    print( '        .dotline   { fill: none; stroke: black; stroke-width: 0.05; stroke-dasharray: 0.1 0.1 }')
    print( '        .symline   { fill: none; stroke: black; stroke-width: 0.1; stroke-dasharray: 1.1 0.5 0.1 0.5; stroke-dashoffset: -0.55 }')
    print( '    </style>')
    print( '    <g transform="scale(1 -1)">')
    print(f'        <path   class="gearwheel" d="{gear_wheel.svg_path()}"/>')
    print(f'        <circle class="helpline"  r="{gear_wheel.r_head()}"/>')
    print(f'        <circle class="symline"   r="{gear_wheel.r_0()}"/>')
    print(f'        <circle class="dotline"   r="{gear_wheel.r_base()}"/>')
    print(f'        <circle class="helpline"  r="{gear_wheel.r_foot()}"/>')
    print( '    </g>')
    print( '</svg>')
