
import math
import techdraw as svg

if __name__ == "__main__":
    r = 20
    
    alpha = math.pi / 4
    beta  = -math.pi / 6
    gamma = math.pi - math.pi / 6
    delta = math.pi / 2

    P = svg.pol2cart(r, alpha)
    Q = svg.pol2cart(r, beta)
    S = svg.pol2cart(r, gamma)
    T = svg.pol2cart(r, delta)
    M = (0, 0)

    img = svg.Image(size=(150, 100), center=(50, 50))
    svg.Circle(img.content, M, r)
    svg.Text(img.content, (-1.5, 1), 'M')
    svg.Line(img.content, (-2 * r, 0), (2 * r, 0), svg.SYM_STROKE)
    svg.Line(img.content, (0, -2 * r), (0, 2 * r), svg.SYM_STROKE)
    svg.Line(img.content, M, 2 * svg.pol2cart(r, alpha), svg.THIN_STROKE)
    svg.Dot(img.content, P, fill='red')
    svg.Text(img.content, P, 'P', offset=(-1, 1), rotation=alpha - math.pi/2, fill='red')
    svg.Line(img.content, M, P, stroke='red')
    svg.Dot(img.content, M)
    svg.LineLabel(img.content, M, P, 'r', pos=0.6, fill='red')
    svg.Path(img.content, svg.PathCreator(T).line_to(Q, S, T).path, svg.THIN_STROKE, fill='none')
    svg.Arc(img.content, svg.pol2cart(1.5 * r, 0), 1.5 * P, 1.5 * r, svg.THIN_STROKE)
    svg.ArcLabel(img.content, M, 1.5 * r, 0.5 * alpha, u'\u03B1', offset=(0, 0.5))
    
    img.write('svg-demo.svg')
