
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import openpyxl as op
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import plotly.figure_factory as ff
import streamlit as st  # pip install streamlit
import streamlit.components.v1 as components



st.set_page_config(
page_title = "Everyone Can Support",
page_icon = ":phone:",
initial_sidebar_state="expanded",
)



def get_data_from_excel3():
    dfs = pd.read_excel(
        io="reports/general-dynamics/general-dynamics.xlsx",
        engine="openpyxl",
        #sheet_name="",
        skiprows=0,
        #usecols="B:R",
        #nrows=1000,
    )
    
    # Add 'hour' column to dataframe
    #df["hour"] = pd.to_datetime(df["receiving time"]).dt.hour
    return dfs



dfg = get_data_from_excel3()

st.subheader("Welcome to support reports dashboard!")
st.text("General dynamics")
#st.write("https://www.buymeacoffee.com/ustyuzhaniX")
#st.sidebar.header("Choose here")


st.dataframe(dfg)


chart_data1 = pd.DataFrame(dfg, columns=['total tickets'])

st.area_chart(chart_data1)


chart_data = pd.DataFrame(dfg, columns=['sla'])

st.area_chart(chart_data)


chart_data2 = pd.DataFrame(dfg, columns=['first response'])

st.area_chart(chart_data2)







