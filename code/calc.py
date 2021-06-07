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
        
        self.bolt = inpt.bolt_info
        self.bolt['load_vector'] = []
        self.bolt['load-moment_vector'] = []
        self.force = inpt.force_info


    
    
    def draw_resulting_vectors(self):
        pass

    def shear_load(self):
        # calulate sum of all fastener ares
        sA = 0
        for i in range(len(self.bolt['name'])):
            Ai = self.bolt['diameter[mm]'][i]**2*math.pi / 4
            Gi = self.bolt['E[MPa]'][i]
            sA += Ai*Gi

        # final vector after adding all forces
        finVec = [0,0]
        for i in range(len(self.force['name'])):
            pass


    def shear_load_moment(self):
        pass

    def calc_driver(self, centroid):
        self.err_lab.config(text='')
        vec = Vectors().convert_to_vector(self.force)

