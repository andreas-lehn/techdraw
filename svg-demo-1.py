#!/usr/env python3

import math
import numpy as np
import svghelper as svg

if __name__ == "__main__":
    r = 20
    
    alpha = math.pi / 3
    beta  = math.pi - math.pi / 6
    gamma = -math.pi / 6
    delta = math.pi / 2

    P = svg.pol2cart(r, alpha)
    Q = svg.pol2cart(r, beta)
    S = svg.pol2cart(r, gamma)
    T = svg.pol2cart(r, delta)
    M = (0, 0)

    img = svg.Image(size=(150, 100), center=(50, 50))
    svg.Circle(img.content, M, r)
    svg.Text(img.content, (-1.5, 1), 'M')
    svg.Line(img.content, (-2 * r, 0), (2 * r, 0), svg.sym_stroke)
    svg.Line(img.content, (0, -2 * r), (0, 2 * r), svg.sym_stroke)
    svg.Line(img.content, M, (2 * r * math.sin(alpha), 2 * r * math.cos(alpha)), svg.thin_stroke)
    svg.Point(img.content, P, fill='red')
    svg.Text(img.content, P, 'P', offset=(-1, 1), rotation=alpha, fill='red')
    svg.Line(img.content, M, P, stroke='red')
    svg.Point(img.content, M)
    svg.LineLabel(img.content, M, P, 'r', pos=0.6, fill='red')
    svg.Path(img.content, svg.PathCreator(T).line_to(Q, S, T), svg.thin_stroke, fill='none')
    svg.Arc(img.content, (0, 1.5 * r), 1.5 * P, 1.5 * r, svg.thin_stroke)
    svg.ArcLabel(img.content, M, 1.5 * r, 0.5 * alpha, u'\u03B1', offset=(0, 0.5))
    img.write('svg-demo-1.svg')
