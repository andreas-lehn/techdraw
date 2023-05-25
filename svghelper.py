#!/usr/env python3

import math
import numpy as np
import xml.etree.ElementTree as etree

class Image(etree.Element):

    def __init__(self, size, center, attrib = {}):
        w, h = size
        cx, cy = center
        attrib.update({'width': f'{w}mm', 'height': f'{h}mm', 'viewBox': f'{-cx} {-cy} {w} {h}', 'xmlns': 'http://www.w3.org/2000/svg', 'version': '1.1'})
        super().__init__('svg', attrib)
        self.style = etree.SubElement(self, 'style')
        self.content = etree.SubElement(self, 'g', {'transform': 'scale(1, -1)'})

    def write(self, file):
        tree = etree.ElementTree(self)
        tree.write(file)
        

class Element(etree.Element):

    def __init__(self, parent, tag, attrib = {}):
        super().__init__(tag, attrib)
        parent.append(self)

def str(f):
    return f'{f:.3f}'

class Line(Element):

    def __init__(self, parent, p1, p2, attrib = {}):
        x1, y1 = p1
        x2, y2 = p2
        attrib.update({'x1': str(x1), 'y1': str(y1), 'x2': str(x2), 'y2': str(y2)})
        super().__init__(parent, 'line', attrib)

class Circle(Element):

    def __init__(self, parent, c, r, attrib = {}):
        cx, cy = c
        attrib.update({'cx': str(cx), 'cy': str(cy), 'r': str(r)})
        super().__init__(parent, 'circle', attrib)

class Point(Element):
    
    def __init__(self, parent, c, attrib = {}):
        cx, cy = c
        attrib.update({'cx': str(cx), 'cy': str(cy), 'r': '0.5'})
        super().__init__(parent, 'circle', attrib)


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
    M = (0, 0)
    r = 20
    alpha = math.pi / 3
    P = (r * math.sin(alpha), r * math.cos(alpha))
    img = Image((150, 100), (50, 50))
    base_circle = Circle(img.content, M, r, { 'fill': 'lightgrey', 'stroke': 'black', 'stroke-width': '0.35'})
    m_point = Point(img.content, M, {'fill': 'black'})
    p_point = Point(img.content, P, {'fill': 'black'})
    h_sym_line = Line(img.content, (-2 * r, 0), (2 * r, 0), { 'stroke': 'black', 'stroke-width': '0.2', 'stroke-dasharray': '2.1 0.8 0.2 0.8'})
    v_sym_line = Line(img.content, (0, -2 * r), (0, 2 * r), { 'stroke': 'black', 'stroke-width': '0.2', 'stroke-dasharray': '2.1 0.8 0.2 0.8'})
    img.write('demo-image.svg')
