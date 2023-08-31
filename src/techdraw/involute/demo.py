
import numpy as np
import techdraw as svg
from .. import involute

if __name__ == "__main__":
    r = 20 # radius of bas circle
    M = np.array([0, 0]) # mid point of base circle

    n = 60 # number of line segements
    max_alpha = svg.radians(-180) # max alpha of involute
    alpha = svg.radians(-60) # angle on the base circle
    gamma = involute.gamma(alpha) # angle of the involute point
    P = svg.pol2cart(r, alpha) # example point on base circle
    Q = involute.point(r, alpha) # example point on involute
    d = involute.distance(r, alpha) # length of 
    S = svg.pol2cart(r, 0) # start point of involute
    O = svg.orth(P) # orthognal vector of P

    img = svg.Image((150, 100), (50, 50))
    img.content = svg.Rotation(img.content, svg.radians(90))

    # involutes
    svg.Path(img.content, svg.PathCreator(S).line_to(*involute.points(r, max_alpha, 0, n)).path, fill='none')

    # base circle
    svg.Circle(img.content, M, r)
    svg.Line(img.content, (-2 * r, 0), (2 * r, 0), svg.SYM_STROKE)
    svg.Line(img.content, (0, -2 * r), (0, 2 * r), svg.SYM_STROKE)

    # construction lines
    svg.Line(img.content, M, svg.pol2cart(2 * r, alpha), svg.THIN_STROKE)
    svg.Line(img.content, M, svg.pol2cart(2 * r, gamma), svg.THIN_STROKE)
    svg.Line(img.content, Q - P, Q + P, svg.THIN_STROKE)
    svg.Line(img.content, Q - O / 2, P + O / 2, svg.THIN_STROKE)
    svg.RightAngleSymbol(img.content, P, alpha)
    svg.RightAngleSymbol(img.content, Q, alpha, clockwise=True)

    # r
    svg.Line(img.content, M, P)
    svg.LineLabel(img.content, M, P, 'r')

    # alpha
    arc_stroke = { 'fill': 'none', 'stroke': 'red', 'stroke-width': svg.THICK_STROKE['stroke-width']}
    svg.Line(img.content, P, Q, arc_stroke)
    svg.Arc(img.content, P, S, r, arc_stroke)
    svg.ArcLabel(img.content, M, r, 0.4 * alpha, '\u03B1', offset=(-0.5, 0.5), fill=arc_stroke['stroke'])

    # gamma
    gamma_color = 'blue'
    svg.Line(img.content, M, Q, stroke=gamma_color)
    svg.LineLabel(img.content, M, Q, 's', fill=gamma_color)
    svg.Arc(img.content, Q, svg.pol2cart(d, 0), d, svg.THIN_STROKE, stroke=gamma_color)
    svg.ArcLabel(img.content, M, d, 0.5 * gamma, '\u03B3', offset=(-0.5, 0.5), fill=gamma_color)

    # key points
    svg.Dot(img.content, M)
    svg.Dot(img.content, S)
    svg.Dot(img.content, P)
    svg.Dot(img.content, Q)

    img.write('techdraw/involute/demo.svg')
