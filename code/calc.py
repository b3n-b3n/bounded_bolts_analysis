# importing libraries
import math

# importing local files
import input_interface
import scheme

class Vectors:
    def convert_to_vector(self, force):
        vec = []
        for i in range(len(force['name'])):
            x = force['size[N]'][i] / math.cos(force['angle[deg]'])
            y = force['size[N]'][i] / math.sin(force['angle[deg]'])
            vec.append((x,y))
        return vec

class Calculate:
    def __init__(self, err_lab, inpt):
        self.G_denom = 2.6  # denominator in calculation of G
        self.err_lab = err_lab
        
        # data provided by user
        self.bolt = inpt.bolt_info
        self.force = inpt.force_info
        
        # resulting vectors
        self.res_vec = {}
        self.res_vec['load_vector'] = []
        self.res_vec['load-moment_vector'] = []
    

    def draw_resulting_vectors(self):
        pass

    def shear_load(self, vect):
        # calulate sum of all fastener ares
        sA = 0
        for i in range(len(self.bolt['name'])):
            Ai = self.bolt['diameter[mm]'][i]**2*math.pi / 4
            Gi = self.bolt['E[MPa]'][i]/2.6
            sA += Ai*Gi

        # final vector after adding all forces
        for i in range(len(self.bolt['name'])):
            finVec = [0,0]
            for j in range(len(vect)):
                Gi = self.bolt['E[MPa]'][i]/2.6
                Ai = self.bolt['diameter[mm]'][i]**2*math.pi / 4
                finVec[0] += vect[j][0]*(Ai*Gi / sA)
                finVec[1] = vect[j][1]*(Ai*Gi / sA)
            self.res_vec['load_vector'].append(finVec)


    def shear_load_moment(self):
        pass

    def calc_driver(self, centroid):
        self.err_lab.config(text='')
        vect = Vectors().convert_to_vector(self.force)


