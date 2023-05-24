#!/usr/env python3

import getopt
import sys
import math
import numpy as np

def involute(alpha):
    '''
    Calculates the angle _gamma_ of the involute point and the distance _s_ of it form the center of the base circle.
        Parameter:
            alpha: angle on the base circle
        Returns:
            involute angle _gamma_ 
            distance _s_ of the involute point form the center of the base circle
    '''
    return alpha - math.atan(alpha), math.sqrt(alpha ** 2 + 1)

def inv_involute(s):
    '''
    Calculates _alpha_ so that _involute(alpha)_ returns (gamma, s).
    It is a kind of inverse involute funktion.
        Parameter:
            s: distance of the involute point from the center of the base circle
        Returns:
            alpha: angle that the involute function needs to calculate (gamma, s)
    '''
    return math.sqrt(s ** 2 - 1)

def polar2xy(r, alpha):
    return r * math.sin(alpha), r * math.cos(alpha)

def intersection_point(x0, y0, alpha0, x1, y1, alpha1):
    '''returns the intersection point of two lines'''
    dx0, dy0 = math.sin(alpha0), math.cos(alpha0)
    dx1, dy1 = math.sin(alpha1), math.cos(alpha1)
    '''
    x0 + r0 * dx0 = x1 + r1 * dx1
    y0 + r0 * dy0 = y1 + r1 * dy1
    -----------------------------
    r0 * dx0 - r1 * dx1 = x1 - x0
    r0 * dy0 - r1 * dy1 = y1 - y0
    '''
    a = np.array([[dx0, -dx1], [dy0, -dy1]])
    b = np.array([x1 - x0, y1 - y0])
    r = np.linalg.solve(a, b)
    return x0 + dx0 * r[0], y0 + dy0 * r[0]

def intersect_x(x, y, alpha):
    return intersection_point(0, 0, math.pi / 2, x, y, alpha)

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
        return self.r_0() - (1 + c) * self.modul

    def r_base(self):
        '''returns the radius of the base circle'''
        return self.r_0() * math.cos(self.alpha)

    def r_c(self):
        alpha = self.theta() / 2 - self.beta_base()
        return self.r_base() * math.sin(alpha)
    
    def theta(self):
        '''returns the angle between two teeth'''
        return 2 * math.pi / self.n_teeth

    def beta_0(self):
        '''returns the angle offsets of the intesection of the tooth with the Teilkreis'''
        return self.theta() / 4
    
    def beta_base(self):
        '''returns the angle offsets of the tooth base point'''
        return self.beta_0() + involute(self.alpha)[0]

    def beta_head(self):
        '''returns the angle offsets of the tooths head point'''
        return self.beta_base() - involute(inv_involute(self.r_head() / self.r_base()))[0]
    
    def svg_path(self):
        r_0, r_h, r_b, r_c = self.r_0(), self.r_head(), self.r_base(), self.r_c()
        b_0, b_h, b_b = self.beta_0(), self.beta_head(), self.beta_base()

        x0, y0 = polar2xy(r_b, -self.theta() + b_b)
        result = f'M {x0} {y0}'
        
        for i in range(self.n_teeth):
            offset = i * self.theta()
            x0, y0 = polar2xy(r_b, offset - b_b)
            result += f' A {r_c:.3f} {r_c:.3f} 0 0 1 {x0:.3f} {y0:.3f}'
            x1, y1 = polar2xy(r_0, offset - b_0)
            x0, y0 = intersection_point(x0, y0, offset - b_b, x1, y1, offset - b_0 + self.alpha)
            result += f' Q {x0:.3f} {y0:.3f} {x1:.3f} {y1:.3f}'
            x0, y0 = polar2xy(r_h, offset - b_h)
            x1, y1 = intersection_point(x1, y1, offset - b_0 + self.alpha, x0, y0, offset - b_h + inv_involute(r_h / r_b))
            result += f' Q {x1:.3f} {y1:.3f} {x0:.3f} {y0:.3f}'
            x0, y0 = polar2xy(r_h, offset + b_h)
            result += f' A {r_h:.3f} {r_h:.3f} 0 0 0 {x0:.3f} {y0:.3f}'
            x1, y1 = polar2xy(r_0, offset + b_0)
            x0, y0 = intersection_point(x0, y0, offset + b_h - inv_involute(r_h / r_b), x1, y1, offset + b_0 - self.alpha)
            result += f' Q {x0:.3f} {y0:.3f} {x1:.3f} {y1:.3f}'
            x0, y0 = polar2xy(r_b, offset + b_b)
            x1, y1 = intersection_point(x1, y1, offset + b_0 - self.alpha, x0, y0, offset + b_b)
            result += f' Q {x1:.3f} {y1:.3f} {x0:.3f} {y0:.3f}'
        return result + ' C'

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
    print( '        path { fill: lightgrey; stroke: black; stroke-width: 0.2}')
    print( '        .helpline  { fill: none; stroke: black; stroke-width: 0.05; stroke-dasharray: 1 0.8 }')
    print( '        .dotline   { fill: none; stroke: black; stroke-width: 0.05; stroke-dasharray: 0.1 0.1 }')
    print( '        .symline   { fill: none; stroke: black; stroke-width: 0.1; stroke-dasharray: 1.1 0.5 0.1 0.5; stroke-dashoffset: -0.55 }')
    print( '    </style>')
    print( '    <g transform="scale(1 -1)">')
    print(f'        <path d="{gear_wheel.svg_path()}"/>')
    print(f'        <circle class="helpline" r="{gear_wheel.r_head()}"/>')
    print(f'        <circle class="symline"  r="{gear_wheel.r_0()}"/>')
    print(f'        <circle class="dotline"  r="{gear_wheel.r_base()}"/>')
    print(f'        <circle class="helpline" r="{gear_wheel.r_foot()}"/>')
    print( '    </g>')
    print( '</svg>')
