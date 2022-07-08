#!/usr/bin/env python
# coding: utf-8

# # <font color=salmon>    World Happiness Report  </font>
# 

# In[22]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import numpy as np


# In[2]:


import plotly.offline as pyo
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression


# In[3]:


from dash import Dash, dcc, html, Input, Output
from jupyter_dash import JupyterDash


# ## Data Processing
# 
# - Explore all the data set
# - Try to make them all look a like
# - Drop Whisker-high, Whisher-low columns
# - Renaming columns
# - Merge column Regional indicator to 2022 dataset from 2021

# In[4]:


df_2022 = pd.read_csv('Data/2022.csv')



# In[5]:


df_2021 = pd.read_csv('Data/2021.csv')



# Processing 2021 data
df_2021.insert(0, 'Rank', list(range(1,len(df_2021)+1)))
df_2021 = df_2021.drop(['upperwhisker', 'lowerwhisker', 'Standard error of ladder score',\
                        'Logged GDP per capita'], axis=1)
df_2021 = df_2021.drop(['Perceptions of corruption', 'Ladder score in Dystopia', 'Generosity', \
                        'Freedom to make life choices', 'Healthy life expectancy', 'Social support'], axis=1)

df_2021.columns = ['Rank', 'Country','Region', 'Score', 'GDP per Capita',
       'Social Support', 'Healthy Life Expectancy',
       'Freedom for life choices', 'Generosity',
       'Perceptions of Corruption', 'Dystopia + Residual']



# In[7]:


df_2020 = pd.read_csv('Data/2020.csv')



# Processing 2020 data

df_2020.insert(0, 'Rank', list(range(1,len(df_2020)+1)))
df_2020 = df_2020.drop(['upperwhisker', 'lowerwhisker', 'Standard error of ladder score',\
                        'Logged GDP per capita'], axis=1)
df_2020 = df_2020.drop(['Perceptions of corruption', 'Ladder score in Dystopia', 'Generosity',\
                        'Freedom to make life choices', 'Healthy life expectancy', 'Social support'], axis=1)

df_2020.columns = ['Rank', 'Country','Region', 'Score', 'GDP per Capita',
       'Social Support', 'Healthy Life Expectancy',
       'Freedom for life choices', 'Generosity',
       'Perceptions of Corruption', 'Dystopia + Residual']



# ### Processing 2022 data
# * First a new column Region in 2022 data set was added from 2021 using pandas merge function
# * 'Whisker-high', 'Whisker-low' columns was droped
# * Then 'Dystopia + residual' and 'Region' column was re-arranged in the datafraem to look excatly like 2021, 2020
# * Finally columns were renamed to match to 2021, 2020 dataset.


region=df_2021[['Country', 'Region']]

df_2022 = df_2022.merge(region, on='Country')

df_2022 = df_2022.drop(['Whisker-high', 'Whisker-low'], axis=1)
regions = df_2022.pop('Region')
df_2022.insert(2, 'Region', regions)
dystopia = df_2022.pop('Dystopia (1.83) + residual')
df_2022['Dystopia + Residual']=dystopia
df_2022.columns=['Rank', 'Country','Region', 'Score', 'GDP per Capita',
       'Social Support', 'Healthy Life Expectancy',
       'Freedom for life choices', 'Generosity',
       'Perceptions of Corruption', 'Dystopia + Residual']





def create_barplot_top(data, number_of_countries, year):

    fig = go.Figure()

    #color_list = ['#2170B4', '#A54588', '#3A8382', '#F28560', '#9482C4', '#3A3A3A', '#35617E']
    #color_list=['#FCE1A5', '#F6AB76', '#EA7558', '#D34A55', '#AD2B5F', '#7F1B61', '#401248']
#     color_list=['rgb(237,247,178)', 'rgb(213,238,179)', 'rgb(152,214,185)', \
#                 'rgb(78,187,194)', 'rgb(30,145,192)', 'rgb(34,92,166)', \
#                 'rgb(33,49,140)']
    color_list=['rgb(205,227,233)', 'rgb(145,192,227)', 'rgb(116,155,228)', \
                'rgb(118,118,215)', 'rgb(120,73,175)', 'rgb(110,44,129)', \
                'rgb(85,23,76)']
    col_list = data.columns[4:]
    for col, color in zip(col_list,color_list):
        fig.add_trace(go.Barpolar(
            theta = data['Country'][:number_of_countries],
            r = data[col][:number_of_countries],
            name = col,
            marker = dict(color=color), opacity=0.7
            )
        )

    fig.update_layout(
        title = dict(
            text=f'Top {number_of_countries} Happy Countries of {year}', 
            yanchor = 'top', xanchor='center',
            x = 0.5, y=0.95
        ),
        barmode='stack',
        template='simple_white'
    )


    fig.add_annotation(dict(font=dict(color='grey',size=18),
        text = 'Happiest Countries',                   
        x = 0.5, y=0.52, showarrow=False 
    ))

    fig.add_annotation(dict(font=dict(color='grey',size=18),
        text = 'of the World',                   
        x = 0.5, y=0.48, showarrow=False 
    ))

    fig.update_layout(width=1000, height=800)
    fig.update_layout(legend=dict(
        orientation = 'h',
        yanchor = 'top',
        y=-0.1,
        xanchor='center',
        x=0.5
    ))

    fig.update_layout(polar=dict(radialaxis=dict(range=[-4,8], showticklabels=False, 
                                                ticks='', linewidth=0, showgrid=False),
                                 angularaxis = dict(
                                    direction = "clockwise",
                                        period = 30, showgrid=False, showline=False) 
                            ))
    fig.show()





app = Dash(__name__)

#app = JupyterDash(__name__)

app.layout = html.Div([
            dcc.RadioItems(
                ['2022', '2021', '2020'],
                '2022',
                id='year',
                inline=True
            ),

    dcc.Graph(id='indicator-graphic'),


])


@app.callback(
    [Output('indicator-graphic', 'figure')],
    [Input('year', 'value')])


def update_graph(year_value):
    
    if year_value == '2022':
        fig=create_barplot_top(df_2022,30, 2022)
    
    elif year_value == '2021':
        fig=create_barplot_top(df_2021,30, 2021)
        
    elif year_value == '2020':
        fig=create_barplot_top(df_2020,30, 2020)
        
    return fig
        

if __name__ == '__main__':
    app.run_server(debug=True)

#app.run_server(mode='inline', port=8051)









