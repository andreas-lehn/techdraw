#!/usr/env python3

import math
import numpy as np
import svghelper as svg

def gamma(alpha):
    '''
    Calculates the angle _gamma_ of _alpha_
        Parameter:
            alpha: angle on the base circle
        Returns:
            involute angle _gamma_ 
    '''
    return alpha - math.atan(alpha)

def distance(alpha):
    '''
    Calculates the distance _s_ to the center of the base circle with radius 1 of an involute point corresponding to _alpha_
        Parameter:
            alpha: angle on the base circle
        Returns:
            distance _s_ of the involute point form the center of the base circle
    '''
    return math.sqrt(alpha ** 2 + 1)

def point_polar(r, alpha):
    '''
    Calculates the polar coordinates of an involute point (angle _gamma_ and the distance _s_ to the center of the base circle)
        Parameter:
            r: radius of the base circle
            alpha: angle on the base circle
        Returns:
            involute angle _gamma_ 
            distance _s_ of the involute point form the center of the base circle
    '''
    return np.array([gamma(alpha), r * distance(alpha)])

def inverse(s):
    '''
    Calculates _alpha_ so that _gamma(alpha)_ returns s.

    It is a kind of inverse involute funktion.
        Parameter:
            s: distance of the involute point from the center of the base circle
        Returns:
            alpha: angle that the involute function needs to calculate (gamma, s)
    '''
    return math.sqrt(s ** 2 - 1)

def polar2xy(r, alpha):
    return r * np.array([math.sin(alpha), math.cos(alpha)])

def point_xy(r, alpha, offset = 0):
    gamma, s = point_polar(r, alpha)
    return polar2xy(s, gamma + offset)

def points(r, alpha, offset, n):
    alpha = alpha / n
    result = []
    for i in range(n):
        result.append(point_xy(r, (i + 1) * alpha, offset))
    return result

def flip(p):
    x, y = p
    return np.array([y, -x])

if __name__ == "__main__":
    r = 20
    n = 60
    alpha = 60 * math.pi / 180

    img = svg.Image((150, 100), (50, 50))

    # involutes
    svg.Path(img.content, svg.PathCreator((r, 0)).line_to(*points(r, math.pi, 0, n)), { 'fill': 'none' })

    # base circle
    svg.Circle(img.content, (0, 0), r)
    svg.Line(img.content, (-2 * r, 0), (2 * r, 0), svg.sym_stroke)
    svg.Line(img.content, (0, -2 * r), (0, 2 * r), svg.sym_stroke)

    # construction lines
    svg.Line(img.content, (0, 0), polar2xy(2 * r, alpha), svg.thin_stroke)
    svg.Line(img.content, (0, 0), polar2xy(2 * r, gamma(alpha)), svg.thin_stroke)
    q = point_xy(r, alpha)
    p = polar2xy(r, alpha)
    svg.Line(img.content, q - p, q + p, svg.thin_stroke)
    o = flip(p)
    svg.Line(img.content, q - o / 2, p + o / 2, svg.thin_stroke)

    # rechte Winkel
    #l = math.sqrt(dx ** 2 + dy ** 2)
    #ra = 5
    #dx, dy = dx / l * ra, dy / l * ra
    #c = math.sqrt(2) * 2
    #print(f'        <path class="dotline" d="M {px - dy} {py + dx} A {ra} {ra} 0 0 0 {px + dx} {py + dy}"/>')
    #print(f'        <circle cx="{px + (dx - dy) / c}" cy="{py + (dy + dx) / c}" r="0.25" fill="black"/>')
    #print(f'        <path class="dotline" d="M {qx - dy} {qy + dx} A {ra} {ra} 0 0 1 {qx - dx} {qy - dy}"/>')
    #print(f'        <circle cx="{qx - (dy + dx) / c}" cy="{qy + (dx - dy) / c}" r="0.25" fill="black"/>')

    # r
    svg.Line(img.content, (0, 0), p)
    svg.LineLabel(img.content, (0, 0), p, 'r')

    # alpha
    arc_stroke = { 'fill': 'none', 'stroke': 'red', 'stroke-width': svg.thick_stroke['stroke-width']}
    svg.Line(img.content, p, q, arc_stroke)
    svg.Arc(img.content, (0, r), p, r, arc_stroke)
    svg.ArcLabel(img.content, (0, 0), r + 0.5, 0.4 * alpha, u'\u03B1', {'fill': arc_stroke['stroke']})

    # gamma
    gamma_color = 'blue'
    svg.Line(img.content, (0, 0), q, {'stroke': gamma_color})
    svg.LineLabel(img.content, (0, 0), q, 's', 0.5, 0.5, {'fill': gamma_color})
    s = math.sqrt((q * q).sum())
    svg.Arc(img.content, (0, s), q, s, svg.thin_stroke, {'stroke': gamma_color})
    svg.ArcLabel(img.content, (0, 0), s + 0.5, 0.4 * gamma(alpha), u'\u03B3', {'fill': gamma_color})

    # key points
    svg.Point(img.content, (0, 0))
    svg.Point(img.content, (0, r))
    svg.Point(img.content, p)
    svg.Point(img.content, q)

    img.write('involute-sample.svg')
