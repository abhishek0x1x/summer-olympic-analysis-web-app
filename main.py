import streamlit as st
import pandas as pd
import numpy as np
import preprocessing
import helpers
import plotly.express as px
st.set_page_config(layout="wide")
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import scipy



# Loading Dataset
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessing.preprocessor(df, region_df)  # Dataset is now ready for analysis

# Creating Sidebar For Navigation and user_menu
st.sidebar.title("Summer Olympics Analysis")
user_menu = st.sidebar.radio(
    "Select an option",
    ['Medal Tally','Broad Analysis','Country-wise Analysis','Athlete-wise Analysis']
)


# Code for user_menu == 'medal_tally'
# -----------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
if user_menu == 'Medal Tally':
    # creating selectboxes for years and countries
    years = helpers.fetch_years(df)
    countries = helpers.fetch_countries(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",countries)

    # displaying Medal Tally
    medal_tally =  helpers.display_medal_tally(df,selected_year,selected_country)
    st.table(medal_tally)

# Code for user_menu == 'Broad Analysis'
# -------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
if user_menu == 'Broad Analysis':
    editions = df['year'].nunique()
    hosts = df['city'].nunique()
    sports = df['sport'].nunique()
    events = df['event'].nunique()
    athletes = df['id'].nunique()
    nations= df['region'].nunique()
    # ---------------------------------------------
    st.title("Some Statistical Figures")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Editions", value=editions)
    with col2:
        st.metric(label="Hosts", value=hosts)
    with col3:
        st.metric(label="Sports", value=sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Events", value=events)
    with col2:
        st.metric(label="Athletes", value=athletes)
    with col3:
        st.metric(label="Nations", value=nations)
    # -----------------------------------------------
    st.title("Participating Nations Over The Years")

    nations_over_time = df.groupby('year')['region'].nunique().reset_index()
    fig = px.line(nations_over_time, x='year', y='region')
    st.plotly_chart(fig)
    #-------------------------------------------------
    st.title("Total Events Over The Years")

    events_over_time = df.groupby('year')['event'].nunique().reset_index()
    fig = px.line(events_over_time, x='year', y='event',)
    st.plotly_chart(fig)
    #-------------------------------------------------
    st.title("Total Athletes Over The Years")

    athletes_over_time = df.groupby('year')['id'].nunique().reset_index()
    fig = px.line(athletes_over_time, x='year', y='id')
    st.plotly_chart(fig)
    # -------------------------------------------------
    st.title("Sports wise Total Events Over The Years")
    fig, ax = plt.subplots(figsize=(20, 20))

    x = df.drop_duplicates(['year', 'sport', 'event'])
    ax = sns.heatmap(x.groupby(['sport','year'])['event'].count().unstack().fillna(0).astype('int'),annot=True)
    st.pyplot(fig)
    # --------------------------------------------------
    st.title("Most Successful Athletes")

    sports = helpers.fetch_sports(df)
    selected_sport = st.selectbox("Select a Sport",sports)

    successful_athlete = helpers.fetch_most_successful_athlete(df,selected_sport)
    st.table(successful_athlete)

# Code for user_menu == 'Country Wise Analysis'
# -------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
if user_menu == 'Country-wise Analysis':
    countries = helpers.fetch_countries(df)
    del countries[0]

    selected_country = st.sidebar.selectbox("Select Country", countries)

    st.title("Total Medals Over The Years")

    medal_yearwise = df.drop_duplicates(['year', 'season', 'city', 'sport', 'event', 'region', 'medal'])
    medal_yearwise = medal_yearwise[medal_yearwise['region'] == selected_country].groupby(['year'])[
        'medal'].count().reset_index()
    fig = px.line(medal_yearwise, x='year', y='medal')
    st.plotly_chart(fig)

    #---------------------------------------------------
    st.title("Total Medals Over The Years")

    x = df.drop_duplicates(['year', 'season', 'city', 'sport', 'event', 'region', 'medal'])
    x = x[x['region'] == selected_country]

    fig, ax = plt.subplots(figsize=(10, 10))
    ax = sns.heatmap(x.pivot_table(index='sport',columns='year',values='medal', aggfunc='count').fillna(0).
                     astype('int'),annot=True)

    st.pyplot(fig)

    #----------------------------------------------------
    st.title("Top 10 Athletes Country-wise")

    top_10_athletes = helpers.fetch_top_10_athletes(df,selected_country)
    st.table(top_10_athletes)


# for  user_menu == 'Athlete-wise Analysis'
# --------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['id', 'age'])
    x1 = athlete_df['age'].dropna()
    x2 = athlete_df[athlete_df['medal'] == 'Gold']['age'].dropna()
    x3 = athlete_df[athlete_df['medal'] == 'Silver']['age'].dropna()
    x4 = athlete_df[athlete_df['medal'] == 'Bronze']['age'].dropna()

    st.title("Athletes Age Distribution")
    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ['Overall', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
        show_hist=False,
        show_rug=False,
    )
    st.plotly_chart(fig)

#     ---------------------------------------------------------------------------
    x = df.drop_duplicates(subset=['id', 'sex', 'year'])
    male = x[x['sex'] == 'M'].groupby('year')['sex'].count().reset_index()
    female = x[x['sex'] == 'F'].groupby('year')['sex'].count().reset_index()

    merged_mf = male.merge(female, on='year', how='left').fillna(0).astype('int')
    merged_mf.rename(columns={'sex_x': 'male', 'sex_y': 'female'}, inplace=True)

    st.title("Male-Female Participation Over The Years")
    fig = px.line(merged_mf, x='year', y=['male', 'female'])
    st.plotly_chart(fig)











