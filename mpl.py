
import matplotlib.pyplot as plt
import bokeh.mpl as mpl 
from bokeh.plotting import figure, output_file, show

plt.plot([1,2,3,4])
plt.ylabel('some numbers')

d = mpl.to_bokeh(plt) 

show(d) 




