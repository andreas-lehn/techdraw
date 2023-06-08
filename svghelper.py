#!/usr/env python3

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

class Element(etree.Element):
    def __init__(self, parent, tag, *attr_list):
        attributes = dict()
        for attrs in attr_list: attributes.update(attrs)
        super().__init__(tag, attributes)
        parent.append(self)

def merge_attributes(*attr_list):
        result = dict()
        for attrs in attr_list: result.update(attrs)
        return result

def str(f):
    return f'{f:.3f}'

def normalize(p):
    x, y = p
    l = math.sqrt(x ** 2, y ** 2)
    return x / l, y / l

def Line(parent, p1, p2, *user_attrs):
    x1, y1 = p1
    x2, y2 = p2
    return etree.SubElement(parent, 'line', merge_attributes({ 'x1': str(x1), 'y1': str(y1), 'x2': str(x2), 'y2': str(y2) }, mid_stroke, *user_attrs))

def Circle(parent, center, radius, *user_attrs):
    cx, cy = center
    return etree.SubElement(parent, 'circle', merge_attributes({ 'cx': str(cx), 'cy': str(cy), 'r': str(radius) }, thick_stroke, *user_attrs))

def Point(parent, p, *user_attrs):
    cx, cy = p
    return etree.SubElement(parent, 'circle', merge_attributes({'cx': str(cx), 'cy': str(cy), 'r': '0.5', 'fill': 'black'}, *user_attrs))

def Path(parent, d, *user_attrs):
    return etree.SubElement(parent, 'path', merge_attributes({'d': d}, thick_stroke, *user_attrs))

def Translation(parent, origin, *attrs):
    tx, ty = origin
    return etree.SubElement(parent, 'g', merge_attributes({'transform': f'translate({str(tx)} {str(ty)})'}, *attrs))

def Rotation(parent, rotation, *attrs):
    rotation = -180 * rotation / math.pi
    return etree.SubElement(parent, 'g', merge_attributes({'transform': f'rotate({str(rotation)})'}, *attrs))

def Text(parent, pos, text, rotation = 0, *attrs):
    x, y = pos
    rotation = -180 * rotation / math.pi
    g = etree.SubElement(parent, 'g', {'transform': f'translate({str(x)} {str(y)}) rotate({str(rotation)})'})
    t = etree.SubElement(g, 'text', merge_attributes({'transform': 'scale(0.25, -0.25)', 'fill': 'black', 'stroke': 'none'}, *attrs))
    t.text = text
    return g

def angle(p):
    p = np.array(p)
    return np.arccos(np.dot(np.array([0, 1]), p) / np.sqrt((p * p).sum()))

def LineLabel(parent, p1, p2, text, pos = 0.5, offset = 0.5, *attrs):
    p1, p2, offset = np.array(p1), np.array(p2), np.array(offset)
    x, y = p1 + (p2 - p1) * pos
    alpha = -180 * (angle(p2 - p1) - math.pi / 2) / math.pi
    g = etree.SubElement(parent, 'g', {'transform': f'translate({str(x)} {str(y)}) rotate({str(alpha)})'})
    t = etree.SubElement(g, 'text', merge_attributes({'transform': f'translate(0 {str(offset)}) scale(0.25, -0.25)', 'fill': 'black', 'stroke': 'none'}, *attrs))
    t.text = text
    return g

def Arc(parent, p, q, r, *attrs):
    return Path(parent, PathCreator(p).arc_to(q, r), merge_attributes({ 'fill': 'none' }, *attrs))

def ArcLabel(parent, p, r, alpha, text, *attrs):
    x, y = p
    g = etree.SubElement(parent, 'g', {'transform': f'translate({str(x + r * math.sin(alpha))} {str(y + r * math.cos(alpha))}) rotate({str(-180 * alpha / math.pi)})'})
    t = etree.SubElement(g, 'text', merge_attributes({'transform': 'scale(0.25, -0.25)', 'fill': 'black', 'stroke': 'none'}, *attrs))
    t.text = text
    return g

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

if __name__ == "__main__":
    r = 20
    
    alpha = math.pi / 3
    beta  = math.pi - math.pi / 6
    gamma = -math.pi / 6
    delta = math.pi / 2

    p = np.array([r * math.sin(alpha), r * math.cos(alpha)])
    q = np.array([r * math.sin(beta),  r * math.cos(beta)])
    s = np.array([r * math.sin(gamma), r * math.cos(gamma)])
    t = np.array([r * math.sin(delta), r * math.cos(delta)])

    img = Image((150, 100), (50, 50))
    Circle(img.content, (0, 0), r)
    Line(img.content, (-2 * r, 0), (2 * r, 0), sym_stroke)
    Line(img.content, (0, -2 * r), (0, 2 * r), sym_stroke)
    Line(img.content, (0, 0), (2 * r * math.sin(alpha), 2 * r * math.cos(alpha)), thin_stroke)
    Point(img.content, p, {'fill': 'red'})
    Line(img.content, (0, 0), p, { 'stroke': 'red'})
    Point(img.content, (0, 0))
    LineLabel(img.content, (0, 0), p, 'r', 0.6, 0.5, {'fill': 'red'})
    Path(img.content, PathCreator(t).line_to(q, s, t), {'fill' : 'none'}, thin_stroke)
    Arc(img.content, (0, 1.5 * r), 1.5 * p, 1.5 * r, thin_stroke)
    ArcLabel(img.content, (0, 0), 1.5 * r + 0.5, 0.5 * alpha, u'\u03B1')
    img.write('demo-image.svg')
