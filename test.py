import matplotlib.pyplot as plt

ax = plt.axes()
ax.arrow(.1,0,.6,0, width=0.001, color="k", 
             head_width=0.1, head_length=0.15, overhang=0)
plt.show()