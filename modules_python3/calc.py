# importing libraries
import tkinter
import pandas
import numpy
import math


class Auxilliary:
    """ this class is host to funcitons which serve for auxilliary
    calculation in the analysis """
    def convert_to_vector(self, force: list) -> list:
        vec = []
        for i in range(len(force['name'])):
            x = math.cos(math.radians(
                force['angle[deg]'][i])) * force['force[N]'][i]
            y = math.sin(math.radians(
                force['angle[deg]'][i])) * force['force[N]'][i]
            vec.append((x, y))
        return vec

    def distance_from_centroid(self, cx: int, cy: int, x: int, y: int) -> int:
        dx, dy = abs(cx - x), abs(cy - y)
        return math.sqrt(dx**2 + dy**2)

    def zip_vectors(self, v1, v2) -> list:
        out = []
        for i in range(len(v1)):
            out.append([v1[i][0] + v2[i][0], v1[i][1] + v2[i][1]])
        return out

    def force_moment(self, c: int, force: list, vect: list) -> int:
        finMoment = 0
        xpos = force['x-pos[mm]']
        ypos = force['y-pos[mm]']
        for i in range(len(xpos)):
            # vector from centroid to the force point
            ri = numpy.array([xpos[i] - c[0], ypos[i] - c[1]])
            fi = numpy.array(vect[i])
            finMoment += numpy.cross(ri, fi)
        return finMoment

    def invert_vector(self, vect: list) -> list:
        for i in range(len(vect)):
            vect[i][0] *= -1
            vect[i][1] *= -1
        return vect


class Calculate:
    def __init__(self, err_lab: tkinter.Label, table) -> None:
        self.G_denom = 2.6  # denominator in calculation of G
        self.err_lab = err_lab

        # data provided by user
        self.bolt = table.bolt_info
        self.force = table.force_info

        self.aux = Auxilliary()

        # outputs of the data
        self.shear_load = []
        self.moment_load = []
        self.sum_load = []

    def shear_load_func(self, vect: list) -> list:
        # calulate sum of all fastener ares
        sA = 0
        out = []
        for i in range(len(self.bolt['name'])):
            Ai = self.bolt['diameter[mm]'][i]**2 * math.pi / 4
            Gi = self.bolt['E[MPa]'][i] / 2.6
            sA += Ai * Gi

        # final vector after adding all forces
        # for every bolt considers every force
        for i in range(len(self.bolt['name'])):
            finVec = [0, 0]
            for j in range(len(vect)):
                Gi = self.bolt['E[MPa]'][i] / 2.6
                Ai = self.bolt['diameter[mm]'][i]**2 * math.pi / 4
                finVec[0] += vect[j][0] * (Ai * Gi / sA)
                finVec[1] += vect[j][1] * (Ai * Gi / sA)
            out.append(finVec)
        return out

    def moment_load_func(self, c: int, vect: list,
                         moment_of_force: int) -> list:
        sA = 0
        out = []
        for i in range(len(self.bolt['name'])):
            Ai = self.bolt['diameter[mm]'][i]**2 * math.pi / 4
            Gi = self.bolt['E[MPa]'][i] / 2.6
            x, y = self.bolt['x-pos[mm]'][i], self.bolt['y-pos[mm]'][i]
            d = self.aux.distance_from_centroid(c[0], c[1], x, y)
            sA += Ai * Gi * d**2

        M = self.aux.force_moment(c, self.force, vect)
        M += moment_of_force

        for i in range(len(self.bolt['name'])):
            finVec = [0, 0]
            for j in range(len(vect)):
                Gi = self.bolt['E[MPa]'][i] / 2.6
                Ai = self.bolt['diameter[mm]'][i]**2 * math.pi / 4
                d = self.aux.distance_from_centroid(c[0], c[1], x, y)

                # this here needs to be done
                finVec[0] += M * (Ai * Gi * d / sA)
                finVec[1] += M * (Ai * Gi * d / sA)
                # this here needs to be done
            out.append(finVec)
        return out

    def calc_driver(self, centroid: list, force_moment: int) -> None:
        self.err_lab.config(text='')
        vect = self.aux.convert_to_vector(self.force)

        self.shear_load = self.aux.invert_vector(self.shear_load_func(vect))
        self.moment_load = self.aux.invert_vector(
            self.moment_load_func(centroid, vect, force_moment))
        self.sum_load = self.aux.zip_vectors(self.shear_load, self.moment_load)


class OutCalc:
    """ 
    method create_dataframe returns the dicionary needed for the output table
    other methods are used for evaluation of the results and auxiliary calculations
    """
    def __init__(self, calc, inpt, table) -> None:
        self.table = table
        self.calc = calc
        self.inpt = inpt
        self.bolts_num = len(self.table.bolt_info['name'])

    def calculate_tau(self, vect) -> list:
        out = []
        if vect[0] == '-':
            return ['-' for i in range(self.bolts_num)]
        d = self.table.bolt_info['diameter[mm]']
        for i in range(len(vect)):
            area = math.pi * d[i] / 4
            out.append(float(vect[i]) * area)
        return out

    def calculate_sigma(self, vect, t) -> list:
        if vect[0] == '-':
            return ['-' for i in range(self.bolts_num)]
        out = []
        d = self.table.bolt_info['diameter[mm]']
        for i in range(len(vect)):
            out.append(vect[i] / (d[i] * t[i]))
        return out

    def calculate_rfi(self, sigma, Fbry) -> list:
        if sigma[0] == '-':
            return ['-' for i in range(self.bolts_num)]
        out = []
        for sig in sigma:
            out.append(Fbry / sig)
        return out

    def calculate_rf(self, tau) -> list:
        if tau[0] == '-':
            return ['-' for i in range(self.bolts_num)]
        out = []
        rms = self.table.bolt_info['Rms[MPa]']
        for i in range(self.bolts_num):
            out.append(rms[i] / tau[i])
        return out

    def vect_to_size(self, vect) -> list:
        # takes vector and calculates its size
        if not vect:
            return ['-' for i in range(self.bolts_num)]
        return [
            math.sqrt(vect[i][0]**2 + vect[i][1]**2) for i in range(len(vect))
        ]

    def create_dataframe(self) -> pandas.DataFrame:
        tab_data = {}  # table data
        tab_data['ID Number'] = self.table.bolt_info['name']
        tab_data['d [mm]'] = self.table.bolt_info['diameter[mm]']
        tab_data['Fx [N]'] = [
            self.calc.sum_load[i][0] for i in range(len(self.calc.sum_load))
        ]
        tab_data['Fy [N]'] = [
            self.calc.sum_load[i][1] for i in range(len(self.calc.sum_load))
        ]
        tab_data['F [N]'] = self.vect_to_size(self.calc.sum_load)
        tab_data['τ [MPa]'] = self.calculate_tau(tab_data['F [N]'])
        tab_data['RF [-]'] = self.calculate_rf(tab_data['τ [MPa]'])
        tab_data['σ1 [MPa]'] = self.calculate_sigma(
            tab_data['F [N]'], self.table.bolt_info['t1[mm]'])
        tab_data['RF1 [-]'] = self.calculate_rfi(
            tab_data['σ1 [MPa]'], float(self.inpt.object1['Fbry[MPa]'].get()))
        tab_data['σ2 [MPa]'] = self.calculate_sigma(
            tab_data['F [N]'], self.table.bolt_info['t2[mm]'])
        tab_data['RF2 [-]'] = self.calculate_rfi(
            tab_data['σ2 [MPa]'], float(self.inpt.object2['Fbry[MPa]'].get()))

        df = pandas.DataFrame(data=tab_data)
        return df
