#!/usr/env python3

import getopt
import sys
import math

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

def inv_alpha(s):
    '''
    Calculates _alpha_ so that _involute(alpha)_ returns (gamma, d).
    It is a kind of inverse involute funktion.
        Parameter:
            r: distance of the involute point from the center of the base circle
        Returns:
            alpha: angle that the involure function need to calculate (gamma, r)
    '''
    return math.sqrt(s ** 2 - 1)

def polar2xy(r, alpha):
    return r * math.sin(alpha), r * math.cos(alpha)

class GearWheel:
    ''' Involute gear wheel'''

    def __init__(self, modul, n_teeth, alpha = 20 * math.pi / 180):
        self.modul = modul
        self.n_teeth = n_teeth
        self.alpha = alpha

    def radius(self):
        '''returns the radius of the gear wheel (Teilkreisradius)'''
        return self.modul * self.n_teeth / 2

    def r_head(self):
        '''return the radius of the tooth heads (Kopfkreisradius)'''
        return self.radius() + self.modul

    def r_foot(self):
        '''return the radius of the tooth heads (Kopfkreisradius)'''
        return self.radius() - self.modul

    def r_base(self):
        '''returns the radius of the base circle'''
        return self.radius() * math.cos(self.alpha)

    def alpha_teeth(self):
        '''returns the angle between two teeth'''
        return 2 * math.pi / self.n_teeth

    def ctrl_angles(self):
        '''returns the angle offsets of the characteristc tooth points on Kopfkreis, Teilkreis, Grundkreis'''
        beta = self.alpha_teeth() / 4
        gamma = beta + involute(self.alpha)[0]
        alpha = gamma - involute(inv_alpha(self.r_head() / self.r_base()))[0]
        return [alpha, beta, gamma]

    def ctrl_points(self):
        points = []
        angles = self.ctrl_angles()
        r0 = self.radius()
        rh = self.r_head()
        rb = self.r_base()
        rf = self.r_foot()
        for i in range(self.n_teeth):
            offset = i * self.alpha_teeth()
            point = []
            point.append(polar2xy(rf, offset - angles[2]))
            point.append(polar2xy(rb, offset - angles[2]))
            point.append(polar2xy(r0, offset - angles[1]))
            point.append(polar2xy(rh, offset - angles[0]))
            point.append(polar2xy(rh, offset + angles[0]))
            point.append(polar2xy(r0, offset + angles[1]))
            point.append(polar2xy(rb, offset + angles[2]))
            point.append(polar2xy(rf, offset + angles[2]))
            points.append(point)
        return points

    def svg_line_path(self):
        wheel_points = self.ctrl_points()
        result = ''
        cmd = 'M'
        for tooth_points in wheel_points:
            for x, y in tooth_points:
                result += f'{cmd} {x} {y}'
                cmd = ' L'
        return result + ' C'

def usage():
    print(sys.argv[0] + " usage:")
    print("    -t, --teeth <int> number of teeth")
    print("    -m, --modul <float> modul of gear wheel in mm")

if __name__ == "__main__":
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'm:t:', ['modul=', 'teeth='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    
    m = 2.0
    t = 30
    for o, a in optlist:
        if (o in ("-m", "--modul")):
            m = float(a)
        elif (o in ("-t", "--teeth")):
            t = int(a)
        else:
            assert False, "unhandled option"

    gear_wheel = GearWheel(m, t)
    print( '<svg width="10cm" height="20cm" viewBox="-100 -100 200 200" xmlns="http://www.w3.org/2000/svg" version="1.1" baseProfile="full">')
    print(f'    <path id="gearwheel" d="{gear_wheel.svg_line_path()}" fill="blue" stroke="black" stroke-width="0.5"/>')
    print(f'    <circle id="headcircle" r="{gear_wheel.radius()}" fill="none" stroke="black" stroke-width="0.1"/>')
    print(f'    <circle id="basecircle" r="{gear_wheel.r_base()}" fill="none" stroke="black" stroke-width="0.1"/>')
    print( '</svg>')
