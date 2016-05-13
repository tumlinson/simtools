''' Docstring 
'''
import numpy as np
import math 

from astropy.io import ascii 
from astropy.table import Table 

from bokeh.io import output_file, gridplot 
from bokeh.plotting import Figure
from bokeh.resources import CDN
from bokeh.embed import components 
from bokeh.models import ColumnDataSource, HBox, VBoxForm, HoverTool, Paragraph 
from bokeh.models.widgets import Slider, TextInput, Select 
from bokeh.io import hplot, vplot, curdoc
from bokeh.embed import file_html

q = ascii.read('data/fos_qso_short.txt') 
s = Table.read('data/ckp00_41000.fits') 
s['g50'] = s['g50'] / 1.5e11 

sn = (1e-15*q['FLUX']*1. * (1.e15) * 36. ) ** 0.5 

junkf = 1e-15*q['FLUX'] 
junkf[q['WAVE'] < 1100.] = -999.  
junkf[q['WAVE'] > 1800.] = -999.  

full_qso_spectrum = ColumnDataSource(data=dict(w=q['WAVE']*1., f=1e-15*q['FLUX']*1., w0=q['WAVE']*1., f0=1e-15*q['FLUX'], junkf=junkf, sn=sn)) 
full_o5_spectrum = ColumnDataSource(data=dict(w=s['WAVELENGTH']*1., f=1e-12*s['g50']*1., w0=s['WAVELENGTH']*1., f0=1e-12*q['g50'], junkf=junkf, sn=sn)) 

flux_plot = Figure(plot_height=400, plot_width=800, 
              tools="crosshair,hover,pan,reset,resize,save,box_zoom,wheel_zoom", outline_line_color='black', 
              x_range=[900, 2000], y_range=[0, 4e-15], toolbar_location='above') 
flux_plot.background_fill_color = "beige"
flux_plot.background_fill_alpha = 0.5 
flux_plot.yaxis.axis_label = 'Flux' 
flux_plot.xaxis.axis_label = 'Wavelength' 

flux_plot.line('w', 'f', source=full_qso_spectrum, line_width=3, line_color='blue', line_alpha=0.3)

sn_plot = Figure(plot_height=400, plot_width=750, 
              tools="crosshair,hover,pan,reset,resize,save,box_zoom,wheel_zoom", outline_line_color='black', 
              x_range=[900, 2000], y_range=[0, 40], toolbar_location='above')
sn_plot.line('w', 'sn', source=full_qso_spectrum, line_width=3, line_color='orange', line_alpha=0.6)
sn_plot.background_fill_color = "beige"
sn_plot.background_fill_alpha = 0.5 
sn_plot.xaxis.axis_label = 'Wavelength' 
sn_plot.yaxis.axis_label = 'S/N per resel' 

# Set up widgets
redshift = Slider(title="Redshift", value=0.0, start=0., end=1.0, step=0.02)
magnitude = Slider(title="Magnitude", value=18., start=15., end=20.0, step=0.1)
template = Select(title="Template Spectrum", value="QSO", options=["QSO", "O5V Star"])

grating = Select(title="Grating", value="G130M", options=["G130M", "G160M"])
aperture = Slider(title="Aperture (meters)", value=12., start=2., end=20.0, step=1.0)
exptime = Slider(title="exptime", value=1., start=1., end=10.0, step=0.1)

def update_data(attrname, old, new):
 
    full_qso_spectrum.data['w'] = np.array(full_qso_spectrum.data['w0']) * (1. + redshift.value)
    full_qso_spectrum.data['f'] = np.array(full_qso_spectrum.data['f0']) * 10.**( (18.-magnitude.value) / 2.5)
    sn = (np.array(full_qso_spectrum.data['f']) * (1.e15) * 36. ) ** 0.5
    full_qso_spectrum.data['sn'] = sn

    full_qso_spectrum.data['junkf'] = (full_qso_spectrum.data['f']) 
    full_qso_spectrum.data['junkf'][np.where(np.array(full_qso_spectrum.data['w']) < 1200.)] = -999.
    full_qso_spectrum.data['junkf'][np.where(np.array(full_qso_spectrum.data['w']) > 1700.)] = -999. 

    print 'Oh you want the template QSO for ', template.value, 'do you? ' 
    if ('O5' in template.value): 
        full_qso_spectrum.data['w0'] 

# iterate on changes to parameters 
for w in [aperture, redshift, template, magnitude, exptime, grating]:
    w.on_change('value', update_data)
for sd in [redshift, magnitude]:
    sd.on_change('value', update_data)
 
# Set up layouts and add to document
inputs1 = VBoxForm(children=[redshift, magnitude, template])
inputs2 = VBoxForm(children=[grating, aperture, exptime])
b1 = HBox(children=[inputs1, flux_plot])
b2 = HBox(children=[inputs2, sn_plot])
v = VBoxForm(children=[b1, b2])
curdoc().add_root(v)
