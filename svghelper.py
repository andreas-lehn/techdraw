import math
import numpy as np
import xml.etree.ElementTree as etree

class Image(etree.Element):

    def __init__(self, size, center, attrib={}, **extra):
        img_attrib = {
            'width': f'{size[0]}mm', 'height': f'{size[1]}mm',
            'viewBox': f'{-center[0]} {-center[1]} {size[0]} {size[1]}',
            'xmlns': 'http://www.w3.org/2000/svg', 'version': '1.1',
            **attrib }
        super().__init__('svg', img_attrib, **extra)
        self.style = etree.SubElement(self, 'style')
        self.content = etree.SubElement(self, 'g', { 'transform': 'scale(1, -1)', 'fill': 'lightgrey'})

    def write(self, file):
        tree = etree.ElementTree(self)
        etree.indent(tree, '    ')
        tree.write(file)

def len(p):
    return math.sqrt(p[0]**2 + p[1]**2)

def cart2pol(p):
    return np.array([len(p), angle(p)])

def pol2cart(r, phi):
    return np.array([r * np.cos(phi), r * np.sin(phi)])

def orth(p):
    x, y = p
    return np.array([-y, x])

def fmt(f):
    return f'{f:.3f}'

def angle(p):
    return np.arctan2(p[1], p[0])

def rad2grad(alpha):
    return 180 * alpha / math.pi

def grad2rad(alpha):
    return alpha * math.pi / 180

def Line(parent, p1, p2, attrib={}, **extra):
    x1, y1 = p1
    x2, y2 = p2
    return etree.SubElement(parent, 'line', { 'x1': fmt(x1), 'y1': fmt(y1), 'x2': fmt(x2), 'y2': fmt(y2), **medium_stroke, **attrib }, **extra)

def Circle(parent, center, radius, attrib={}, **extra):
    cx, cy = center
    return etree.SubElement(parent, 'circle', { 'cx': fmt(cx), 'cy': fmt(cy), 'r': fmt(radius), **thick_stroke, **attrib }, **extra)

def Point(parent, pos, attrib={}, **extra):
    cx, cy = pos
    return etree.SubElement(parent, 'circle', {'cx': fmt(cx), 'cy': fmt(cy), 'r': '0.5', 'fill': 'black', **attrib}, **extra)

def Path(parent, d, attrib={}, **extra):
    return etree.SubElement(parent, 'path', {'d': d, **thick_stroke, **attrib }, **extra)

def Translation(parent, origin, attrib={}, **extra):
    tx, ty = origin
    return etree.SubElement(parent, 'g', {'transform': f'translate({fmt(tx)} {fmt(ty)}', **attrib }, **extra)

def Rotation(parent, rotation, attrib={}, **extra):
    return etree.SubElement(parent, 'g', {'transform': f'rotate({fmt(rad2grad(-rotation))})', **attrib }, **extra)

def Text(parent, pos, text, attrib={}, rotation = 0, offset = (0, 0), **extra):
    x, y = pos
    g = etree.SubElement(parent, 'g', {'transform': f'translate({fmt(x)} {fmt(y)}) rotate({fmt(rad2grad(-rotation))})'})
    t = etree.SubElement(g, 'text', {'transform': f'translate({fmt(offset[0])} {fmt(offset[1])}) scale(0.25, -0.25)', 'fill': 'black', 'stroke': 'none', **attrib }, **extra)
    t.text = text
    return g

def LineLabel(parent, p1, p2, text, attrib={}, pos = 0.5, offset = 0.5, **extra):
    p = p1 + (p2 - p1) * pos
    alpha = angle(p2 - p1) - math.pi / 2
    return Text(parent, p, text, **attrib, rotation=alpha, offset=(0, offset), **extra)

def Arc(parent, p1, p2, r, attrib={}, clockwise = True, large = False, **extra):
    return Path(parent, PathCreator(p1).arc_to(p2, r), { 'fill': 'none', **attrib }, **extra)

def ArcLabel(parent, center, radius, alpha, text, attrib={}, offset = (0, 0), **extra):
    x, y = center
    pos = (x + radius * math.sin(alpha), y + radius * math.cos(alpha))
    return Text(parent, pos, text, **attrib, rotation=alpha, offset=offset, **extra)
    
class PathCreator:

    def __init__(self, p, alpha = 0):
        self.x, self.y = p
        self.alpha = alpha
        self.d = f'M {self.x:.3f} {self.y:.3f}'

    def intersection_point(self, x1, y1, alpha1):
        '''returns the intersection point of two lines'''
        dx0, dy0 = math.sin(self.alpha), math.cos(self.alpha)
        dx1, dy1 = math.sin(alpha1), math.cos(alpha1)
        '''
        x0 + r0 * dx0 = x1 + r1 * dx1
        y0 + r0 * dy0 = y1 + r1 * dy1
        -----------------------------
        r0 * dx0 - r1 * dx1 = x1 - x0
        r0 * dy0 - r1 * dy1 = y1 - y0
        '''
        a = np.array([[dx0, -dx1], [dy0, -dy1]])
        b = np.array([x1 - self.x, y1 - self.y])
        r = np.linalg.solve(a, b)
        return self.x + dx0 * r[0], self.y + dy0 * r[0]

    def bezier_to(self, p, alpha = 0):
        x1, y1 = p
        x0, y0 = self.intersection_point(x1, y1, alpha)
        self.d += f' Q {x0:.3f} {y0:.3f} {x1:.3f} {y1:.3f}'
        self.x, self.y, self.alpha = x1, y1, alpha
        return self.d

    def arc_to(self, p, r):
        self.x, self.y = p
        self.d += f' A {r:.3f} {r:.3f} 0 0 0 {self.x:.3f} {self.y:.3f}'
        return self.d

    def line_to(self, *points):
        for self.x, self.y in points:
            self.d += f' L {self.x:.3f} {self.y:.3f}'
        return self.d

    def close(self):
        self.d += ' C'
        return self.d

thick_stroke = { 'stroke': 'black', 'stroke-width': '0.35', 'stroke-linecap': 'round' }
medium_stroke = { 'stroke': 'black', 'stroke-width': '0.2', 'stroke-linecap': 'round' }
thin_stroke = { 'stroke': 'black', 'stroke-width': '0.1', 'stroke-linecap': 'round'}
sym_stroke = { 'stroke': 'black', 'stroke-width': '0.2', 'stroke-dasharray': '2.0 1.0 0.0 1.0', 'stroke-dashoffset': '1.0', 'stroke-linecap': 'round' }
dash_stroke = { 'stroke': 'black', 'stroke-width': '0.1', 'stroke-dasharray': '1.0 1.0', 'stroke-dashoffset': '0.5', 'stroke-linecap': 'round' }
dot_stroke = { 'stroke': 'black', 'stroke-width': '0.1', 'stroke-dasharray': '0.0 0.2', 'stroke-linecap': 'round' }
