
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import openpyxl as op
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import plotly.figure_factory as ff
import streamlit as st  # pip install streamlit
import streamlit.components.v1 as components


#import pdfkit
#from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
#from datetime import date
#from streamlit.components.v1 import iframe


#components.html(""" """, height=100,)

st.set_page_config(
page_title = "Everyone Can Support",
page_icon = ":phone:",
#initial_sidebar_state="expanded",
)

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
#st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache(allow_output_mutation=True)
def get_data_from_excel():
    df = pd.read_excel(
        io="reports/Report_status_2023-01-03_2023-01-09_1673351175.xlsx",
        engine="openpyxl",
        #sheet_name="",
        skiprows=0,
        #usecols="B:R",
        #nrows=1000,
    )
    
    # Add 'hour' column to dataframe
    #df["hour"] = pd.to_datetime(df["receiving time"]).dt.hour
    return df



def get_data_from_excel1():
    dfs = pd.read_excel(
        io="reports/efective-solution/Efective_solution_2022-12-27_2023-01-02.xlsx",
        engine="openpyxl",
        #sheet_name="",
        skiprows=0,
        #usecols="B:R",
        #nrows=1000,
    )
    
    # Add 'hour' column to dataframe
    #df["hour"] = pd.to_datetime(df["receiving time"]).dt.hour
    return dfs



dfs = get_data_from_excel1()
df = get_data_from_excel()
st.subheader("Dashboard")
st.text("Report_status_2023-01-03_2023-01-09_1673351175.xlsx")



# ---- SIDEBAR ----

st.markdown("""---""")


with st.expander("Efective solution >= 60 minutes (? Tickets) NM Brazil"):
    st.text("?.xlsx")
    st.dataframe(dfs) 

with st.expander("Efective solution >= 60 minutes (? Tickets) NM Latam"):
    st.text("?.xlsx")
    

with st.expander("Efective solution >= 60 minutes (? Tickets) NM Indonesian"):
    st.text("?")
    
    
with st.expander("Efective solution >= 60 minutes (? Tickets) NM English"):
    st.text("?.xlsx")    



st.markdown("""---""")



#st.sidebar.header("Please filter Here:")

#language = st.sidebar.multiselect(
#    "Select the language:",
#    options=df["language"].unique(),
#    default=df["language"].unique()
#)
#
#
#df = df.query(
#            "language == @language"
#        )


with st.form("my_form"):
    language = st.multiselect(
    "Select the language:",
    options=df["language"].unique(),
    default=df["language"].unique()
)
    submitted = st.form_submit_button("Submit")
    if submitted:
        df = df.query(
            "language == @language"
        )
        
    else:
        st.stop()
         
        
#import time

#my_bar = st.progress(0)

#for percent_complete in range(100):
#    time.sleep(0.09)
#    my_bar.progress(percent_complete + 1)

        
        # ---- MAINPAGE ----

#st.text("Report_status_2022-12-13_2022-12-19_1671546653.xlsx")
st.markdown("##")

# TOP KPI's
total_tickets = len(df)


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
     
    if time <= '00:05:00':
        return '5 minutes'
    elif time <= '00:15:00':
        return '15 minutes'
    elif time <= '00:30:00':
        return '30 minutes'
    elif time <= '00:45:00':
        return '45 minutes'
    elif time <= '01:00:00':
        return '60 minutes'
    elif time <= '23:59:00':
        return '61 minutes and more'
    else:
        return 'неизвестно'


df['sla cat'] = df['date of the first response'].apply(sla_category)



sla5 = df[df['sla cat'] == '5 minutes']['sla cat'].count()


sla55 = df[df['sla cat'] == '5 minutes']['sla cat'].count()
#print(sla55)

#display(HTML(f"<li><span> SLA 5 minutes met {sla55} tickets, which is {sla55 / len(l):.0%}.</li></span>"))





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

st.markdown("""---""")


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Tickets:")
    st.subheader(f"{total_tickets}")
with middle_column:
    st.subheader("First response")
    st.subheader(f"{meantime_str}")
with right_column:
    st.subheader("5 min SLA")
    st.subheader(f"{sla55 / len(df):.0%}")
    
    
    
    
    


#st.dataframe(data=dfs, width=300, height=300, use_container_width=True)




#[BAR CHART]


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
    x=ticket_lang.index,
    y="ticket number",
    text="ticket number",
    orientation="v",
    title="<b>Ticket by lang</b>",
    color_discrete_sequence=["#0083B8"] * len(ticket_lang),
    template="plotly_white",
)

fig_ticket_lang.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)




ticket_by_sla = (
    df.groupby(by=["sla cat"]).count()[["ticket number"]].sort_values(by="ticket number")
)

fig_ticket_by_sla = px.scatter(
    ticket_by_sla,
    x=ticket_by_sla.index,
    y="ticket number",
    orientation="v",
    title="<b>Tickets by sla</b>",
    color_discrete_sequence=["#0083B8"] * len(ticket_by_sla),
    template="plotly_white",
)

fig_ticket_by_sla.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

ticket_by_channel = (
    df.groupby(by=["ticket channel"]).count()[["ticket number"]].sort_values(by="ticket number")
)

fig_ticket_by_channel = px.bar(
    ticket_by_channel,
    x=ticket_by_channel.index,
    y="ticket number",
    text="ticket number",
    orientation="v",
    title="<b>Tickets by channel</b>",
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
    elif cat == 'Organizational questions':
        return 'organizational questions'
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
    x=ticket_by_topics.index,
    y="ticket number",
    text="ticket number",
    orientation="v",
    title="<b>Tickets by topic</b>",
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
    x=ticket_by_subtopics.index,
    y="ticket number",
    text="ticket number",
    orientation="v",
    title="<b>Tickets by subtopic</b>",
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
    x=ticket_by_agent.index,
    y="ticket number",
    text="ticket number",
    orientation="v",
    title="<b>Tickets by agent</b>",
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


st.plotly_chart(fig_ticket_lang, use_container_width=True)
st.plotly_chart(fig_ticket_by_channel, use_container_width=True)
st.plotly_chart(fig_ticket_by_topics, use_container_width=True)
st.plotly_chart(fig_ticket_by_subtopics, use_container_width=True)
st.plotly_chart(fig_ticket_by_agent, use_container_width=True)

st.text( f"Tickets by SLA:")




pivot = pd.pivot_table(df, index='agent', columns='sla cat', values='date of the first response', aggfunc='count')

pivot['total'] = pivot.sum(axis=1)

column_order = ['5 minutes', '15 minutes', '30 minutes', '45 minutes','60 minutes','61 minutes and more','total']

pivot = pivot.reindex(column_order, axis=1)

pivot['5 minutes'] = (pivot['5 minutes'] / pivot['total']).round(2)
pivot['15 minutes'] = (pivot['15 minutes'] / pivot['total']).round(2)
# посчитать долю тикетов за 30 минут по отношению к столбцу total и округлить до 2 знаков после запятой
pivot['30 minutes'] = (pivot['30 minutes'] / pivot['total']).round(2)
pivot['45 minutes'] = (pivot['45 minutes'] / pivot['total']).round(2)
pivot['60 minutes'] = (pivot['60 minutes'] / pivot['total']).round(2)
# посчитать долю тикетов за 60+ по отношению к столбцу total и округлить до 2 знаков после запятой
pivot['61 minutes and more'] = (pivot['61 minutes and more'] / pivot['total']).round(2)
#pivot['неизвестно'] = pivot['неизвестно']

column_order = ['5 minutes', '15 minutes', '30 minutes', '45 minutes','60 minutes','61 minutes and more','total']
# подписать таблицу
pivot.columns.name = 'agent/first response'
# отсортировать таблицу по колонке 10 минут — у кого выше доля, тот окажется выше в топе
pivot.sort_values(by='5 minutes', ascending=False, inplace=True)
# заполнить пустые значения 0
pivot = pivot.fillna(0)

pivot = pivot\
.style.format('{:.0%}')\
.format('{:.0f}', subset=['total'])\
.background_gradient(cmap='ocean_r')

st.dataframe(pivot)



st.plotly_chart(fig_ticket_by_sla, use_container_width=True)

st.text( f"Tickets by close date:")


df['close date'] = df['close date'].apply(
    pd.to_numeric, errors='ignore')

    

df['close date'] = df['close date'].astype('str').str[-8:]



def sla_category(time):
     
    if time <= '0:10:00':
        return '10 minutes'
    elif time <= '0:30:00':
        return '30 minutes'
    elif time <= '0:45:00':
        return '45 minutes'
    elif time <= '1:00:00':
        return '60 minutes'
    elif time <= '23:59:00':
        return '61 minutes and more'
    else:
        return 'неизвестно'


df['topics close'] = df['close date'].apply(sla_category)


pivot = pd.pivot_table(df, index='topics', columns='topics close', values='ticket number', aggfunc='count')
pivot = pivot.fillna(0)
pivot['total'] = pivot.sum(axis=1)

column_order = ['10 minutes','30 minutes','45 minutes','60 minutes','61 minutes and more','неизвестно','total']

pivot = pivot.reindex(column_order, axis=1)

pivot['10 minutes'] = (pivot['10 minutes'] / pivot['total'])
#pivot['20 minutes'] = (pivot['20 minutes'] / pivot['total'])
#pivot['15 минут'] = (pivot['15 минут'] / pivot['total']) + pivot['10 минут']
pivot['30 minutes'] = (pivot['30 minutes'] / pivot['total'])
pivot['45 minutes'] = (pivot['45 minutes'] / pivot['total'])
pivot['60 minutes'] = (pivot['60 minutes'] / pivot['total'])
pivot['61 minutes and more'] = (pivot['61 minutes and more'] / pivot['total'])
pivot['неизвестно'] = (pivot['неизвестно'] / pivot['total'])

#pivot.drop('ticket number', inplace=True, axis=1);
pivot.sort_values(by='10 minutes', ascending=False, inplace=True)
pivot = pivot.fillna(0)



pivot = pivot.style.format('{:.0%}')\
.format('{:.0f}', subset=['total'])\
.background_gradient(cmap='ocean_r', subset=['10 minutes',	'30 minutes',	'45 minutes',	'60 minutes',	'61 minutes and more','неизвестно','total'])


st.dataframe(pivot)


st.text( f"Topics filter:")


def sla_category(cat):
     
    if cat == 'Int Other':
        return 'other'
    if cat == 'Int Homework questions':
        return 'Homework questions'
    if cat == 'Int Marketing':
        return 'Marketing'
    if cat == 'Int Organizational Issues':
        return 'Organizational Issues'
    if cat == 'Int Payments':
        return 'Payments'
    if cat == 'Int Refunds':
        return 'Refunds'
    if cat == 'Int Product':
        return 'Product'
    if cat == 'Int Technical issues':
        return 'Technical issues'
    if cat == 'Organizational questions':
        return 'Organizational questions'
    if cat == 'Platform bugs':
        return 'Platform bugs'
    if cat == 'Reactions in SM (Social Media)':
        return 'Reactions in SM (Social Media)'
    
    else:
        return 'неизвестно'


df['topics_filter'] = df['topics'].apply(sla_category)



pivot = pd.pivot_table(df, index='agent', columns='topics_filter', values='close date', aggfunc='count')
pivot = pivot.fillna(0)
pivot['total'] = pivot.sum(axis=1)



column_order = ['Reactions in SM (Social Media)','Platform bugs','Organizational questions','Technical issues','Product','Refunds','Payments','Organizational Issues','Marketing','Homework questions','other','неизвестно','total']

pivot = pivot.reindex(column_order, axis=1).sort_values(by=column_order, ascending=True)

pivot.sort_values(by='total', ascending=False, inplace=True)
#pivot['other'] = (pivot['other'] / pivot['total'])

#pivot.drop('ticket number', inplace=True, axis=1);
pivot = pivot.fillna(0)
pivot = pivot.style.format('{:.0f}')\
.format('{:.0f}', subset=['total'])\
.background_gradient(cmap='ocean_r', subset=['Reactions in SM (Social Media)','Platform bugs','Organizational questions','Technical issues','Product','Refunds','Payments','Organizational Issues','Marketing','Homework questions','other','неизвестно','total'])


st.dataframe(pivot)

st.text( f"Tickets by hour:")


pivot = pd.pivot_table(df, index='hour', columns='sla cat', values='ticket number', aggfunc='count')
pivot = pivot.fillna(0)
pivot['total'] = pivot.sum(axis=1)

column_order = ['5 minutes', '15 minutes','30 minutes','45 minutes','60 minutes','61 minutes and more','total']

pivot = pivot.reindex(column_order, axis=1)


pivot['5 minutes'] = (pivot['5 minutes'] / pivot['total'])
pivot['15 minutes'] = (pivot['15 minutes'] / pivot['total'])
#pivot['15 минут'] = (pivot['15 минут'] / pivot['total']) + pivot['10 минут']
pivot['30 minutes'] = (pivot['30 minutes'] / pivot['total'])
pivot['45 minutes'] = (pivot['45 minutes'] / pivot['total'])
pivot['60 minutes'] = (pivot['60 minutes'] / pivot['total'])
pivot['61 minutes and more'] = (pivot['61 minutes and more'] / pivot['total'])
pivot.drop('total', inplace=True, axis=1);
#pivot.sort_values(by='5 minutes', ascending=False, inplace=True)
pivot = pivot.fillna(0)
pivot = pivot.style.format('{:.0%}')\
.background_gradient(cmap='ocean_r', subset=['5 minutes',	'15 minutes','30 minutes','45 minutes','60 minutes',	'61 minutes and more'])

st.dataframe(pivot)






chart_data = pivot

st.area_chart(chart_data)






names = sorted([
    'Roxana Hernández',
    'Christian Sanchez',
    'Ivan Polyakov',
    'Fabián Socha',
    'Lisedt Rengifo',
    'Dina Natasha',
    'Bayu Wicaksono',
    'Bella Eka Syahputri',
    'Julio Johanes',
    'Windra Fortian',
    'Irina Savenkova',
    'Njeungue Wandji',
    'Ahmed Khalifa',
    'Ivan Ustyuzhaninov',
    'Elizaveta Toporova',
    'Jefferson Brito',
    'Mariana Smirnova'
])





data = []
for i in names:
    temp = df[df['agent'] == i]
    time = temp['date of the first response'].median()
    if not time:
        continue
    mins = time.total_seconds() // 60
    data.append([i, time, ])

def change_timedelta_to_normal_float(fl):
    m = fl // 60
    m = '0' + str(int(m)) if m < 10 else str(int(m))
    secs = fl % 60
    secs = '0' + str(int(secs)) if secs < 10 else str(int(secs))
    return f'{m}:{secs}'
        
data = pd.DataFrame(columns=['agent', 'time'], data=data).set_index('agent')
data['time'] = data['time'].dt.total_seconds().fillna(0)

#print(data['time'])

data['human'] = data['time'].apply(change_timedelta_to_normal_float)



fig_sla_by_agent = px.bar(
    data,
    x=data.index,
    y='time',
    text=data['human'],
    title="<b>SLA by Agent</b>",
    color_discrete_sequence=["#0083B8"] * len(data),
    template="plotly_white",
)
fig_sla_by_agent.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


st.plotly_chart(fig_sla_by_agent, use_container_width=True)






df['date'] = df['date'].apply(
    pd.to_numeric, errors='ignore')
    
df['date'] = df['date'].astype('str').str[-8:]


def date_category(bad_date):
     
    if bad_date < '23-01-03':
        return 'date out of frame'   
    else:
        return 'date on frame'

df['+date'] = df['date'].apply(date_category)
df5 = df.loc[df['+date'].isin(['date out of frame'])]
df6 = df.loc[df['+date'].isin(['date on frame'])]


st.text(f"Heatmap by date:")


pivot = pd.pivot_table(df6, index='date', columns='hour', values='ticket number', aggfunc='count')
pivot.fillna(0, inplace=True)
#pivot.sort_values(by='total', ascending=False, inplace=True)

piv =  px.imshow(pivot)

st.plotly_chart(piv, theme=None)

#HEATMAP

#pivot = pivot.style.format('{:.0}')\
#.format('{:.0f}')\
#.background_gradient(cmap='ocean_r')



#st.dataframe(pivot)



#fig = px.imshow(pivot)


#st.dataframe(pivot)




tickets_by_date = df6.groupby(by=["date"]).count()[["ticket number"]]
fig_tickets_by_date = px.bar(
    tickets_by_date,
    x=tickets_by_date.index,
    y="ticket number",
    text="ticket number",
    title="<b>Tickets by date</b>",
    color_discrete_sequence=["#0083B8"] * len(tickets_by_date),
    template="plotly_white",
)
fig_tickets_by_date.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_tickets_by_date, use_container_width=True)




temp = df6[df6['hour'].isin(range(10, 22))]

pivot = pivot = pd.pivot_table(temp, index='date', values='+date', aggfunc='count')


tickets_by_date = temp.groupby(by=["date"]).count()[["ticket number"]]
fig_tickets_by_date = px.bar(
    tickets_by_date,
    x=tickets_by_date.index,
    y="ticket number",
    text="ticket number",
    title="<b>Tickets by day shift</b>",
    color_discrete_sequence=["#0083B8"] * len(tickets_by_date),
    template="plotly_white",
)
fig_tickets_by_date.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_tickets_by_date, use_container_width=True)




temp = df6[df6['hour'].isin([22, 23, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])]
pivot = pivot = pd.pivot_table(temp, index='date', values='+date', aggfunc='count')


tickets_by_date = temp.groupby(by=["date"]).count()[["ticket number"]]
fig_tickets_by_date = px.bar(
    tickets_by_date,
    x=tickets_by_date.index,
    y="ticket number",
    text="ticket number",
    title="<b>Tickets by day night shift</b>",
    color_discrete_sequence=["#0083B8"] * len(tickets_by_date),
    template="plotly_white",
)
fig_tickets_by_date.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_tickets_by_date, use_container_width=True)


df7 = df5[['ticket number','receiving time','agent','topics','subtopics']]



st.text( f"Tickets receiving time out of actual time-frame: {len(df7)}")


df7.sort_values(by='agent', ascending=True, inplace=True)

st.dataframe(df7)

st.text(f"Tickets with sla +5 minutes")

df['date of the first response'] = df['date of the first response'].apply(
    pd.to_numeric, errors='ignore')

    
df['date of the first response'] = df['date of the first response'].astype('str').str[-8:]

def sla_category(bad_time):
     
    if bad_time <= '00:05:00':
        return '5 minutes'
    elif bad_time <= '00:15:00':
        return '15 minutes'
    elif bad_time <= '00:30:00':
        return '30 minutes'
    elif bad_time <= '00:45:00':
        return '45 minutes'
    elif bad_time <= '01:00:00':
        return '60 minutes'
    elif bad_time <= '23:59:00':
        return '61 minutes and more'   
    else:
        return 'неизвестно'

df['+5'] = df['date of the first response'].apply(sla_category)
df8 = df.loc[df['+5'].isin(['15 minutes', '30 minutes', '45 minutes', '60 minutes','61 minutes and more'])]

df10 = df8[['ticket number','agent','topics', 'subtopics', '+5']]

st.text( f"Total tickets with sla +5 minutes: {len(df10)}")

df10.sort_values(by='agent', ascending=True, inplace=True)

st.dataframe(df10)



pivot = pd.pivot_table(df8, index='agent', values='+5',aggfunc='count')
pivot.sort_values(by='+5', ascending=True, inplace=True)
pivot = pivot.style.format('{:.0}')\
.format('{:.0f}', subset=['+5'])\
.background_gradient(cmap='ocean_r', subset=['+5'])

st.dataframe(pivot)



#st.write(
#    "Take your pdf here"
#)


#env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
#template = env.get_template("template.html")


#grade = form.slider("Grade", 1, 100, 60)
#submit = form.form_submit_button("Generate PDF")

#if submit:
#    html = template.render(
#        student=student,
#        course=course,
#        grade=f"{grade}/100",
#        date=date.today().strftime("%B %d, %Y"),
#    )

#    pdf = pdfkit.from_string(html, False)


#    right.success("🎉 Your report was generated!")
    # st.write(html, unsafe_allow_html=True)
    # st.write("")
#    right.download_button(
#        "⬇️ Download PDF",
#        data=pdf,
#        file_name="report.pdf",
#        mime="application/octet-stream",
#    )


#import warnings

#with warnings.catch_warnings():
#    warnings.simplefilter("ignore", category=RuntimeWarning)
#    foo = np.nanmean(df)




# ---- HIDE STREAMLIT STYLE ----



hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)  
        
    
            
        



