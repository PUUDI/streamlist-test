import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from  datetime import datetime,date,timedelta
import time

#page configurations
st.set_page_config(
     page_title="Covid-Dashboard",
     page_icon="🧊",
     layout="wide",
     
) 
# df = pd.read_excel('owid-covid-data.xlsx')

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
dfd_world = df_world.groupby(by = 'date').sum().reset_index()

df_sl = df.loc[df['location'] == "Sri Lanka"]
saarck_list = ['afghanistan','Bangladesh','Bhutan' ,'India' , 'Nepal' , 'Maldives','Pakistan','Sri Lanka']

df_saarck = df[df.location.isin(saarck_list)]
df_saarck =  df_saarck.groupby(by = 'date').sum().reset_index()
df_asia = df.loc[df['location'] == 'Asia']

dfd_world = df_world.groupby(by = 'date').sum().reset_index()
dfd_sl = df_sl.groupby(by = 'date').sum().reset_index()
#sidebar options
#Variable selector
variable = st.sidebar.selectbox("", ('Total Cases', 'New Cases', 'New Deaths', 'Total Deaths'), 0)




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
title1 = "Best graph in the world"    
fig1 = px.line( x =dfd_world['date'], y = dfd_world[var_title])    
    
fig1.update_layout(
title=title1,
# template='plotly_dark',
xaxis_title="Date",
yaxis_title=variable,
legend_title="Legend Title"
)
    
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_world['date'], y=(df_world[var_title]),
                    mode='lines',
                    name='lines'))
fig2.add_trace(go.Scatter(x=df_sl['date'], y=df_sl[var_title],
                    mode='lines',
                    name='lines'))
fig2.add_trace(go.Scatter(x=df_saarck['date'], y=df_saarck[var_title],
                    mode='lines',
                    name='lines'))

#Layout seperator
#First Column
col1,col2 = st.columns(2)


col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)