# importing libraries
import pandas
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
            x = math.cos(math.radians(force['angle[deg]'][i])) * force['force[N]'][i]
            y = math.sin(math.radians(force['angle[deg]'][i])) * force['force[N]'][i]
            vec.append((x,y))
        return vec

    def distance_from_centroid(self, cx, cy, x, y):
        dx, dy = abs(cx - x), abs(cy - y)
        return math.sqrt(dx**2 + dy**2)

    def zip_vectors(self, v1, v2):
        for i in range(len(v1)):
            v1[i][0] += v2[i][0]
            v1[i][1] += v2[i][1]
        return v1

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

    def invert_vector(self, vect):
        for i in range(len(vect)):
            vect[i][0] *= -1 
            vect[i][1] *= -1
        return vect

class Calculate:
    def __init__(self, err_lab, inpt):
        self.G_denom = 2.6  # denominator in calculation of G
        self.err_lab = err_lab
        
        # data provided by user
        self.bolt = inpt.bolt_info
        self.force = inpt.force_info

        self.aux = Auxilliary()
        
        # outputs of the data
        self.shear_load = []
        self.moment_load = []
        self.sum_load = []

    def shear_load_func(self, vect):
        # calulate sum of all fastener ares
        sA = 0
        out = []
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
            out.append(finVec)
        return out


    def moment_load_func(self, c, vect, moment_of_force):
        sA = 0
        out = []
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
            out.append(finVec)
        return out
           

    def sum_resulting_vectors(self):
        pass

    def calc_driver(self, centroid, force_moment):
        self.err_lab.config(text='')
        vect = self.aux.convert_to_vector(self.force)
        calc_out = {}

        self.shear_load = self.aux.invert_vector(self.shear_load_func(vect))
        self.moment_load = self.aux.invert_vector(self.moment_load_func(centroid, vect, force_moment))
        self.sum_load = self.aux.zip_vectors(self.shear_load, self.moment_load)


class OutCalc:
    def __init__(self, calc, inpt):
        self.inpt = inpt
        self.calc = calc
        self.bolts_num = len(self.inpt.bolt_info['name'])
        self.round_to = 3


    def calculate_tau(self, vect):
        out = []
        if vect[0] == '-': return ['-' for i in range(self.bolts_num)]
        
        d = self.inpt.bolt_info['diameter[mm]']
        for i in range(len(vect)):
            area = math.pi*d[i] / 4
            out.append(round(float(vect[i])*area, self.round_to))
        return out


    def calculate_sigma(self, vect, t):
        if vect[0] == '-': return ['-' for i in range(self.bolts_num)]
        out = []
        d = self.inpt.bolt_info['diameter[mm]']
        for i in range(len(vect)):
            out.append(round(vect[i] / (d[i]*t[i]), self.round_to))
        return out


    def calculate_rf(self, tau):
        if tau[0] == '-': return ['-' for i in range(self.bolts_num)]
        out = []
        rm = self.inpt.bolt_info['Rm[MPa]']
        for i in range(self.bolts_num): 
            out.append(round(rm[i]/2/tau[i], self.round_to))
        return out

    def vect_to_size(self, vect):
        # takes vector and calculates its size
        if not vect: return ['-' for i in range(self.bolts_num)]
        return [round(math.sqrt(vect[i][0]**2 + vect[i][1]**2), self.round_to) for i in range(len(vect))] 


    def create_dataframe(self):
        tab_data = {}  # table data
        tab_data['name'] = self.inpt.bolt_info['name']
        tab_data['d[mm]'] = self.inpt.bolt_info['diameter[mm]']
        tab_data['Fs[N]'] = self.vect_to_size(self.calc.shear_load)
        tab_data['Fm[N]'] = self.vect_to_size(self.calc.moment_load)
        tab_data['F[N]'] = self.vect_to_size(self.calc.sum_load)
        tab_data['Tau[MPa]'] = self.calculate_tau(tab_data['F[N]'])
        tab_data['RF-0'] = self.calculate_rf(tab_data['Tau[MPa]'])
        tab_data['Sigma_1[MPa]'] = self.calculate_sigma(tab_data['F[N]'], self.inpt.bolt_info['t1[mm]'])
        tab_data['Sigma_2[MPa]'] = self.calculate_sigma(tab_data['F[N]'], self.inpt.bolt_info['t2[mm]'])
        tab_data['RF-1'] = ['-' for i in range(self.bolts_num)]
        tab_data['RF-2'] = ['-' for i in range(self.bolts_num)]

        df = pandas.DataFrame(data=tab_data)
        print(df)
        return df
