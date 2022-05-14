import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
from bokeh.plotting import figure
from bokeh.models import Title
with st.echo(code_location='below'):

    st.write(f"## In this project we use datasets on Indonesian food preferences, India power capacity, and body measurements")

    df6=pd.read_csv("https://raw.githubusercontent.com/temporarywarlord/streamlit-hw/master/DATASET_cultural%20dimension%20of%20food%20consumption.csv")
    df20=df6.iloc[:, 0].str.split(';', expand=True)
    t=df6.columns.values
    t=t.tolist()[0].split(';')
    df20=df20.rename(lambda x: t[x], axis=1)
    df6=df20

    if st.checkbox('Show raw data', key=101):
        st.subheader('Raw data')
        df6

    st.write("Let's start with a dataset on food preferences in Indonesia. Here, we will see what impacts food decisions for different groups of people.")

    t=list(df6.columns.values)
    indonvalues=[]
    indontypes=[]
    for string in t:
        if string[:2]=='(E' or string[:2]=='(D' or string[:3]=='(24' or string[:3]=='(25':
            indonvalues.append(string)
        if string[:2]=='(B':
            indontypes.append(string)

    typesel=st.multiselect('What types of people are you interested in?', indontypes, key=101)
    valuesel=st.multiselect('What things about types of people are you interested in?', indonvalues, key=102)

    for type in typesel:
        for value in valuesel:
            fign=alt.Chart(df6).mark_bar().encode(
        x=alt.X(value, aggregate='count', type='quantitative', stack="normalize"),
        y=alt.Y(type, type='nominal'),
        color=value
    ).properties(
    width=600
    )
            st.altair_chart(fign)

    months_list=["19January", "19Febuary", "19March", "19April", "19May", "19June", "19July", "19August", "19September", "19October", "19November", "19December","20January", "20Febuary", "20March", "20April", "20May", "20June", "20July", "20August", "20September", "20October", "20November", "20December","21January", "21Febuary", "21March", "21April", "21May", "21June", "21July", "21August", "21September", "21October", "21November", "21December", "22January"]
    monthseries=pd.Series(months_list)
    monthslist2=["2019-01", "2019-02", "2019-03", "2019-04", "2019-05", "2019-06", "2019-07", "2019-08", "2019-09", "2019-10", "2019-11", "2019-12", "2020-01", "2020-02", "2020-03", "2020-04", "2020-05", "2020-06", "2020-07", "2020-08", "2020-09", "2020-10", "2020-11", "2020-12", "2021-01", "2021-02", "2021-03", "2021-04", "2021-05", "2021-06", "2021-07", "2021-08", "2021-09", "2021-10", "2021-11", "2021-12", "2022-01", ]

    st.write(f"## Now, let's move on to power capacity of India. Here we'll start with the question - what sources of energy does India use and how has their total amount and their share changed over the last three years?")

    df2=pd.read_csv("https://raw.githubusercontent.com/temporarywarlord/streamlit-hw/master/All%20India%20Installed%20Capacity.csv")

    df2=df2.drop(['month'], axis=1)
    df2=df2.T
    df2=df2.rename(lambda x: monthslist2[x], axis=1)
    df2=df2.reset_index()

    df2=pd.melt(df2, id_vars='index', var_name='month', value_name='capacity')

    highlight = alt.selection(type='single', on='mouseover',
                          fields=['index'], nearest=True) ###FROM: https://altair-viz.github.io/gallery/multiline_highlight.html

    base = alt.Chart(df2).encode(
    x='month:N',
    y='capacity:Q',
    color='index:N'
    )

    points = base.mark_circle().encode(
    opacity=alt.value(0)
    ).add_selection(
    highlight
    ).properties(
    width=600
    )

    lines = base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3))
    )

    st.altair_chart(points + lines) ###END FROM https://altair-viz.github.io/gallery/multiline_highlight.html

    st.write("So we've looked into its main sources of energy - but what specific kinds of renewable energy does India have?")

    df1=pd.read_csv("https://raw.githubusercontent.com/temporarywarlord/streamlit-hw/master/All%20India%20Installed%20Capacity(RES).csv")

    df1=df1.drop(['Month'], axis=1)
    df1['Month']=monthseries
    if st.checkbox('Show raw data', key=102):
        st.subheader('Raw data')
        df1

    df1dropped=df1.drop(['Month', "ID"], axis=1)
    df1Tdropped=df1dropped.T
    df1Tdropped=df1Tdropped.rename(lambda x: monthslist2[x], axis=1)

    arg2=st.select_slider(label='What month do you want to see?', options=monthslist2, key=2)
    df1TdroppedInd=df1Tdropped.reset_index(level=0)

    fig2=px.pie(df1TdroppedInd[[arg2, "index"]], values=arg2, names="index")
    st.plotly_chart(fig2)

    df3=pd.read_csv("https://raw.githubusercontent.com/temporarywarlord/streamlit-hw/master/installed-capacity%20sectorwise.csv")
    df3dropped=df3.drop(['Month and Year'], axis=1)
    df3Tdropped=df3dropped.T

    df3TdroppedInd=df3Tdropped.reset_index(level=0)

    df3Tdropped=df3Tdropped.rename(lambda x: months_list[x], axis=1)

    st.write(f"## Who creates new energy - central government, state governments, or private companies?")
    if st.checkbox('Show raw data', key=103):
        st.subheader('Raw data')
        df3TdroppedInd
    df3Tdropped=df3Tdropped.reset_index(level=0)

    t=pd.melt(df3Tdropped[['index', "19January", "22January"]], id_vars=['index'], var_name='Month', value_name='power-capacity')

    fig4=alt.Chart(t).mark_bar().encode(
    alt.Column('index'), alt.X('Month'),
    alt.Y('power-capacity', axis=alt.Axis(grid=False)),
    alt.Color('Month')
    ).properties(width=80)
    st.altair_chart(fig4)
    st.write("As we can see, it was the private sector that introduced the most new energy.")

    df4=pd.read_csv("https://raw.githubusercontent.com/temporarywarlord/streamlit-hw/master/Installed%20Capacity%20State%20wise.csv")

    df4['non-res']=df4['grand_total']-df4['res']

    st.write(f"## Logarythmic growth of renewable and non-renewable energy in indian states, dynamics")

    if st.checkbox('Show raw data', key=104):
        st.subheader('Raw data')
        df4

    fig7=px.scatter(df4, x='res', y='non-res', animation_frame='month', animation_group='state', color='region', hover_name='state', log_x=True, size_max=55)
    st.plotly_chart(fig7)

    st.write('Here, it becomes even more visible that almost the entire energetic growth for India in the last three years came from using renewables.')

    df10=pd.read_csv("https://raw.githubusercontent.com/temporarywarlord/streamlit-hw/master/Body%20Measurements%20_%20original_CSV.csv")
    n=df10.columns.values

    st.write(f"## The third dataset is about different measurements of people.")

    st.write('You can choose what measurements you want to see regressions of, and what gender you want to compare. Age is >=16')

    r=st.selectbox(label='Gender', options=['male', 'female', 'both'])
    if r=='male':
        df10 = df10.loc[df10['Gender']==1]
    if r=='female':
        df10 = df10.loc[df10['Gender'] == 2]
    df10=df10.loc[df10['Age']>15]
    d=st.selectbox(label='', options=n[2:len(n)], key=200)
    f=st.selectbox(label='', options=n[2:len(n)], key=201)

    x=df10[d] ### FROM: https://stackoverflow.com/questions/54603873/bokeh-plot-regression-lines-on-scatter-plot
    y=df10[f]
    par = np.polyfit(x, y, 1, full=True)
    slope=par[0][0]
    intercept=par[0][1]
    y_predicted = [slope*i + intercept  for i in x]

    fig10=figure()
    fig10.circle(x,y)
    fig10.line(x,y_predicted,color='red',legend='y='+str(round(slope,2))+'x+'+str(round(intercept,2))) ###END FROM https://stackoverflow.com/questions/54603873/bokeh-plot-regression-lines-on-scatter-plot
    fig10.add_layout(Title(text=d, align="center"), "below")
    fig10.add_layout(Title(text=f, align="center"), "left")
    st.bokeh_chart(fig10)

    st.write("Datasets are taken from here (https://www.kaggle.com/datasets/ramjasmaurya/indias-power-capacity?select=All+India+Installed+Capacity%28RES%29.csv), here (https://www.kaggle.com/datasets/saurabhshahane/food-consumption-in-indonesia?select=DATASET_cultural+dimension+of+food+consumption.xlsx), and here (https://www.kaggle.com/datasets/saurabhshahane/body-measurements-dataset)")
    st.write(f"## That's all folks!")
