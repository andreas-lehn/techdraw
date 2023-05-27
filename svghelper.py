#!/usr/env python3

import math
import numpy as np
import xml.etree.ElementTree as etree

class Image(etree.Element):

    def __init__(self, size, center, attrib = {}):
        my_attrs = {
            'width': f'{size[0]}mm', 'height': f'{size[1]}mm',
            'viewBox': f'{-center[0]} {-center[1]} {size[0]} {size[1]}',
            'xmlns': 'http://www.w3.org/2000/svg', 'version': '1.1'}
        my_attrs.update(attrib)
        super().__init__('svg', my_attrs)
        self.style = etree.SubElement(self, 'style')
        self.content = etree.SubElement(self, 'g', {'transform': 'scale(1, -1)', 'fill': 'lightgrey', 'stroke': 'black', 'stroke-width': '0.35' })

    def write(self, file):
        tree = etree.ElementTree(self)
        tree.write(file)

class Element(etree.Element):
    def __init__(self, parent, tag, elem_attrs = {}, user_attrs = {}):
        elem_attrs.update(user_attrs) # User attributes overwrite element attributes
        super().__init__(tag, elem_attrs)
        parent.append(self)

def str(f):
    return f'{f:.3f}'

def normalize(p):
    x, y = p
    l = math.sqrt(x ** 2, y ** 2)
    return x / l, y / l

class Line(Element):
    def __init__(self, parent, p1, p2, user_attrs = {}):
        x1, y1 = p1
        x2, y2 = p2
        super().__init__(parent, 'line', {'x1': str(x1), 'y1': str(y1), 'x2': str(x2), 'y2': str(y2), 'stroke-width': '0.2'}, user_attrs)

class Circle(Element):
    def __init__(self, parent, center, radius, user_attrs = {}):
        cx, cy = center
        super().__init__(parent, 'circle', {'cx': str(cx), 'cy': str(cy), 'r': str(radius)}, user_attrs)

class Point(Element):
    def __init__(self, parent, p, user_attrs = {}):
        cx, cy = p
        super().__init__(parent, 'circle', {'cx': str(cx), 'cy': str(cy), 'r': '0.5', 'fill': 'black', 'stroke': 'none'}, user_attrs)

class Path(Element):
    def __init__(self, parent, d, user_attrs = {}):
        super().__init__(parent, 'path', {'d': d}, user_attrs)

class Group(Element):
    def __init__(self, parent, origin, attributes = {}):
        x, y = origin
        super().__init__(parent, 'g', {f'transform': 'translate({x} {y}) rotate({rotation})'}, attributes)

class Text(Element):
    def __init__(self, parent, origin, text, attributes = {}):
        x, y = origin
        super().__init__(parent, 'g', {f'transform': f'translate({x} {y})'})
        t = Element(self, 'text', {'transform': 'scale(0.25, -0.25)', 'fill': 'black', 'stroke': 'none'}, attributes)
        t.text = text

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

    def __init__(self, p, alpha):
        self.x, self.y = p
        self.alpha = alpha
        self.d = f'M {self.x:.3f} {self.y:.3f}'

    def bezier_to(self, p, alpha):
        x1, y1 = p
        x0, y0 = intersection_point(self.x, self.y, self.alpha, x1, y1, alpha)
        self.d += f' Q {x0:.3f} {y0:.3f} {x1:.3f} {y1:.3f}'
        self.x, self.y, self.alpha = x1, y1, alpha

    def arc_to(self, p, r):
        self.x, self.y = p
        self.d += f' A {r:.3f} {r:.3f} 0 0 0 {self.x:.3f} {self.y:.3f}'

    def line_to(self, p):
        self.x, self.y = p
        self.d += f' L {self.x:.3f} {self.y:.3f}'

    def close(self):
        self.d += ' C'

if __name__ == "__main__":
    r = 20
    alpha = math.pi / 3
    p = (r * math.sin(alpha), r * math.cos(alpha))
    img = Image((150, 100), (50, 50))
    Circle(img.content, (0, 0), r)
    sym_stroke = { 'stroke': 'black', 'stroke-width': '0.2', 'stroke-dasharray': '2.0 0.90 0.2 0.90', 'stroke-dashoffset': '1.0'}
    Line(img.content, (-2 * r, 0), (2 * r, 0), sym_stroke)
    Line(img.content, (0, -2 * r), (0, 2 * r), sym_stroke)
    light_stroke = { 'stroke': 'black', 'stroke-width': '0.1' }
    Line(img.content, (0, 0), (2 * r * math.sin(alpha), 2 * r * math.cos(alpha)), light_stroke)
    Point(img.content, p, {'fill': 'red'})
    Line(img.content, (0, 0), p, { 'stroke': 'red'})
    Point(img.content, (0, 0))
    Text(img.content, (r * math.sin(alpha) / 2 - 1, r * math.cos(alpha) / 2), 'r', {'fill': 'red'})
    img.write('demo-image.svg')
