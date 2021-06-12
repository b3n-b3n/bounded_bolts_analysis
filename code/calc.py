# importing libraries
import numpy
import math

# importing local files
import input_interface
import scheme

class Auxilliary:
    """ this class is host to funcitons which serve for auxilliary
    calculation in the analysis """
    def convert_to_vector(self, force):
        vec = []
        for i in range(len(force['name'])):
            x = math.cos(math.radians(force['angle[deg]'][i])) * force['size[N]'][i]
            y = math.sin(math.radians(force['angle[deg]'][i])) * force['size[N]'][i]
            vec.append((x,y))
        return vec

    def distance_from_centroid(self, cx, cy, x, y):
        dx, dy = abs(cx - x), abs(cy - y)
        return math.sqrt(dx**2 + dy**2)

    def zip_vectors(self, v1, v2):
        return [v1[0]+v2[0], v1[1]+v2[1]]

    def force_moment(self, c, force, vect):
        finMoment = 0
        xpos = force['x-pos[mm]']
        ypos = force['y-pos[mm]']
        for i in range(len(xpos)):
            # vector from centroid to the force point
            ri = numpy.array([xpos[i]-c[0], ypos[i]-c[1]])
            fi = numpy.array(vect[i])
            finMoment += numpy.cross(ri, fi)
        return finMoment


class Calculate:
    def __init__(self, err_lab, inpt):
        self.G_denom = 2.6  # denominator in calculation of G
        self.err_lab = err_lab
        
        # data provided by user
        self.bolt = inpt.bolt_info
        self.force = inpt.force_info
        
        # resulting vectors
        self.res_vect = {}
        self.res_vect['load_vector'] = []
        self.res_vect['load-moment_vector'] = []

        self.aux = Auxilliary()


    def shear_load(self, vect):
        # calulate sum of all fastener ares
        sA = 0
        for i in range(len(self.bolt['name'])):
            Ai = self.bolt['diameter[mm]'][i]**2*math.pi / 4
            Gi = self.bolt['E[MPa]'][i]/2.6
            sA += Ai*Gi

        # final vector after adding all forces
        # for every bolt considers every force
        for i in range(len(self.bolt['name'])):
            finVec = [0,0]
            for j in range(len(vect)):
                Gi = self.bolt['E[MPa]'][i]/2.6
                Ai = self.bolt['diameter[mm]'][i]**2*math.pi / 4
                finVec[0] += vect[j][0]*(Ai*Gi / sA)
                finVec[1] += vect[j][1]*(Ai*Gi / sA)
            
            # convert result to reaction force
            finVec[0] *= -1
            finVec[1] *= -1
            self.res_vect['load_vector'].append(finVec)


    def shear_load_moment(self, c, vect, moment_of_force):
        sA = 0 
        for i in range(len(self.bolt['name'])):
            Ai = self.bolt['diameter[mm]'][i]**2*math.pi / 4
            Gi = self.bolt['E[MPa]'][i]/2.6
            x, y = self.bolt['x-pos[mm]'][i], self.bolt['y-pos[mm]'][i]
            d = self.aux.distance_from_centroid(c[0], c[1], x, y)
            sA += Ai* Gi * d**2    
        
        M = self.aux.force_moment(c, self.force, vect)
        M += moment_of_force

        for i in range(len(self.bolt['name'])):
            finVec = [0,0]
            for j in range(len(vect)):
                Gi = self.bolt['E[MPa]'][i]/2.6
                Ai = self.bolt['diameter[mm]'][i]**2*math.pi / 4
                d = self.aux.distance_from_centroid(c[0], c[1], x, y)

                # this here needs to be done
                finVec[0] += M*(Ai*Gi*d / sA)
                finVec[1] += M*(Ai*Gi*d / sA)
                # this here needs to be done
            
            # convert result to reaction force
            finVec[0] *= -1
            finVec[1] *= -1
            self.res_vect['load_vector'].append(finVec)
           

    def sum_resulting_vectors(self):
        pass

    def calc_driver(self, centroid, force_moment):
        self.err_lab.config(text='')
        vect = self.aux.convert_to_vector(self.force)

        self.shear_load(vect)
        self.shear_load_moment(centroid, vect, force_moment)

        # return self.aux.zip_vectors(self.res_vect['load_vector'],  self.res_vect['load-moment_vector'])
        return self.res_vect['load-moment_vector']
        # tato funkcia vrati vysledny vektor do main s čoho sa to
        # potom prekreslí v sketchi

