import math
import numpy as np

def gamma(alpha):
    '''
    Calculates the angle _gamma_ of _alpha_
        Parameter:
            alpha: angle on the base circle
        Returns:
            involute angle _gamma_ 
    '''
    return alpha - math.atan(alpha)

def distance(r, alpha):
    '''
    Calculates the distance _s_ to the center of the base circle with radius 1 of an involute point corresponding to _alpha_
        Parameter:
            r:     radius of the base circle
            alpha: angle on the base circle
        Returns:
            distance _s_ of the involute point form the center of the base circle
    '''
    return r * math.sqrt(alpha ** 2 + 1)

def point_polar(r, alpha):
    '''
    Calculates the polar coordinates of an involute point (angle _gamma_ and the distance _s_ to the center of the base circle)
        Parameter:
            r: radius of the base circle
            alpha: angle on the base circle
        Returns:
            involute angle _gamma_ 
            distance _s_ of the involute point form the center of the base circle
    '''
    return distance(r, alpha), gamma(alpha)

def inverse(r, s):
    '''
    Calculates _alpha_ so that _distance(r, alpha)_ returns s.

    It is a kind of inverse involute funktion.
        Parameter:
            s: distance of the involute point from the center of the base circle
        Returns:
            alpha: angle that the involute function needs to calculate (gamma, s)
    '''
    return math.sqrt((s / r) ** 2 - 1)

def point(r, alpha, offset = 0):
    s, beta = point_polar(r, alpha)
    return s * np.array([np.cos(beta + offset), np.sin(beta + offset)])

def points(r, alpha, offset, n):
    alpha = alpha / n
    return [point(r, (i + 1) * alpha, offset) for i in range(n)]
