# @Email:  contact@pythonandvba.com
# @Website:  https://pythonandvba.com
# @YouTube:  https://youtube.com/c/CodingIsFun
# @Project:  Sales Dashboard w/ Streamlit



import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import openpyxl as op
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import plotly.figure_factory as ff
import streamlit as st  # pip install streamlit



# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
#st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache(allow_output_mutation=True)
def get_data_from_excel():
    df = pd.read_excel(
        io="Report_status_2022-10-25_2022-10-31_web_GENERAL.xlsx",
        engine="openpyxl",
        #sheet_name="Sales",
        skiprows=0,
        #usecols="B:R",
        #nrows=1000,
    )
    
    # Add 'hour' column to dataframe
    #df["hour"] = pd.to_datetime(df["receiving time"]).dt.hour
    return df



df = get_data_from_excel()




# ---- SIDEBAR ----



st.sidebar.header("Please Filter Here:")

language = st.sidebar.multiselect(
    "Select the language:",
    options=df["language"].unique(),
    default=df["language"].unique()
)

agent_name = st.sidebar.multiselect(
    "Agent",
    options=df["agent"].unique(),
    default=df["agent"].unique(),
)

topics = st.sidebar.multiselect(
    "Topics",
    options=df["topics"].unique(),
    default=df["topics"].unique()
)

subtopics = st.sidebar.multiselect(
    "Subtopics",
    options=df["subtopics"].unique(),
    default=df["subtopics"].unique()
)

df = df.query(
    "language == @language & agent ==@agent_name & topics == @topics & subtopics == @subtopics"
)



        
        # ---- MAINPAGE ----
st.title("Dashboard")
st.title("Dashboard")
st.markdown("##")

# TOP KPI's
total_tickets = {len(df)}


df['receiving_time'] = pd.to_datetime(df['receiving time'])


#print(df['date of the first response'])


df['date of the first response'] = pd.to_datetime(
    df['date of the first response'], format='%Y-%m-%d %H:%M:%S', errors='ignore')

#print(df['date of the first response'])

df['receiving_time'] = pd.to_datetime(df['receiving time'])


df['hour'] = pd.to_datetime(df['receiving time']).dt.hour
df['month'] = pd.to_datetime(df['receiving time']).dt.month_name()
df['date'] = pd.to_datetime(df['receiving time']).dt.date

df['date of the first response'] = df['date of the first response'].drop_duplicates()
df['date of the first response'] = df['date of the first response'].apply(
    pd.to_numeric, errors='ignore')


#print(df['date of the first response'])




#print(df['date of the first response'])

#print(df['date of the first response'])


#df['receiving time'] = df['receiving time'].astype('str').str[-8:]

#print(df['receiving time'])

#print(df['date of the first response'])

df['date of the first response'] = (pd.to_datetime(
    df['date of the first response']) - pd.to_datetime(df['receiving time'])).astype('str').str[-8:]

#print(df['date of the first response'])

#df['date of the first response'] = (pd.to_datetime(
#    df['date of the first response']) - pd.to_datetime(df['receiving time']))


#print(df['date of the first response'])



#print(df['date of the first response'])

def sla_category(time):
     
    if time < '00:05:00':
        return '5 minutes'
    elif time <= '00:15:00':
        return '15 minutes'
    elif time <= '00:30:00':
        return '30 minutes'
    elif time <= '00:45:00':
        return '45 minutes'
    elif time <= '01:00:00':
        return '60 minutes'
    elif time <= '23:00:00':
        return '61 minutes and more'
    else:
        return 'неизвестно'


df['sla cat'] = df['date of the first response'].apply(sla_category)


sla5 = df[df['sla cat'] == '5 minutes']['sla cat'].count()






# Служебные функции
def annotate_bars_column(data, column, index=0, align='center'):


    for i, v in enumerate(data[column].iteritems()):
        plt.text(x=i+index, y=v[1], s=v[1], ha=align, va='bottom')


df.loc[df['date of the first response'] != '0',
      'date of the first response'] = pd.to_timedelta(df['date of the first response'])






meantime = df.loc[df['date of the first response'] != 'неизвестно', 'date of the first response'].median()


#print(meantime)

def change_timedelta_to_normal(td):
    secs = td.total_seconds()
    m = secs // 60
    m = '0' + str(int(m)) if m < 10 else str(int(m))
    secs = secs % 60
    secs = '0' + str(int(secs)) if secs < 10 else str(int(secs))
    return f'{m}:{secs}'
meantime_str = change_timedelta_to_normal(meantime)



#print(sla5)



left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Tickets:")
    st.subheader(f"{total_tickets}")
with middle_column:
    st.subheader("First response")
    st.subheader(f"{meantime_str}")
with right_column:
    st.subheader("5 min SLA")
    st.subheader(f"{sla5}")

st.markdown("""---""")



#SALES BY PRODUCT LINE [BAR CHART]




ticket_by_sla = (
    df.groupby(by=["sla cat"]).count()[["ticket number"]].sort_values(by="ticket number")
)

fig_ticket_by_sla = px.bar(
    ticket_by_sla,
    x="ticket number",
    y=ticket_by_sla.index,
    orientation="h",
    title="<b>tickets by sla</b>",
    color_discrete_sequence=["#0083B8"] * len(ticket_by_sla),
    template="plotly_white",
)

fig_ticket_by_sla.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)




def sla_category(time):
     
    if time == 'Int Spanish':
        return 'spanish'
    elif time == 'Int English':
        return 'english'
    elif time == 'Int Indonesian':
        return 'indonesian'
    elif time == 'Int Portuguese':
        return 'portuguese'
    else:
        return 'неизвестно'


df['lang cat'] = df['language'].apply(sla_category)




ticket_lang = (
    df.groupby(by=["lang cat"]).count()[["ticket number"]].sort_values(by="ticket number")
)

fig_ticket_lang = px.bar(
    ticket_lang,
    x="ticket number",
    y=ticket_lang.index,
    orientation="h",
    title="<b>ticket by lang</b>",
    color_discrete_sequence=["#0083B8"] * len(ticket_lang),
    template="plotly_white",
)

fig_ticket_lang.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


ticket_by_channel = (
    df.groupby(by=["ticket channel"]).count()[["ticket number"]].sort_values(by="ticket number")
)

fig_ticket_by_channel = px.bar(
    ticket_by_channel,
    x="ticket number",
    y=ticket_by_channel.index,
    orientation="h",
    title="<b>tickets by channel</b>",
    color_discrete_sequence=["#0083B8"] * len(ticket_by_channel),
    template="plotly_white",
)




def sla_category(cat):
     
    if cat == 'Int Marketing':
        return 'marketing'
    elif cat == 'Int Homework questions':
        return 'homework questions'
    elif cat == 'Int Organizational Issues':
        return 'organizational issues'
    elif cat == 'Int Technical issues':
        return 'technical issues'
    elif cat == 'Int Refunds':
        return 'refunds'
    elif cat == 'Int Payments':
        return 'payments'
    elif cat == 'Int Other':
        return 'other'
    elif cat == 'Int Product':
        return 'product'
    elif cat == 'Reactions in SM (Social Media)':
        return 'social media'
    elif cat == 'Platform bugs':
        return 'platform bug'
    else:
        return 'неизвестно'


df['topics cat'] = df['topics'].apply(sla_category)





ticket_by_topics = (
    df.groupby(by=["topics cat"]).count()[["ticket number"]].sort_values(by="ticket number")
)

fig_ticket_by_topics = px.bar(
    ticket_by_topics,
    x="ticket number",
    y=ticket_by_topics.index,
    orientation="h",
    title="<b>ticket by topic</b>",
    color_discrete_sequence=["#0083B8"] * len(ticket_by_topics),
    template="plotly_white",
)

fig_ticket_by_topics.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


ticket_by_subtopics = (
    df.groupby(by=["subtopics"]).count()[["ticket number"]].sort_values(by="ticket number")
)

fig_ticket_by_subtopics = px.bar(
    ticket_by_subtopics,
    x="ticket number",
    y=ticket_by_subtopics.index,
    orientation="h",
    title="<b>ticket by subtopic</b>",
    color_discrete_sequence=["#0083B8"] * len(ticket_by_subtopics),
    template="plotly_white",
)

fig_ticket_by_subtopics.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)




fig_ticket_by_channel.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


ticket_by_agent = (
    df.groupby(by=["agent"]).count()[["ticket number"]].sort_values(by="ticket number")
)

fig_ticket_by_agent = px.bar(
    ticket_by_agent,
    x="ticket number",
    y=ticket_by_agent.index,
    orientation="h",
    title="<b>tickets by agent</b>",
    color_discrete_sequence=["#0083B8"] * len(ticket_by_agent),
    template="plotly_white",
)

fig_ticket_by_agent.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)








#tickets_close = df.groupby(by=["agent"]).count()[["close date"]]
#fig_tickets_close = px.bar(
#    tickets_close,
#    x=tickets_close.index,
#    y="close date",
#    title="<b>tickets close</b>",
#    color_discrete_sequence=["#0083B8"] * len(tickets_close),
#    template="plotly_white",
#)
#fig_tickets_close.update_layout(
#    xaxis=dict(tickmode="linear"),
#    plot_bgcolor="rgba(0,0,0,0)",
#    yaxis=(dict(showgrid=False)),
#)


#TICKETS BY HOUR [BAR CHART]
tickets_by_date = df.groupby(by=["date"]).count()[["ticket number"]]
fig_tickets_by_date = px.bar(
    tickets_by_date,
    x=tickets_by_date.index,
    y="ticket number",
    title="<b>tickets by date</b>",
    color_discrete_sequence=["#0083B8"] * len(tickets_by_date),
    template="plotly_white",
)
fig_tickets_by_date.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)




left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_ticket_by_sla, use_container_width=True)
left_column.plotly_chart(fig_ticket_lang, use_container_width=True)
right_column.plotly_chart(fig_ticket_by_topics, use_container_width=True)
right_column.plotly_chart(fig_ticket_by_subtopics, use_container_width=True)
left_column.plotly_chart(fig_ticket_by_channel, use_container_width=True)

left_column.plotly_chart(fig_ticket_by_agent, use_container_width=True)
right_column.plotly_chart(fig_tickets_by_date, use_container_width=True)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
        
        
        
        
        
        
        
        
    
            
        



