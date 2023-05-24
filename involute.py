#!/usr/env python3

import math
import svghelper as svg

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

def path(r, alpha, offset, n):
    p = svg.Path(point(r, 0, offset), alpha)
    for i in range(n):
        beta = (i + 1) * alpha / n
        p.lineTo(point(r, beta, offset))
    return p.d

if __name__ == "__main__":
    r = 20
    n = 60
    m = 1
    alpha = 60 * math.pi / 180
    print( '<svg width="150mm" height="100mm" viewBox="-50 -50 150 100" xmlns="http://www.w3.org/2000/svg" version="1.1" baseProfile="full">')
    print( '    <style>')
    print( '        .base      { fill: lightgrey; stroke: black; stroke-width: 0.2}')
    print( '        .involute  { fill: none; stroke: black; stroke-width: 0.2}')
    print( '        .arcline   { fill: none; stroke: red;   stroke-width: 0.2}')
    print( '        .radius    { fill: none; stroke: black;   stroke-width: 0.2}')
    print( '        .s         { fill: none; stroke: blue;   stroke-width: 0.2}')
    print( '        .helpline  { fill: none; stroke: black; stroke-width: 0.05; stroke-dasharray: 1 0.8 }')
    print( '        .dotline   { fill: none; stroke: black; stroke-width: 0.05 }')
    print( '        .symline   { fill: none; stroke: black; stroke-width: 0.1; stroke-dasharray: 2.0 0.8 0.1 0.8; stroke-dashoffset: -1.0 }')
    print( '    </style>')
    print( '    <g transform="scale(1 -1)">')
    for i in range(0, m): print(f'        <path class="involute" d="{path(r, math.pi, i * 2 * math.pi / m, n)}"/>')
    print(f'        <circle class="base" r="{r}"/>')
    print(f'        <circle r="0.4" fill="black"/>')
    print(f'        <line class="symline" x1="{r * 2}" x2="{-r * 2}"/>')
    print(f'        <line class="symline" y1="{r * 2}" y2="{-r * 2}"/>')
    x1, y1 = polar2xy(r * 2, alpha)
    print(f'        <line class="dotline" x1="{x1}" y1="{y1}"/>')
    x1, y1 = polar2xy(r * 2, gamma(alpha))
    print(f'        <line class="dotline" x1="{x1}" y1="{y1}"/>')
    px, py = point(r, alpha)
    print(f'        <circle cx="{px}" cy="{py}" r="0.4" fill="black"/>')
    qx, qy = polar2xy(r, alpha)
    print(f'        <circle cx="{qx}" cy="{qy}" r="0.4" fill="black"/>')
    dx, dy = qx - px, qy - py
    print(f'        <line class="dotline" x1="{px - dx / 2}" y1="{py - dy / 2}" x2="{qx + dx / 2}" y2="{qy + dy / 2}"/>')
    print(f'        <line class="dotline" x1="{px - dy}" y1="{py + dx}" x2="{px + dy}" y2="{py - dx}"/>')
    print(f'        <line class="arcline" x1="{px}" y1="{py}" x2="{qx}" y2="{qy}"/>')
    print(f'        <g transform="translate({(px + qx) * 0.5} {(py + qy) * 0.5})"><text transform="scale(0.25 -0.25)" fill="red">&#x03B1;</text></g>')
    print(f'        <path class="arcline" d="M 0 {r} A {r} {r} 0 0 0 {qx} {qy}"/>')
    print(f'        <line class="radius"  x2="{qx}" y2="{qy}"/>')
    print(f'        <g transform="translate({qx * 0.6} {qy * 0.6 + 1})"><text transform="scale(0.25 -0.25)" fill="black">r</text></g>')
    print(f'        <line class="s"       x1="{px}" y1="{py}"/>')
    print(f'        <g transform="translate({px * 0.8 - 2} {py * 0.8})"><text transform="scale(0.25 -0.25)" fill="blue">s</text></g>')
    beta = 0 # math.pi / 36
    ra = 10
    ax, ay = polar2xy(ra, -beta)
    bx, by = polar2xy(ra, gamma(alpha) + beta)
    print(f'        <path stroke="blue" stroke-width="0.1" fill="none" d="M {ax} {ay} A {ra} {ra} 0 0 0 {bx} {by}"/>')
    print(f'        <g transform="translate({0.0} {ra + 1})"><text transform="scale(0.25 -0.25)" fill="blue">&#x03B3;</text></g>')
    ra = 5
    ax, ay = polar2xy(ra, -beta)
    bx, by = polar2xy(ra, alpha + beta)
    print(f'        <path stroke="red" stroke-width="0.1" fill="none" d="M {ax} {ay} A {ra} {ra} 0 0 0 {bx} {by}"/>')
    print(f'        <g transform="translate({ra - 2} {ra - 1})"><text transform="scale(0.25 -0.25)" fill="red">&#x03B1;</text></g>')

    l = math.sqrt(dx ** 2 + dy ** 2)
    dx, dy = dx / l * ra, dy / l * ra
    c = math.sqrt(2) * 2
    print(f'        <path class="dotline" d="M {px - dy} {py + dx} A {ra} {ra} 0 0 0 {px + dx} {py + dy}"/>')
    print(f'        <circle cx="{px + (dx - dy) / c}" cy="{py + (dy + dx) / c}" r="0.25" fill="black"/>')
    print(f'        <path class="dotline" d="M {qx - dy} {qy + dx} A {ra} {ra} 0 0 1 {qx - dx} {qy - dy}"/>')
    print(f'        <circle cx="{qx - (dy + dx) / c}" cy="{qy + (dx - dy) / c}" r="0.25" fill="black"/>')
    print( '    </g>')
    print( '</svg>')
