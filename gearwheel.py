#!/usr/env python3

import argparse
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
        return self.beta_base() - involute.gamma(involute.inverse(self.r_base(), self.r_head()))
    
    def svg_path(self):
        r_0, r_h, r_b, r_f = self.r_0(), self.r_head(), self.r_base(), self.r_foot()
        b_0, b_h, b_b, b_f = self.beta_0(), self.beta_head(), self.beta_base(), self.theta() / 2

        path = svg.PathCreator(svg.pol2cart(r_f, -b_f), -b_f / 2 + math.pi / 2)
        for i in range(self.n_teeth):
            offset = i * self.theta()
            path.bezier_to(svg.pol2cart(r_b, offset - b_b), offset - b_b)
            path.bezier_to(svg.pol2cart(r_0, offset - b_0), offset - b_0 + self.alpha)
            path.bezier_to(svg.pol2cart(r_h, offset - b_h), offset - b_h + involute.inverse(r_b, r_h))
            path.arc_to(svg.pol2cart(r_h, offset + b_h), r_h)
            path.alpha = offset + b_h - involute.inverse(r_b, r_h)
            path.bezier_to(svg.pol2cart(r_0, offset + b_0), offset + b_0 - self.alpha)
            path.bezier_to(svg.pol2cart(r_b, offset + b_b), offset + b_b)
            path.bezier_to(svg.pol2cart(r_f, offset + b_f), offset + b_f + math.pi / 2)
        path.close()
        return path.d

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
