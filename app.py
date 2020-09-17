Skip to content
Search or jump to…

Pull requests
Issues
Marketplace
Explore
 
@mugdhap1505 
austinlasseter
/
plotly_dash_tutorial
2
1223
Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
plotly_dash_tutorial/04 visualize pandas/pandas_example1.py /
@austinlasseter
austinlasseter refreshed all examples
Latest commit bc242a0 on Sep 6, 2019
 History
 1 contributor
45 lines (39 sloc)  1.31 KB
  

# imports
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

# read in the dataset
source="../00 resources/titanic.csv"
df=pd.read_csv(source)
# group survival results by sex and cabin class
sex_survive=df.groupby(['Sex', 'Pclass']).Survived.mean()
sex_survive=sex_survive*100
mylist=list(sex_survive)

# instantiate the class
app = dash.Dash()
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
app.title = 'Titanic!'

# define the layout
app.layout = html.Div(children=[
    html.H1(children='Titanic!'),
    html.Div(children='Who survived the sinking of the Titanic?'),
    dcc.Graph(
        id='titanic-graph',
        figure={
            'data': [
                {'x': ['1st Class', '2nd Class', '3rd Class'], 'y': [mylist[0], mylist[1], mylist[2]], 'type': 'bar', 'name': 'Female'},
                {'x': ['1st Class', '2nd Class', '3rd Class'], 'y': [mylist[3], mylist[4], mylist[5]], 'type': 'bar', 'name': 'Male'},
            ],
            'layout': {
                'title': 'Survival Rate by Sex',
                'xaxis':{'title':'Cabin Class'},
                'yaxis':{'title':'Percentage Survival'},
            }
        }
    ),
    html.H1('this is another heading')
])

# execute
if __name__ == '__main__':
    app.run_server()
© 2020 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
