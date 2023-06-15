import numpy as np
import xml.etree.ElementTree as etree

class Image(etree.Element):

    def __init__(self, size, center, attrib={}, **extra):
        img_attrib = {
            'width': f'{fmt_f(size[0])}mm', 'height': f'{fmt_f(size[1])}mm',
            'viewBox': f'{fmt_f(-center[0], -center[1], *size)}',
            'xmlns': 'http://www.w3.org/2000/svg', 'version': '1.1',
            **attrib }
        super().__init__('svg', img_attrib, **extra)
        #TODO: Description hinzufügen
        self.style = etree.SubElement(self, 'style')
        self.content = etree.SubElement(self, 'g', { 'transform': 'scale(1, -1)', 'fill': 'lightgrey'})

    def write(self, file):
        tree = etree.ElementTree(self)
        etree.indent(tree, '    ')
        tree.write(file)

def length(p):
    return np.sqrt(p[0]**2 + p[1]**2)

def cart2pol(p):
    return np.array([length(p), angle(p)])

def pol2cart(r, phi):
    return np.array([r * np.cos(phi), r * np.sin(phi)])

def orth(p):
    x, y = p
    return np.array([-y, x])

def fmt_f(f, *floats):
    result = f'{f:.3f}'
    for f in floats:
        result += f' {f:.3f}'
    return result

def angle(p):
    return np.arctan2(p[1], p[0])

def degrees(alpha):
    return np.degrees(alpha)

def radians(alpha):
    return np.radians(alpha)

def Line(parent, p1, p2, attrib={}, **extra):
    x1, y1 = p1
    x2, y2 = p2
    return etree.SubElement(parent, 'line', { 'x1': fmt_f(x1), 'y1': fmt_f(y1), 'x2': fmt_f(x2), 'y2': fmt_f(y2), **medium_stroke, **attrib }, **extra)

def Circle(parent, center, radius, attrib={}, **extra):
    cx, cy = center
    return etree.SubElement(parent, 'circle', { 'cx': fmt_f(cx), 'cy': fmt_f(cy), 'r': fmt_f(radius), **thick_stroke, **attrib }, **extra)

def Dot(parent, pos, attrib={}, **extra):
    cx, cy = pos
    return etree.SubElement(parent, 'circle', {'cx': fmt_f(cx), 'cy': fmt_f(cy), 'r': '0.5', 'fill': 'black', **attrib}, **extra)

def Path(parent, d, attrib={}, **extra):
    return etree.SubElement(parent, 'path', {'d': d, **thick_stroke, **attrib }, **extra)

def Translation(parent, origin, attrib={}, **extra):
    return etree.SubElement(parent, 'g', {'transform': f'translate({fmt_f(*origin)}', **attrib }, **extra)

def Rotation(parent, rotation, attrib={}, **extra):
    return etree.SubElement(parent, 'g', {'transform': f'rotate({fmt_f(degrees(rotation))})', **attrib }, **extra)

def Text(parent, pos, text, attrib={}, rotation = 0, offset = (0, 0), **extra):
    g = etree.SubElement(parent, 'g', {'transform': f'translate({fmt_f(*pos)}) rotate({fmt_f(degrees(rotation))})'})
    t = etree.SubElement(g, 'text', {'transform': f'translate({fmt_f(*offset)}) scale(0.25, -0.25)', 'fill': 'black', 'stroke': 'none', **attrib }, **extra)
    t.text = text
    return g

def LineLabel(parent, p1, p2, text, attrib={}, pos = 0.5, offset = 0.5, **extra):
    p = p1 + (p2 - p1) * pos
    return Text(parent, p, text, **attrib, rotation=angle(p2 - p1), offset=(0, offset), **extra)

def Arc(parent, p1, p2, r, attrib={}, **extra):
    return Path(parent, PathCreator(p1).arc_to(p2, r).path, { 'fill': 'none', **attrib }, **extra)

def ArcLabel(parent, center, radius, alpha, text, attrib={}, offset=(0.0, 0.0), **extra):
    pos = np.array(center) + pol2cart(radius, alpha)
    return Text(parent, pos, text, **attrib, rotation = alpha - radians(90), offset=offset, **extra)

def RightAngleSymbol(parent, pos, rotation, attrib={}, clockwise=False, **extra):
    pos = np.array(pos)
    v1 = pol2cart(5, rotation)
    v2 = orth(v1)
    if clockwise:
        v1, v2 = -v2, v1
    g = etree.SubElement(parent, 'g')
    result = Path(g, PathCreator(pos + v1).arc_to(pos + v2, length(v2)).path, { **thin_stroke, 'fill': 'none', **attrib}, **extra)
    Dot(g, pos + (v1 + v2) / 2 / np.sqrt(2))
    return result

class PathCreator:
    #TODO: Arc verändern, dass es mit Punkt und Richtung funktioniert

    def __init__(self, p, alpha = 0.0):
        self.x, self.y = p
        self.alpha = alpha
        self.path = f'M {fmt_f(self.x, self.y)}'

    def add(self, path):
        self.path += ' ' + path
    
    def pos(self):
        return np.array([self.x, self.y])
    
    def intersection_point(self, x1, y1, alpha1):
        '''returns the intersection point of two lines'''
        dx0, dy0 = pol2cart(1, self.alpha)
        dx1, dy1 = pol2cart(1, alpha1)
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

    def curve_to(self, p, angle):
        x1, y1 = p
        x0, y0 = self.intersection_point(x1, y1, angle)
        self.add(f'Q {fmt_f(x0, y0, x1, y1)}')
        self.x, self.y, self.alpha = x1, y1, angle
        return self

    def arc_to(self, p, r):
        self.x, self.y = p
        self.add(f'A {fmt_f(r, r)} 0 0 1 {fmt_f(self.x, self.y)}')
        return self

    def line_to(self, *points):
        for x, y in points:
            self.add(f'L {fmt_f(x, y)}')
            self.x, self.y, self.alpha = x, y, angle((x - self.x, y - self.y))
        return self

    def line(self, distance):
        return self.line_to(self.pos() + pol2cart(distance, self.alpha))
    
    def move_to(self, p, angle=0.0):
        self.x, self.y = p
        self.alpha = angle
        self.add(f'M {fmt_f(self.x, self.y)}')
        return self

    def close(self):
        self.add('C')
        return self

thick_stroke = { 'stroke': 'black', 'stroke-width': '0.35', 'stroke-linecap': 'round' }
medium_stroke = { 'stroke': 'black', 'stroke-width': '0.2', 'stroke-linecap': 'round' }
thin_stroke = { 'stroke': 'black', 'stroke-width': '0.1', 'stroke-linecap': 'round'}
sym_stroke = { 'stroke': 'black', 'stroke-width': '0.2', 'stroke-dasharray': '2.0 1.0 0.0 1.0', 'stroke-dashoffset': '1.0', 'stroke-linecap': 'round' }
dash_stroke = { 'stroke': 'black', 'stroke-width': '0.1', 'stroke-dasharray': '1.0 1.0', 'stroke-dashoffset': '0.5', 'stroke-linecap': 'round' }
dot_stroke = { 'stroke': 'black', 'stroke-width': '0.1', 'stroke-dasharray': '0.0 0.2', 'stroke-linecap': 'round' }
