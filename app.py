import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from  datetime import datetime,date,timedelta
import time
import numpy as np

#page configurations
st.set_page_config(
     page_title="Covid-Dashboard",
     page_icon="🧊",
     layout="wide",
     
) 
# df = pd.read_excel('owid-covid-data.xlsx')
# https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv
#read data in chunks of 1 million rows at a time
if 'number' not in st.session_state:
    start = time.time()
    st.session_state['number'] = 1
    chunk = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv",chunksize=100000)
    st.session_state['df'] = pd.concat(chunk)
    end = time.time()
    st.write("Read csv with chunks: ",(end-start),"sec")
#keeping the df inside the session in order to not rerun the import code
df =st.session_state.df 
# chunk = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv",chunksize=100000)
# chunk = pd.read_excel('https://covid.ourworldindata.org/data/owid-covid-data.xlsx',chunksize=10000)



df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")

#date range picker
max_date = max(df['date'])
min_date =  min(df['date'])

# dt_max = datetime.strptime(max_date,'%Y-%m-%d')
# dt_min = datetime.strptime(min_date,'%Y-%m-%d')

start_time = st.sidebar.date_input(
     "Select the date range?",
     min_value=datetime.date(min_date), 
     max_value=datetime.date(max_date),
     value = [datetime.date(max_date) - timedelta(days=7),datetime.date(max_date)]

   )
st.write("Start time:", start_time)

#Selecting regions 
regions = st.sidebar.multiselect(
     'Select the regions',
     ['World', 'Asia', 'SAARCK'])
st.write(regions)

if len(start_time) ==1:
    st.write("Please choose a date range")
else:
    #date filter function   
    after_start_date = df['date'] >= start_time[0].strftime('%Y-%m-%d %H:%M:%S')
    before_end_date = df['date'] <= start_time[1].strftime('%Y-%m-%d %H:%M:%S')
        
    between_two_dates = after_start_date & before_end_date
        
    df = df.loc[between_two_dates]
    df

df_world = df.loc[df['location'] == "World"]
df_world = df_world.groupby(by = 'date').sum().reset_index()

df_sl = df.loc[df['location'] == "Sri Lanka"]
df_sl = df_sl.groupby(by = 'date').sum().reset_index()

saarck_list = ['afghanistan','Bangladesh','Bhutan' ,'India' , 'Nepal' , 'Maldives','Pakistan','Sri Lanka']
df_saarck = df[df.location.isin(saarck_list)]
df_saarck =  df_saarck.groupby(by = 'date').sum().reset_index()

df_asia = df.loc[df['location'] == 'Asia']
df_asia=  df_asia.groupby(by = 'date').sum().reset_index()

dfd_world = df_world.groupby(by = 'date').sum().reset_index()

#Calculating the weekly monthly averages and daily
df_world_i = df_world.set_index('date')
df_sl_i = df_sl.set_index('date')
df_asia_i = df_asia.set_index('date')
df_saarck_i = df_saarck.set_index('date')
#sidebar options
#Variable selector
variable = st.sidebar.selectbox("", ('Total Cases', 'New Cases', 'New Deaths', 'Total Deaths'), 1)

cal_type = st.sidebar.radio(
     "",
     ('Daily', 'Weekly Average', 'Monthly Average'))

if cal_type == 'Weekly Average':
     df_world_cal = df_world_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("W").mean()
     df_sl_cal = df_sl_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("W").mean()
     df_asia_cal = df_asia_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("W").mean()
     df_saarck_cal = df_saarck_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("W").mean()

elif cal_type == "Monthly Average" :
     df_world_cal = df_world_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("M").mean()
     df_sl_cal = df_sl_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("M").mean()
     df_asia_cal = df_asia_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("M").mean()
     df_saarck_cal = df_saarck_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("M").mean()

else:
        df_world_cal = df_world_i
        df_sl_cal = df_sl_i
        df_asia_cal = df_asia_i
        df_saarck_cal = df_saarck_i        
# after_start_date
# before_end_date

st.write("""

# COVID Dashboard 

""")








if variable == "Total Cases":
        var_title = "total_cases"
elif variable == "New Cases":
        var_title = "new_cases"
elif variable == "New Deaths":
        var_title = "new_deaths"
else:
        var_title = "total_deaths"
    
# title1 = "{} summary between {} and {}".format(var_title , start_date , end_date)
 
#Objects to draw the line plot
title2 = 'Covid Cases Across the Regions'

colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']  

mode_size = [8, 8, 12, 8]
line_size = [2, 2, 4, 2]

#Default layout for the all the graphs
layout = go.Layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    ),
    font={
            "family": "Nunito",
            "size": 12,
            "color": "#707070",
        },
    title={
            "font": {
                "family": "Lato",
                "size": 18,
                "color": "#1f1f1f",
            },
        },
   
   paper_bgcolor="#ffffff",
   colorway=px.colors.qualitative.G10,
   # Sets background color to white
   
   xaxis=dict(showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',)
          # Removes X-axis grid lines
    ),
    
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
    autosize = False,
    margin = dict(
        autoexpand = False,
        l = 100,
        r = 20,
        t = 110,
    ),
    showlegend = False,
    plot_bgcolor = 'white'
)
#Figure1
   
   
#REgion selecting code
variable_list = [df_sl_cal]
labels2 = ['Sri Lanka']
y_df = pd.DataFrame()
y_df['sl'] = df_sl_cal[var_title]


for var in regions:
    if var == 'Asia':
        labels2.append('Asia')
        variable_list.append(df_asia_cal)
        y_df['Asia'] = df_asia_cal[var_title]
    if var == 'World':
        labels2.append('World')
        variable_list.append(df_world_cal)
        y_df['World'] = df_world_cal[var_title]
    if var == 'SAARCK':
        labels2.append('SAARCK')
        variable_list.append(df_saarck_cal)
        y_df['SAARCK'] = df_saarck_cal[var_title]

y_df_array = np.transpose(y_df.to_numpy())
y_df_array
#Figure2

fig2 = go.Figure(layout=layout)

for i in range(len(variable_list)):
    fig2.add_trace(go.Scatter(x=variable_list[i].index, y=variable_list[i][var_title], mode='lines',
        name=labels2[i],
        line=dict(color=colors[i]),  #width=line_size[i]
        connectgaps=True,  
        text = labels2,      
        hovertemplate=
        'Cases: %{y:}'+
        '<br>Date: %{x}<br>',
        
    ))

    fig2.add_trace(go.Scatter(
        x=[variable_list[i].index[0], variable_list[i].index[-1]],
        y=[variable_list[i][var_title][0], variable_list[i][var_title][-1]],
        mode='markers',
        marker=dict(color=colors[i]) # size=mode_size[i])
    ))

annotations = []

# Adding labels
for y_trace, label, color in zip(y_df_array, labels2, colors):
    # labeling the left_side of the plot
    annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                  xanchor='right', yanchor='top',
                                  text=label + ' {}'.format(round(y_trace[0])),
                                  font=dict(family='Arial',
                                            size=16),
                                  showarrow=False))
    # labeling the right_side of the plot
    annotations.append(dict(xref='paper', x=0.95, y=y_trace[len(y_trace)-1],
                                  xanchor='left', yanchor='top',
                                  text='{}'.format(round(y_trace[len(y_trace)-1])),
                                  font=dict(family='Arial',
                                            size=16),
                                  showarrow=False))
# Title
annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text='Covid cases across regions',
                              font=dict(family='Arial',
                                        size=30,
                                        color='rgb(37,37,37)'),
                              showarrow=False))
# Source
annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='Source: PewResearch Center & ' +
                                   'Storytelling with data',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))

fig2.update_layout(annotations=annotations)

# fig2.add_trace(go.Scatter(x=df_world_cal.index, y=(df_world_cal[var_title]),
#                     mode='lines',
#                     name='lines'))
# fig2.add_trace(go.Scatter(x=df_sl_cal.index, y=df_sl_cal[var_title],
#                     mode='lines',
#                     name='lines'))
# fig2.add_trace(go.Scatter(x=df_saarck_cal.index, y=df_saarck_cal[var_title],
#                     mode='lines',
#                     name='lines'))
# fig2.add_trace(go.Scatter(x=df_asia_cal.index, y=df_asia_cal[var_title],
#                     mode='lines',
#                     name='lines'))                   

#Layout seperator
#First Column
# col1,col2 = st.columns(2)


# col1.plotly_chart(fig2, config={"displayModeBar": False, "showTips": False}, use_container_width=True)
# col2.plotly_chart(fig2, config={"displayModeBar": False, "showTips": False}, use_container_width=True)
st.plotly_chart(fig2,use_container_width=True)