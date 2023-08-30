
import math
import techdraw.involute as involute
import techdraw as svg

class GearWheel:
    ''' Involute gear wheel'''

    def __init__(self, modul, n_teeth, alpha = 20 * math.pi / 180):
        self.modul = modul
        self.n_teeth = n_teeth
        self.alpha = alpha

    def r_0(self):
        '''returns the radius of the gear wheel (Teilkreisradius)'''
        return self.modul * self.n_teeth / 2

    def r_head(self):
        '''returns the radius of the tooth heads (Kopfkreisradius)'''
        return self.r_0() + self.modul

    def r_foot(self):
        '''returns the radius of the tooth foot (Fußkreisradius)'''
        C = 0.167 # Magische Konstante, siehe: https://www.tec-science.com/de/getriebe-technik/evolventenverzahnung/evolventen-zahnrad-geometrie/
        return min(self.r_0() - self.modul, self.r_base()) - C * self.modul

    def r_base(self):
        '''returns the radius of the base circle'''
        return self.r_0() * math.cos(self.alpha)

    def tau(self):
        '''returns the angle between two teeth'''
        return 2 * math.pi / self.n_teeth

    def beta_0(self):
        '''returns the angle offsets of the intesection of the tooth with the Teilkreis'''
        return self.tau() / 4

    def beta(self):
        '''returns the angle offsets of the tooth base point'''
        return self.beta_0() + involute.gamma(self.alpha)

    def gamma(self):
        '''returns the angle offsets of the tooths head point'''
        return self.beta() - involute.gamma(involute.inverse(self.r_base(), self.r_head()))

    def tooth_ctrl_points(self):
        '''returns the controls points of a tooth
         
        The control points are returned as an array of tupels (r, phi, tangent),
        starting from the head point to the foot point.
        
        r, phi:  polar coordinates of the control point
        tangent: tangent of the tooth in that control point
        '''

        r_0, r_h, r_b, r_f = self.r_0(), self.r_head(), self.r_base(), self.r_foot()
        b_0, b_h, b_b, b_f = self.beta_0(), self.gamma(), self.beta(), self.tau() / 2

        return [(r_h, b_h, b_h - involute.inverse(r_b, r_h)),
                (r_0, b_0, b_0 - self.alpha),
                (r_b, b_b, b_b),
                (r_f, b_f, b_f + math.pi /2)]

    def svg_path(self):
        r_0, r_h, r_b, r_f = self.r_0(), self.r_head(), self.r_base(), self.r_foot()
        b_0, b_h, b_b, b_f = self.beta_0(), self.gamma(), self.beta(), self.tau() / 2

        path = svg.PathCreator(svg.pol2cart(r_f, -b_f), -b_f / 2 + math.pi/2)
        for i in range(self.n_teeth):
            offset = i * self.tau()
            path.curve_to(svg.pol2cart(r_b, offset - b_b), offset - b_b)
            path.curve_to(svg.pol2cart(r_0, offset - b_0), offset - b_0 + self.alpha)
            path.curve_to(svg.pol2cart(r_h, offset - b_h), offset - b_h + involute.inverse(r_b, r_h))
            path.alpha = offset - b_h + math.pi/2
            path.arc_to_line(svg.pol2cart(r_h, offset + b_h), offset + b_h + math.pi/2)
            path.alpha = offset + b_h - involute.inverse(r_b, r_h)
            path.curve_to(svg.pol2cart(r_0, offset + b_0), offset + b_0 - self.alpha)
            path.curve_to(svg.pol2cart(r_b, offset + b_b), offset + b_b)
            path.curve_to(svg.pol2cart(r_f, offset + b_f), offset + b_f + math.pi/2)
        path.close()
        return path.path
