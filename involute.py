#!/usr/env python3

import math

def gamma(alpha):
    '''
    Calculates the angle _gamma_ of _alpha_
        Parameter:
            alpha: angle on the base circle
        Returns:
            involute angle _gamma_ 
    '''
    return alpha - math.atan(alpha)

def distance(alpha):
    '''
    Calculates the distance _s_ to the center of the base circle of an involute point corresponding to _alpha_
        Parameter:
            alpha: angle on the base circle
        Returns:
            distance _s_ of the involute point form the center of the base circle
    '''
    return math.sqrt(alpha ** 2 + 1)

def polar(alpha):
    '''
    Calculates the polar coordinates of an involute point (angle _gamma_ and the distance _s_ to the center of the base circle)
        Parameter:
            alpha: angle on the base circle
        Returns:
            involute angle _gamma_ 
            distance _s_ of the involute point form the center of the base circle
    '''
    return gamma(alpha), distance(alpha)

def inverse(s):
    '''
    Calculates _alpha_ so that _gamma(alpha)_ returns s.
    It is a kind of inverse involute funktion.
        Parameter:
            s: distance of the involute point from the center of the base circle
        Returns:
            alpha: angle that the involute function needs to calculate (gamma, s)
    '''
    return math.sqrt(s ** 2 - 1)

def polar2xy(r, alpha):
    return r * math.sin(alpha), r * math.cos(alpha)

def point(r, alpha, offset = 0):
    gamma, s = polar(alpha)
    return polar2xy(r * s, gamma + offset)

def points(r, alpha, offset, n):
    '''calulate _n_ points of an involute of base circle wiht radius _r_ up to an involute angle _alpha_'''
    result = []
    for i in range(n + 1):
        result.append(point(r, i * alpha / n, offset))
    return result

def path(r, alpha, offset, n):
    d = ''
    cmd = "M"
    for x,y in points(r, alpha, offset, n):
        d += f'{cmd} {x} {y}'
        cmd = ' L'
    return d

if __name__ == "__main__":
    r = 20
    n = 60
    m = 4
    print( '<svg width="200mm" height="200mm" viewBox="-100 -100 200 200" xmlns="http://www.w3.org/2000/svg" version="1.1" baseProfile="full">')
    for i in range(0, m):
        print(f'    <path d="{path(r, math.pi, i * 2 * math.pi / m, n)}" stroke="black" fill="none" stroke-width="0.2"/>')
    print(f'    <circle r="{r}" fill="blue" stroke="black" stroke-width="0.2"/>')
    print( '</svg>')
