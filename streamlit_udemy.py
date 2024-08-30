import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from numerize.numerize import numerize

st.set_page_config(
    page_title="Udemy Dashboard",
    page_icon="🚀",
    layout="wide",  # This makes the layout wide instead of centered
    initial_sidebar_state="expanded"  # The sidebar is expanded by default
)
df = pd.read_csv("udemy_data_clean.csv")
st.sidebar.header('Udemy Dashboard Filter')
st.sidebar.image('udemy.webp')
st.sidebar.write('This dataset contain information about online courses, from a platform like Udemy.')

years = df['year'].unique().tolist()
years.insert(0, 'All')
selected_year = st.sidebar.selectbox('Select Year', options=years)

dur = df['duration'].unique().tolist()
dur.insert(0,'All')
dur_redio = st.sidebar.selectbox('Choose Duration',options= dur)

pre = df['price_range'].unique().tolist()
pre.insert(0,'All')
pre_redio = st.sidebar.selectbox('Choose Price range ',options= pre)

paid = df['is_paid'].unique().tolist()
paid.insert(0,'All')
paid_redio = st.sidebar.radio('Is Paid?',options= paid)

df_cop = df.copy()

if selected_year != 'All':
    df_cop = df_cop[df_cop['year'] == selected_year]

if dur_redio != 'All':
    df_cop = df_cop[df_cop['duration'] == dur_redio]

if pre_redio != 'All':
    df_cop = df_cop[df_cop['price_range'] == pre_redio]

if paid_redio != 'All':
    df_cop = df_cop[df_cop['is_paid'] == paid_redio] 


col1, col2, col3, col4 = st.columns(4)


with col1:
    total_profit = int(df_cop['profit'].sum())
    #formatted_p = f"{total_profit:,}"
    st.metric("Total Profit",numerize(total_profit))


with col2:
    total_sub = int(df_cop['num_subscribers'].sum())
    #formatted_s = f"{total_sub:,}"
    st.metric("Number of Sebscribers",numerize(total_sub))

with col3:
    total_re = int(df_cop['num_reviews'].sum())
    #formatted_r = f"{total_re:,}"
    st.metric("Number of reviews",numerize(total_re))
with col4:
    total_le = int(df_cop['num_lectures'].sum())
    #formatted_le = f"{total_le:,}"
    st.metric("Number of lactures",numerize(total_le))

st.header('Udemy Data')
st.subheader('you can take a look on sample of dataset and see affective on the data')
st.write(df_cop.head())

c1,c2 = st.columns((5,5))

with c1:

    
    ds = df_cop['subject'].value_counts().reset_index()

    fig1 = px.bar(data_frame= ds,x='count',y='subject',title='Total Number of Each Subject')   

    st.plotly_chart(fig1,use_container_width=True)


    fig2 = px.bar(data_frame=df_cop,
        x =df_cop.groupby('subject')['num_subscribers'].sum().index,
        y = df_cop.groupby('subject')['num_subscribers'].sum().values,title='Total Number of Subscribers by Each Subject',labels={'x':'Subject','y':'Number of Subscribers'} )
    st.plotly_chart(fig2,use_container_widh=True)



    su_le = df_cop.groupby('subject')['level'].value_counts().reset_index()
    fig3 = px.bar(data_frame=su_le,
                x = 'subject',
                y = 'count',
                color = 'level',
                title = 'Total Number for each Subject by level',
                labels={'count': 'Count', 'subject': 'Subject'})

    st.plotly_chart(fig3,use_container_width=True)

with c2:

    dur_sub = df_cop.groupby('subject')['duration'].value_counts().reset_index()

    fig4 = px.bar(dur_sub,
                x='subject',
                y='count',
                color='duration',
                title='Duration Range Counts by Subject',
                labels={'count': 'Count', 'subject': 'Subject','Duration Range': 'Duration Range'},
                )
    st.plotly_chart(fig4,use_container_width=True)




    pri_ran_sub = df_cop.groupby('subject')['price_range'].value_counts().reset_index()
    fig5 = px.bar(pri_ran_sub,
                x='subject',
                y='count',
                color='price_range',
                title='Price Range Counts by Subject',
                labels={'count': 'Count', 'subject': 'Subject','price_range': 'Price Range'},
                )
    st.plotly_chart(fig5,use_container_width=True)

    num_sub = df_cop.groupby('year')['num_subscribers'].sum()
    fig6 = px.line(data_frame=num_sub, x = num_sub.index , y = num_sub.values)
    st.plotly_chart(fig6,use_container_width=True)

sub_of_paid = df_cop.groupby(['year','is_paid'])['num_subscribers'].sum().reset_index()
fig7 = px.line(data_frame=sub_of_paid , x = 'year' , y = 'num_subscribers', color= 'is_paid',color_discrete_map={
True: 'blue',   
False: 'red'    
 })
st.plotly_chart(fig7,use_container_width=True)
