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

def distance(alpha):
    '''
    Calculates the distance _s_ to the center of the base circle with radius 1 of an involute point corresponding to _alpha_
        Parameter:
            alpha: angle on the base circle
        Returns:
            distance _s_ of the involute point form the center of the base circle
    '''
    return math.sqrt(alpha ** 2 + 1)

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
    return np.array([gamma(alpha), r * distance(alpha)])

def inverse(s):
    '''
    Calculates _alpha_ so that _distance(alpha)_ returns s.

    It is a kind of inverse involute funktion.
        Parameter:
            s: distance of the involute point from the center of the base circle
        Returns:
            alpha: angle that the involute function needs to calculate (gamma, s)
    '''
    return math.sqrt(s ** 2 - 1)

def point(r, alpha, offset = 0):
    gamma, s = point_polar(r, alpha)
    return s * np.array([math.sin(gamma + offset), math.cos(gamma + offset)])

def points(r, alpha, offset, n):
    alpha = alpha / n
    result = []
    for i in range(n):
        result.append(point(r, (i + 1) * alpha, offset))
    return result
