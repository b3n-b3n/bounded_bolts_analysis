import tkinter
import numpy
import math
import copy

class Geometry:
    def __init__(self):
        pass

    def normalize_coordiantes(self, bolt, force, centroid):
        pos_bolt = numpy.array([bolt["x-pos[mm]"], bolt["y-pos[mm]"]], dtype=numpy.float64)
        pos_force = numpy.array([force["x-pos[mm]"], force["y-pos[mm]"]], dtype=numpy.float64)
        diameter = numpy.array(bolt["diameter[mm]"], dtype=numpy.float64)
        centroid = numpy.array(centroid, dtype=numpy.float64)
        
        merged = pos_bolt + pos_force
        print(merged)
        mi, ma = numpy.min(merged), numpy.max(merged)
        # if mi == ma:
        #     pos_bolt[i] = [0.5 for _ in pos_bolt[i]]
        #     pos_force[i] = [0.5 for _ in pos_force[i]]
        # else:
        pos_bolt = pos_bolt / (ma-mi)
        pos_force = pos_force / (ma-mi)
        diameter = diameter / (ma-mi)
        centroid = centroid / (ma-mi)
        # [(pos_bolt[i][j]-mi) / (ma - mi) for j in range(len(pos_bolt[i]))]   
        # pos_force[i] = [(pos_force[i][j]-mi) / (ma - mi) for j in range(len(pos_force[i]))]   
        
        return pos_bolt, pos_force, centroid, diameter
    

    def normalize_vector_size(self, max_vect, vect, ipadd):
        # max_size is based of padding in the canvas
        # max_vect is the vector with biggest size
        for vec in vect:
            for i in range(2):
                vec[i] = vec[i]*ipadd / max_vect
        return vect


    def convert_to_vector(self, size, angle):
        vec = []
        for i in range(len(size)):
            x = math.cos(math.radians(angle[i])) * size[i]
            y = math.sin(math.radians(angle[i])) * size[i]
            vec.append([x,y])
        return vec


    def max_vector(self, v1, v2):
        out = 0
        for i in v1: out = max([out, max(i, key=abs)], key=abs)
        if v2: 
            for i in v2: out = max([out, max(i, key=abs)], key=abs)
        return abs(out)


    def check_colission(self, i, j, pos, d):
        dx = abs(pos[0][i] - pos[0][j])
        dy = abs(pos[1][i] - pos[1][j])
        rSum = d[i]/2 + d[j]/2  # sum of radiuses
        dist = math.sqrt(dx**2 + dy**2)

        if rSum > dist: return (True, dist)
        else: return (False, None)



class Scheme():
    """creates scheme"""

    def __init__(self, g, input, cw, ch, err_lab, font):
        self.g = g
        self.cw, self.ch = cw, ch
        self.font = font
        self.err_lab = err_lab

        self.ipadd = 90  # inside canvas padding
        self.fc_d = 3  # force point diameter
        self.allowed_diameter = 60  # maximum allowed diameter of a bolt
        self.axis_size = 50  # indicating axis
        self.axis_dist = 20  # disance from the edge
        self.labdist_bolt = 2  # distance of label form the bolt
        self.labdist_force = 10 # distance of label form the force point

        self.geo = Geometry()


    def resize(self, r, pos, ipadd, cw, ch):  # recursive function for resizing diameter
        md = max(r)  # the miggest diameter
        idx = r.index(md)
        for i in range(2):
            if pos[i][idx] == 0.0 or pos[i][idx] == 1.0:
                if md/2 > ipadd/2:
                    d = [d[i] * (ipadd/md) for i in range(len(d))]
        return d

    def indicate_axis(self):
        base = self.axis_dist
        self.g.create_line(base, self.ch-base, base + self.axis_size, self.ch-base, arrow=tkinter.LAST)
        self.g.create_text(base+self.axis_size-10, self.ch-base+10, text='X', font=self.font[1])

        self.g.create_line(base, self.ch-base, base, self.ch-base-self.axis_size, arrow=tkinter.LAST)
        self.g.create_text(base-10, self.ch-base-self.axis_size+10, text='Y', font=self.font[1])


    def draw_centroid(self, centroid):
        d = 5  # diamter of a centroid
        x = self.ipadd + centroid[0]*(self.cw-2*self.ipadd)
        y = self.ch - self.ipadd - centroid[1]*(self.ch-2*self.ipadd)
        self.g.create_oval(x-d, y-d, x+d, y+d, fill='blue')
        # label
        self.g.create_text(x+d+self.labdist_force, y-d-self.labdist_force, text='C.G.', font=self.font[1])


    def draw_bolts(self, pos, d, bolt):
        axis_ratio = 1.3  # how far does the bolt axis extend
        for i in range(len(pos[0])):
            x = self.ipadd + pos[0][i]*(self.cw-2*self.ipadd)
            y = self.ch - self.ipadd - pos[1][i]*(self.ch-2*self.ipadd)
            r = d[i]*(self.cw-2*self.ipadd)/2
            self.g.create_oval(x-r, y-r, x+r, y+r)
            # axes
            self.g.create_line(x, y-r*axis_ratio, x, y+r*axis_ratio, dash=(4,2))
            self.g.create_line(x-r*axis_ratio, y, x+r*axis_ratio, y, dash=(4,2))
            # label
            self.g.create_text(x+r+self.labdist_bolt, y-r-self.labdist_bolt, text=bolt['name'][i], font=self.font[2])


    def draw_force(self, pos, size, force):
        for i in range(len(pos[0])):
            x = self.ipadd + pos[0][i]*(self.cw-2*self.ipadd)
            y = self.ch - self.ipadd - pos[1][i]*(self.ch-2*self.ipadd)
            # point
            self.g.create_oval(x-self.fc_d, y-self.fc_d, x+self.fc_d, y+self.fc_d, fill='red')
            # size
            x2 = size[i][0]
            y2 =  size[i][1]
            self.g.create_line(x, y, x+x2, y-y2, arrow=tkinter.LAST, fill='red')
            # label
            self.g.create_text(x+self.labdist_force+self.fc_d, y-self.fc_d-self.labdist_force, text=force['name'][i], font=self.font[2])

    def draw_result_force(self, pos, size):
        for i in range(len(pos[0])):
            x = self.ipadd + pos[0][i]*(self.cw-2*self.ipadd)
            y = self.ch - self.ipadd - pos[1][i]*(self.ch-2*self.ipadd)
            x2 = size[i][0]
            y2 =  size[i][1]
            self.g.create_line(x, y, x+x2, y-y2, arrow=tkinter.LAST, fill='green')
    

    def solve_colisions(self, pos, diameters):
        """
        after collision has been detected all diameters are resized
        this is repleated untill there are no collisions
        """
        count = 0
        l = len(pos[0])  # lenght of array with the bolts
        while count < l:
            for i in range(count, l):
                collision, dist = self.geo.check_colission(count, i, pos, diameters)
                if collision:
                    count = 0
                    ratio = dist / (diameters[count]/2 + diameters[i]/2)
                    diameters *= ratio
            count += 1
        return diameters

    
    def resize_diameter(self, bolt, posb):
        diameters = numpy.array(bolt['diameter[mm]'], dtype=numpy.float64)
        diameters *= self.allowed_diameter / max(diameters) 
        # make sure nothing overlaps
        # diameters = self.solve_colisions(posb, diameters)
        return diameters


    def redraw(self, bolt, force, centroid, res_vect):
        # clear the canvas before drawing the new scheme     
        self.g.delete('all')

        # ADJUST THE DATA  ----------------------------------------------------------
        # normalize bolt coordinates along with the centroid
        
        # bolt_args = copy.deepcopy(bolt)
        # bolt_args['x-pos[mm]'].append(centroid[0])
        # bolt_args['y-pos[mm]'].append(centroid[1])

        # normalize input to interval [0, 1]
        posb, posf, centroid, diameters = self.geo.normalize_coordiantes(bolt, force, centroid)
        
        # get back centroid coordinates
        # centroid = [posb[0].pop(), posb[1].pop()]
        
        # # resize the diamter and resolve overlaping 
        # diameters = self.resize_diameter(bolt, posb)
            
        load_vect = self.geo.convert_to_vector(force['size[N]'], force['angle[deg]'])
        max_vect = self.geo.max_vector(load_vect, res_vect)

        load_vect = self.geo.normalize_vector_size(max_vect, load_vect, self.ipadd)
        if res_vect: res_vect = self.geo.normalize_vector_size(max_vect, res_vect, self.ipadd)

        # CREATING THE SCHEME ---------------------------------------------------------=
        # margin area
        self.g.create_rectangle(0+self.ipadd, 0+self.ipadd, self.cw-self.ipadd, self.ch-self.ipadd, fill='white', outline='white')
        self.indicate_axis()
        self.draw_bolts(posb, diameters, bolt)
        self.draw_force(posf, load_vect, force)
        self.draw_centroid(centroid)
        
        if res_vect: self.draw_result_force(posb, res_vect)
        self.g.update()
        
    def idk(self):
        print('jes ty kokoos')