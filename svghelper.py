import math
import numpy as np
import xml.etree.ElementTree as etree

class Image(etree.Element):

    def __init__(self, size, center, *attrib, **extra):
        my_attrib = {
            'width': f'{size[0]}mm', 'height': f'{size[1]}mm',
            'viewBox': f'{-center[0]} {-center[1]} {size[0]} {size[1]}',
            'xmlns': 'http://www.w3.org/2000/svg', 'version': '1.1'}
        super().__init__('svg', merge_attributes(my_attrib, *attrib), **extra)
        self.style = etree.SubElement(self, 'style')
        self.content = etree.SubElement(self, 'g', { 'transform': 'scale(1, -1)', 'fill': 'lightgrey'})

    def write(self, file):
        tree = etree.ElementTree(self)
        etree.indent(tree, '    ')
        tree.write(file)

def merge_attributes(*attr_list):
        result = dict()
        for attrs in attr_list: result.update(attrs)
        return result

def cart2pol(p):
    p = np.array(p) 
    r = np.sqrt((p * p).sum())
    phi = np.arctan2(p[1], p[0])
    return np.array([r, phi])

def pol2cart(r, phi):
    return np.array([r * np.sin(phi), r * np.cos(phi)])

def orth(p):
    x, y = p
    return np.array([y, -x])

def str(f):
    return f'{f:.3f}'

def Line(parent, p1, p2, *user_attrs, **extra):
    x1, y1 = p1
    x2, y2 = p2
    return etree.SubElement(parent, 'line', merge_attributes({ 'x1': str(x1), 'y1': str(y1), 'x2': str(x2), 'y2': str(y2) }, mid_stroke, *user_attrs), **extra)

def Circle(parent, center, radius, *user_attrs, **extra):
    cx, cy = center
    return etree.SubElement(parent, 'circle', merge_attributes({ 'cx': str(cx), 'cy': str(cy), 'r': str(radius) }, thick_stroke, *user_attrs), **extra)

def Point(parent, pos, *user_attrs, **extra):
    cx, cy = pos
    return etree.SubElement(parent, 'circle', merge_attributes({'cx': str(cx), 'cy': str(cy), 'r': '0.5', 'fill': 'black'}, *user_attrs), **extra)

def Path(parent, d, *user_attrs, **extra):
    return etree.SubElement(parent, 'path', merge_attributes({'d': d}, thick_stroke, *user_attrs), **extra)

def Translation(parent, origin, *attrs, **extra):
    tx, ty = origin
    return etree.SubElement(parent, 'g', merge_attributes({'transform': f'translate({str(tx)} {str(ty)})'}, *attrs), **extra)

def Rotation(parent, rotation, *attrs, **extra):
    rotation = -180 * rotation / math.pi
    return etree.SubElement(parent, 'g', merge_attributes({'transform': f'rotate({str(rotation)})'}, *attrs), **extra)

def Text(parent, pos, text, *attrs, rotation = 0, offset = (0, 0), **extra):
    x, y = pos
    rotation = -180 * rotation / math.pi
    g = etree.SubElement(parent, 'g', {'transform': f'translate({str(x)} {str(y)}) rotate({str(rotation)})'})
    t = etree.SubElement(g, 'text', merge_attributes({'transform': f'translate({str(offset[0])} {str(offset[1])}) scale(0.25, -0.25)', 'fill': 'black', 'stroke': 'none'}, *attrs), **extra)
    t.text = text
    return g

def angle(p):
    p = np.array(p)
    return np.arccos(np.dot(np.array([0, 1]), p) / np.sqrt((p * p).sum()))

def LineLabel(parent, p1, p2, text, *attrs, pos = 0.5, offset = 0.5, **extra):
    p = p1 + (p2 - p1) * pos
    alpha = angle(p2 - p1) - math.pi / 2
    return Text(parent, p, text, *attrs, rotation=alpha, offset=(0, offset), **extra)

def Arc(parent, p1, p2, r, *attrs, clockwise = True, large = False, **extra):
    return Path(parent, PathCreator(p1).arc_to(p2, r), merge_attributes({ 'fill': 'none' }, *attrs), **extra)

def ArcLabel(parent, center, radius, alpha, text, *attrs, offset = (0, 0), **extra):
    x, y = center
    pos = (x + radius * math.sin(alpha), y + radius * math.cos(alpha))
    return Text(parent, pos, text, *attrs, rotation=alpha, offset=offset, **extra)

def intersection_point(x0, y0, alpha0, x1, y1, alpha1):
    '''returns the intersection point of two lines'''
    dx0, dy0 = math.sin(alpha0), math.cos(alpha0)
    dx1, dy1 = math.sin(alpha1), math.cos(alpha1)
    '''
    x0 + r0 * dx0 = x1 + r1 * dx1
    y0 + r0 * dy0 = y1 + r1 * dy1
    -----------------------------
    r0 * dx0 - r1 * dx1 = x1 - x0
    r0 * dy0 - r1 * dy1 = y1 - y0
    '''
    a = np.array([[dx0, -dx1], [dy0, -dy1]])
    b = np.array([x1 - x0, y1 - y0])
    r = np.linalg.solve(a, b)
    return x0 + dx0 * r[0], y0 + dy0 * r[0]

class PathCreator:

    def __init__(self, p, alpha = 0):
        self.x, self.y = p
        self.alpha = alpha
        self.d = f'M {self.x:.3f} {self.y:.3f}'

    def bezier_to(self, p, alpha = 0):
        x1, y1 = p
        x0, y0 = intersection_point(self.x, self.y, self.alpha, x1, y1, alpha)
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
mid_stroke = { 'stroke': 'black', 'stroke-width': '0.2', 'stroke-linecap': 'round' }
thin_stroke = { 'stroke': 'black', 'stroke-width': '0.1', 'stroke-linecap': 'round'}
sym_stroke = { 'stroke': 'black', 'stroke-width': '0.2', 'stroke-dasharray': '2.0 1.0 0.0 1.0', 'stroke-dashoffset': '1.0', 'stroke-linecap': 'round' }
