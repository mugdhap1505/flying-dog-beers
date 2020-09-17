import plotly.graph_objects as go # or plotly.express as px
fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )



import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


data_dir = ''
data_file = 'energies_and_times.txt'

cook_time = 601.5 # cook time in ms
stack_period = 62 # stack period (duty cycle) in ms
ramp_period = 26 # ramp period in ms
is_folded = False # fold and sum ramp sides?

plot_energy_bounds = [0,10000] # [upper, lower] photon energy axis limits (eV)
plot_voltage_bounds = [2.2,4.99] # [upper, lower] beam energy axis limits (keV)

energy_bin = 2 # photon energy bins size (eV)
voltage_bin = .005 # beam energy bins size (keV)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

data = pd.read_csv(data_dir + data_file, header=0, names=['energy','time'])

data = data[(data['time'] >= cook_time)] # truncates cook period
data['time'] = (data['time'] - cook_time) % stack_period # stack
if is_folded:
    data['time'][(data['time'] < ramp_period/2)] = abs(data['time'][(data['time'] < ramp_period/2)] - ramp_period) # fold ramp sides together
data = data[(data['time'] > ramp_period/2)]

def piecewise_voltage(x): # time to voltage transform
        conds = [x < 15.0, (x >= 15.0) & (x < 25.0), (x >= 25.0) & (x < 28.0), x >= 28.0]
        funcs = [lambda x: 2.2, lambda x: x*0.155-0.125, lambda x: x*0.4166666-6.6666666, lambda x: 5.0]
        return np.piecewise(x, conds, funcs)
data['voltage'] = data['time']
data['voltage'] = data['voltage'].apply(piecewise_voltage)

plot_data = data[(data['voltage'] > plot_voltage_bounds[0]) & (data['voltage'] <= plot_voltage_bounds[1]) & (data['energy'] > plot_energy_bounds[0]) & (data['energy'] <= plot_energy_bounds[1])] # truncate data out of bounds

import plotly.graph_objects as go
import numpy as np
df = data

x=plot_data['voltage'] 
y=plot_data['energy']

fig = go.Figure()





abc = int((plot_voltage_bounds[1]-plot_voltage_bounds[0])/voltage_bin)
#print(abc)
xyz = int((plot_energy_bounds[1]-plot_energy_bounds[0])/energy_bin)
#print(xyz)



fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode='markers',
    showlegend=False,
    marker=dict(
        symbol='x',
        opacity=0.7,
        color='blue',
        size=1,
        #line=dict(width=1),
    )
))



fig.add_trace(go.Histogram2d(
    x=x,
    y=y,
    colorscale=[[0, 'rgb(250,250,250)'], [0.25, 'rgb(0, 159, 222)'], [0.5, 'rgb(242,211,56)'], [0.75, 'rgb(242,143,56)'], [1, 'rgb(217,30,30)']],
    #colorscale='jet',
    zmax=70,
    zmin=1,
    #zmid=9,
    nbinsx=abc,
    nbinsy=xyz,
    #zauto=True
    

    
    

))

fig.update_layout(
    xaxis=dict( ticks='', showgrid=False, zeroline=False, nticks=20 ),
    yaxis=dict( ticks='', showgrid=False, zeroline=False, nticks=20 ),
    autosize=False,
    height=550,
    width=550,
    hovermode='closest',
    title="Energies_&_Times",
    xaxis_title="Beam Energy (keV)",
    yaxis_title="Photon Energy (eV)",
    #margin=dict(l=80, r=80, t=100, b=80),
    #norm=mcolors.PowerNorm(.6),
    
    
)

fig.show()



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        figure=fig
    ),
]
)

if __name__ == '__main__':
    app.run_server()