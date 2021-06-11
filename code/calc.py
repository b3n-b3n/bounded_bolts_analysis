# importing libraries
import math

# importing local files
import input_interface
import scheme

class Vectors:
    def convert_to_vector(self, force):
        vec = []
        for i in range(len(force['name'])):
            x = math.cos(math.radians(force['angle[deg]'][i])) * force['size[N]'][i]
            y = math.sin(math.radians(force['angle[deg]'][i])) * force['size[N]'][i]
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
        self.res_vect = {}
        self.res_vect['load_vector'] = []
        self.res_vect['load-moment_vector'] = []
    

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
        # for every bolt considers every force
        for i in range(len(self.bolt['name'])):
            finVec = [0,0]
            for j in range(len(vect)):
                Gi = self.bolt['E[MPa]'][i]/2.6
                Ai = self.bolt['diameter[mm]'][i]**2*math.pi / 4
                finVec[0] += vect[j][0]*(Ai*Gi / sA)
                finVec[1] = vect[j][1]*(Ai*Gi / sA)
            
            # convert result to reaction force
            finVec[0] *= -1
            finVec[1] *= -1
            self.res_vect['load_vector'].append(finVec)


    def shear_load_moment(self):
        # nezabudni to tu prenásobiť -1 pretože ide o reakčný vektor
        pass

    def sum_resulting_vectors(self):
        pass

    def calc_driver(self, centroid):
        self.err_lab.config(text='')
        vect = Vectors().convert_to_vector(self.force)

        self.shear_load(vect)
        self.shear_load_moment()
        # potom treba výsledné vektory sčítať

        self.sum_resulting_vectors()

        return self.res_vect['load_vector'] 
        # tato funkcia vrati vysledny vektor do main s čoho sa to
        # potom prekreslí v sketchi

