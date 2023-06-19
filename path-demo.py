#!/usr/env python3

import numpy as np
import svghelper as svg

def draw_state(parent, pos, angle):
    svg.Dot(parent, pos)
    svg.Line(parent, pos, pos + svg.pol2cart(10, angle), svg.thin_stroke)

img = svg.Image(size=(100, 100), center=(50, 50))
p = svg.PathCreator((0, 0), np.radians(30))
draw_state(img.content, p.pos(), p.alpha)
p.curve_to((10, 25), svg.radians(90))
draw_state(img.content, p.pos(), p.alpha)
p.line_to((5, 25), (0, 15), (-10, 25))
draw_state(img.content, p.pos(), p.alpha)
Q, beta = (-15, 25), svg.radians(100)
draw_state(img.content, Q, beta)
p.arc_to_line(Q, beta)
draw_state(img.content, p.pos(), p.alpha)
Q, beta = (-30, 30), svg.radians(-90)
draw_state(img.content, Q, beta)
p.arc_to_line(Q, beta)
draw_state(img.content, p.pos(), p.alpha)
beta = svg.radians(45)
draw_state(img.content, Q, beta)
p.arc_to_line(Q, beta)
draw_state(img.content, p.pos(), p.alpha)
beta = svg.radians(90)
draw_state(img.content, Q, beta)
p.arc_to_line(Q, beta)
draw_state(img.content, p.pos(), p.alpha)
Q, beta = (-30, 10), svg.radians(-45)
draw_state(img.content, Q, beta)
p.arc_to_line(Q, beta)
draw_state(img.content, p.pos(), p.alpha)
svg.Path(img.content, p.path, fill='none')
img.write('path-demo.svg')
