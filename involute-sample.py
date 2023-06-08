#!/usr/env python3

import math
import numpy as np
import svghelper as svg
import involute

if __name__ == "__main__":
    r = 20 # radius of bas circle
    M = np.array([0, 0]) # mid point of base circle

    n = 60 # number of line segements
    max_alpha = math.pi # max alpha of involute
    alpha = 60 * math.pi / 180 # angle of example point
    P = svg.pol2cart(r, alpha) # example point on base circle
    Q = involute.point_xy(r, alpha) # example point on involute
    d = r * involute.distance(alpha) # length of 
    S = np.array([0, r]) # start point of involute
    O = involute.flip(P) # orthognal vector of P

    img = svg.Image((150, 100), (50, 50))

    # involutes
    svg.Path(img.content, svg.PathCreator(S).line_to(*involute.points(r, max_alpha, 0, n)), fill='none')

    # base circle
    svg.Circle(img.content, M, r)
    svg.Line(img.content, (-2 * r, 0), (2 * r, 0), svg.sym_stroke)
    svg.Line(img.content, (0, -2 * r), (0, 2 * r), svg.sym_stroke)

    # construction lines
    svg.Line(img.content, M, svg.pol2cart(2 * r, alpha), svg.thin_stroke)
    svg.Line(img.content, M, svg.pol2cart(2 * r, involute.gamma(alpha)), svg.thin_stroke)
    svg.Line(img.content, Q - P, Q + P, svg.thin_stroke)
    svg.Line(img.content, Q - O / 2, P + O / 2, svg.thin_stroke)

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
    svg.Line(img.content, M, P)
    svg.LineLabel(img.content, M, P, 'r')

    # alpha
    arc_stroke = { 'fill': 'none', 'stroke': 'red', 'stroke-width': svg.thick_stroke['stroke-width']}
    svg.Line(img.content, P, Q, arc_stroke)
    svg.Arc(img.content, S, P, r, arc_stroke)
    svg.ArcLabel(img.content, M, r, 0.4 * alpha, u'\u03B1', offset=(-0.5, 0.5), fill=arc_stroke['stroke'])

    # gamma
    gamma_color = 'blue'
    svg.Line(img.content, M, Q, stroke=gamma_color)
    svg.LineLabel(img.content, M, Q, 's', fill=gamma_color)
    svg.Arc(img.content, (0, d), Q, d, svg.thin_stroke, stroke=gamma_color)
    svg.ArcLabel(img.content, M, d, 0.5 * involute.gamma(alpha), u'\u03B3', offset=(-0.5, 0.5), fill=gamma_color)

    # key points
    svg.Point(img.content, M)
    svg.Point(img.content, S)
    svg.Point(img.content, P)
    svg.Point(img.content, Q)

    img.write('involute-sample.svg')
