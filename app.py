import streamlit as st
import pandas as pd
import preprocess,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub
import os

path = kagglehub.dataset_download("heesoo37/120-years-of-olympic-history-athletes-and-results")

file_path_athlete = os.path.join(path, 'athlete_events.csv')
file_path_noc = os.path.join(path, 'noc_regions.csv') 

df = pd.read_csv(file_path_athlete)
region_df = pd.read_csv(file_path_noc)

df = preprocess.preprocess(df,region_df)

st.sidebar.title('Olympic Analysis')
st.sidebar.image('E:\My Work\olympic analysis\download__2_-removebg-preview.png')


user_manual = st.sidebar.radio(
    "Select an option",
    ("Medal Tally", "Overall Analysis", "Country-wise Analysis","Athlete-wise Analysis")
) 

if user_manual == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    years, region = helper.country_year_list(df)
    
    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Region',region)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_manual == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
      
    st.title('Top Stats')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Host Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Year", y="count")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    nations_over_time = helper.data_over_time(df,'Event')
    fig = px.line(nations_over_time, x="Year", y="count")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Year", y="count")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title('No of Events over Time(Every Sport)')
    fig,axis = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0),annot=True)
    st.pyplot(fig)
    
    st.title('Most Successful athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_manual == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df,x='Year',y='Medal')
    st.title(selected_country + ' Medal Tally over the years')
    st.plotly_chart(fig)

    st.title(selected_country + ' excels in following sports')
    pt = helper.country_event_heatmap(df,selected_country)
    fig,axis = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title('Top 5 athletes of ' + selected_country)
    top_5_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top_5_df)

if user_manual == 'Athlete-wise Analysis':

    fig = helper.age_distribution(df)
    fig.update_layout(autosize=False,width=1000,height=500)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    fig = helper.age_distribution_wrt_sport(df)
    fig.update_layout(autosize=False,width=1000,height=500)
    st.title('Distribution of Age wrt Sport')
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    st.title('Height Vs Weight')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_vs_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=50)
    st.pyplot(fig)

    st.title('Men vs Women Participation Over Years')
    final = helper.men_vs_women(df)
    fig = px.line(final,x='Year',y=['Male','Female'])
    st.plotly_chart(fig)




