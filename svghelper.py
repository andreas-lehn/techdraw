#!/usr/env python3

import math
import numpy as np

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

class Path:

    def __init__(self, p, alpha):
        self.x, self.y = p
        self.alpha = alpha
        self.d = f'M {self.x:.3f} {self.y:.3f}'

    def bezierTo(self, p, alpha):
        x1, y1 = p
        x0, y0 = intersection_point(self.x, self.y, self.alpha, x1, y1, alpha)
        self.d += f' Q {x0:.3f} {y0:.3f} {x1:.3f} {y1:.3f}'
        self.x, self.y, self.alpha = x1, y1, alpha

    def arcTo(self, p, r):
        self.x, self.y = p
        self.d += f' A {r:.3f} {r:.3f} 0 0 0 {self.x:.3f} {self.y:.3f}'

    def close(self):
        self.d += ' C'
