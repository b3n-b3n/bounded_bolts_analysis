import math 
import tkinter
import numpy

class Sketch():
    """creates scheme"""

    def __init__(self, g, input, cw, ch):
        self.g = g
        self.cw, self.ch = cw, ch
        self.ipadd = 75  # inside canvas padding
        self.fc_d = 5  # force point diameter
        self.fc_width = 5  # force width
        
        self.allowed_diameter = 40


    def resize(self, r, pos, ipadd, cw, ch):  # recursive function for resizing diameter
        exe = True
        md = max(r)  # the miggest diameter
        idx = r.index(md)
        for i in range(2):
            if pos[i][idx] == 0.0 or pos[i][idx] == 1.0:
                if md/2 > ipadd/2:
                    d = [d[i] * (ipadd/md) for i in range(len(d))]
        return d


    def normalize_coordiantes(self, bolt, force):
        xy = ['x-position', 'y-position']   # name of keys from dict
        pos_bolt = ['', '']  # first is x coordinate then y
        pos_force = ['', '']

        for i in range(2):  # normalizing input of position
            pos_bolt[i], pos_force[i] = bolt[xy[i]], force[xy[i]]
            pos_bolt[i] = [float(pos_bolt[i][j]) for j in range(len(pos_bolt[i]))]
            pos_force[i] = [float(pos_force[i][j]) for j in range(len(pos_force[i]))]
            
            merged = pos_bolt[i] + pos_force[i]
            mi, ma = min(merged), max(merged)
            if mi == ma:
                pos_bolt[i] = [0.5 for _ in pos_bolt[i]]
                pos_force[i] = [0.5 for _ in pos_force[i]]
            else:
                # tu si skoncil g
                pos_bolt[i] = [(pos_bolt[i][j]-mi) / (ma - mi) for j in range(len(pos_bolt[i]))]   
                pos_force[i] = [(pos_force[i][j]-mi) / (ma - mi) for j in range(len(pos_force[i]))]   
        return pos_bolt,  pos_force


    def draw_bolts(self, pos, d):
        # # print(d, 'these are diameters of bolts')
        # # print(pos, 'these are the positions of bolts')
        # ratio = 1.3
        # for i in range(len(pos[0])):
        #     x = self.ipadd + pos[0][i]*(self.cw-2*self.ipadd)
        #     y = self.ipadd + pos[1][i]*(self.ch-2*self.ipadd)
        #     self.g.create_oval(x-d[i], y-d[i], x+d[i], y+d[i], fill='red')
        #     # axes
        #     self.g.create_line(x, y-d[i]*ratio, x, y+d[i]*ratio, dash=(4,2))
        #     self.g.create_line(x-d[i]*ratio, y, x+d[i]*ratio, y, dash=(4,2))
        pass


    def draw_force(self, pos, force):
        ang = force['angle']
        size = force['size']
        for i in range(len(pos[0])):
            x = self.ipadd + pos[0][i]*(self.cw-2*self.ipadd)
            y = self.ipadd + pos[1][i]*(self.ch-2*self.ipadd)
            self.g.create_oval(x-self.fc_d, y-self.fc_d, x+self.fc_d, y+self.fc_d, fill='hotpink')
            
            x2 =  math.cos(math.radians(ang[i]))*size[i]
            y2 =  math.sin(math.radians(ang[i]))*size[i]
            self.g.create_line(x, y, x+x2, y-y2, arrow=tkinter.LAST)
    
    
    def check_diameter(self):
        pass

    
    def chceck_force(self):
        pass

   
    def redraw(self, bolt, force, centroid):
        # clear the canvas before drawing the new sketchz     
        self.g.delete('all')

        # normalize centroid coordinates along with the bolts
        print(bolt['x-position'], bolt['y-position'], 'toto sú inputové infošky')
        # bolt['x-position'].append(centroid[0])
        # bolt['y-position'].append(centroid[1])
        bolt_args = bolt.copy()
        # posb[0], posb[1] = bolt['x-position'].copy(), bolt['y-position'].copy()
        bolt_args['x-position'].append(centroid[0])
        bolt_args['y-position'].append(centroid[1])

        # normalize input to interval [0, 1]
        posb, posf = self.normalize_coordiantes(bolt_args, force)
        
        # # get back centroid coordinates
        # print(posb, 'pred pop')
        centroid[0] = posb[0].pop()
        centroid[1] = posb[1].pop()
        # print(posb, 'po pop')
        
        # resize the diamter
        diameters = numpy.array(bolt['diameter'], dtype=numpy.float64)
        diameters *= self.allowed_diameter / max(diameters) 

        # resize the force
        
        # make sure nothing overlaps
        # self.check_diameter(posb, bolt)
        # self.chceck_force(posf, force)

        # draw scheme
        self.draw_bolts(posb, diameters)
        self.draw_force(posf, force)

        # d = [ float(self.bolt_info['diameter'][i]) for i in range(len(self.bolt_info['diameter']))]  # diameters of bolts
        # r = self.resize(r, pos, ipadd, cw, ch)
        self.g.create_rectangle(0+self.ipadd, 0+self.ipadd, self.cw-self.ipadd, self.ch-self.ipadd, fill='white')
        
    def idk(self):
        print('jes ty kokoos')