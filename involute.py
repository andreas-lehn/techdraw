#!/usr/env python3

import gearwheel
import math

def involute_points(r, alpha, offset, n):
    '''calulate _n_ points of an involute of base circle wiht radius _r_ up to an involute angle _alpha_'''
    result = []
    for i in range(n + 1):
        gamma, l = gearwheel.involute(i * alpha / n)
        result.append(gearwheel.polar2xy(l * r, gamma + offset))
    return result

def involute_path(r, alpha, offset, n):
    d = ''
    cmd = "M"
    points = involute_points(r, alpha, offset, n)
    for x,y in points:
        d += f'{cmd} {x} {y}'
        cmd = ' L'
    return d

if __name__ == "__main__":
    r = 1
    n = 60
    m = 6
    print( '<svg width="20cm" height="20cm" viewBox="-10 -10 20 20" xmlns="http://www.w3.org/2000/svg" version="1.1" baseProfile="full">')
    for i in range(0, m):
        print(f'    <path id="involute" d="{involute_path(r, 2 * math.pi, i * 2 * math.pi / m, n)}" stroke="black" fill="none" stroke-width="0.05"/>')
    print(f'    <circle r="{r}" fill="yellow" stroke="black" stroke-width="0.05"/>')
    print( '</svg>')
