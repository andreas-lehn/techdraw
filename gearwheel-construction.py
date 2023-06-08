#!/usr/env python3

import math
from gearwheel import GearWheel
import svghelper as svg

if __name__ == "__main__":
    modul = 10
    teeth = 12
    alpha = 20

    gear_wheel = GearWheel(modul, teeth, alpha * math.pi / 180)
    p = gear_wheel.tooth_ctrl_points()

    M = (0, 0)
    width = int(gear_wheel.r_head() * 2) + 2
    height = int(gear_wheel.r_head() * 1.75) + 2
    img = svg.Image((width, height), (int(width / 2) - 1, height - 1))

    # draw a single tooth
    r, phi, tan = p[3]
    P0 = svg.pol2cart(r, -phi)
    creator = svg.PathCreator(P0, -tan)
    r, phi, tan = p[2]
    P1 = svg.pol2cart(r, -phi)
    creator.bezier_to(P1, -tan)
    r, phi, tan = p[1]
    P2 = svg.pol2cart(r, -phi)
    creator.bezier_to(P2, -tan)
    r, phi, tan = p[0]
    P3 = svg.pol2cart(r, -phi)
    creator.bezier_to(P3, -tan)
    P4 = svg.pol2cart(r, phi)
    creator.arc_to(P4, gear_wheel.r_head())
    creator.alpha = tan
    r, phi, tan = p[1]
    P5 = svg.pol2cart(r, phi)
    creator.bezier_to(P5, tan)
    r, phi, tan = p[2]
    P6 = svg.pol2cart(r, phi)
    creator.bezier_to(P6, tan)
    r, phi, tan = p[3]
    P7 = svg.pol2cart(r, phi)
    creator.bezier_to(P7, tan)
    svg.Path(img.content, gear_wheel.svg_path(), stroke='lightgrey', fill='none')
    svg.Path(img.content, creator.d)
    svg.Path(img.content, svg.PathCreator(P0).line_to(P7, M), stroke='none')

    # draw Teilkreis and Grundkreis
    r = gear_wheel.r_0()
    M0 = svg.pol2cart(r, -phi)
    M1 = svg.pol2cart(r, 0)
    M2 = svg.pol2cart(r, phi)    
    svg.Arc(img.content, M0, M2, r, svg.sym_stroke)

    r = gear_wheel.r_base()
    svg.Arc(img.content, svg.pol2cart(r, -phi), svg.pol2cart(r, phi), r, svg.dot_stroke)

    # draw symetrie lines and theta
    r = gear_wheel.r_0()
    c = 1.75
    svg.Line(img.content, M, c * M0, svg.thin_stroke)
    svg.Line(img.content, M, c * M2, svg.thin_stroke)
    c -= 0.05
    svg.Arc(img.content, c * M0, c * M2, c * r, svg.thin_stroke)
    svg.ArcLabel(img.content, M, c * r, 0, u'\u03C4', offset=(-0.5, 0.5))
    c -= 0.05
    svg.Line(img.content, M, c * M1, svg.sym_stroke)
    c -= 0.05
    svg.Arc(img.content, c * M0, c * M2, c * r, svg.thin_stroke)
    theta2 = gear_wheel.theta() / 4
    svg.ArcLabel(img.content, M, c * r, -theta2, u'\u03C4/2', offset=(-2.3, 0.5))
    svg.ArcLabel(img.content, M, c * r,  theta2, u'\u03C4/2', offset=(-2.3, 0.5))

    #draw base angles
    c -= 0.05
    phi = gear_wheel.beta_base()
    svg.Line(img.content, M, svg.pol2cart(c * r, -phi), svg.thin_stroke)
    svg.Line(img.content, M, svg.pol2cart(c * r,  phi), svg.thin_stroke)
    c -= 0.05
    svg.Arc(img.content, svg.pol2cart(c * r, -phi), svg.pol2cart(c * r, phi), c * r, svg.thin_stroke)
    svg.ArcLabel(img.content, M, c * r, -phi / 2, u'\u03B2', offset=(-0.9, 0.5))
    svg.ArcLabel(img.content, M, c * r,  phi / 2, u'\u03B2', offset=(-0.9, 0.5))

    # draw Teilkreis angles
    c -= 0.05
    svg.Line(img.content, M, svg.pol2cart(c * r, -gear_wheel.beta_0()), svg.thin_stroke)
    svg.Line(img.content, M, svg.pol2cart(c * r,  gear_wheel.beta_0()), svg.thin_stroke)
    c -= 0.05
    svg.Arc(img.content, svg.pol2cart(c * r, -gear_wheel.beta_0()), svg.pol2cart(c * r, gear_wheel.beta_0()), c * r, svg.thin_stroke)
    svg.ArcLabel(img.content, M, c * r, -theta2 / 2, u'\u03C4/4', offset=(-2.3, 0.5))
    svg.ArcLabel(img.content, M, c * r,  theta2 / 2, u'\u03C4/4', offset=(-2.3, 0.5))

    # draw head angles
    c -= 0.05
    phi = gear_wheel.beta_head()
    svg.Line(img.content, M, svg.pol2cart(c * r, -phi), svg.thin_stroke)
    svg.Line(img.content, M, svg.pol2cart(c * r,  phi), svg.thin_stroke)
    c -= 0.05
    svg.Arc(img.content, svg.pol2cart(c * r, -phi), svg.pol2cart(c * r, phi), c * r, svg.thin_stroke)
    svg.ArcLabel(img.content, M, c * r, -phi / 2, u'\u03B3', offset=(-0.9, 0.5))
    svg.ArcLabel(img.content, M, c * r,  phi / 2, u'\u03B3', offset=(-0.9, 0.5))

    # Mittelpunkt und Controllpunkte
    svg.Point(img.content, M)
    svg.Point(img.content, P0)
    svg.Point(img.content, P1)
    svg.Point(img.content, P2)
    svg.Point(img.content, P3)
    svg.Point(img.content, P4)
    svg.Point(img.content, P5)
    svg.Point(img.content, P6)
    svg.Point(img.content, P7)

    img.write('gearwheel-construction.svg')
