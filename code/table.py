import matplotlib.pyplot as plt

data = [[1,2,3,4],[6,5,4,3],[1,3,5,1]]

table = plt.table(cellText=data, colLabels=['A', 'B', 'C', 'D'], loc='center', 
                  cellLoc='center', colColours=['#FFFFFF', '#F3CC32', '#2769BD', '#DC3735'])
h = table.get_celld()[(0,0)].get_height()
w = table.get_celld()[(0,0)].get_width()

# Create an additional Header
print(w, h)
header = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [1,2,3]]
header[0].visible_edges = "TBL"
header[1].visible_edges = "TB"
header[2].visible_edges = "TBR"
header[1].get_text().set_text("Header")

plt.axis('off')
plt.show()

# enter image description here