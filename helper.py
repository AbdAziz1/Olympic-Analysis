import numpy as np
import plotly.figure_factory as ff

def medal_tally(df):
    medal_tally =df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

    medal_tally = medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x  

def data_over_time(df, col):

    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')

    nations_over_time.rename(columns={'Year': 'Year', 'Count': col}, inplace=True)

    return nations_over_time

def most_successful(df,sport):  
    
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    x = temp_df['Name'].value_counts().reset_index()
    x.rename(columns={'count':'Medals'},inplace=True)
    x = x.head(5).merge(df,left_on='Name',right_on='Name',how='left')[['Name','Medals','Sport','region']].drop_duplicates('Name')
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df['region']==country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df['region']== country]
    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df,country):  
    
    temp_df = df.dropna(subset=['Medal'])
    
    temp_df = temp_df[temp_df['region'] == country]
    
    x = temp_df['Name'].value_counts().reset_index()
    x.rename(columns={'count':'Medals'},inplace=True)
    x = x.head(5).merge(df,left_on='Name',right_on='Name',how='left')[['Name','Medals','Sport']].drop_duplicates('Name')
    return x

def age_distribution(df):
    temp_df = df.drop_duplicates(subset=['Name','region'])

    x1 = temp_df['Age'].dropna()
    x2 = temp_df[temp_df['Medal']=='Gold']['Age'].dropna()
    x3 = temp_df[temp_df['Medal']=='Silver']['Age'].dropna()
    x4 = temp_df[temp_df['Medal']=='Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4],['Overll Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)

    return fig

def age_distribution_wrt_sport(df):

    athlete_df = df.drop_duplicates(subset=['Name','region'])

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics','Swimming', 'Badminton', 'Sailing', 'Gymnastics','Art Competitions', 'Handball', 'Weightlifting','Wrestling','Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing','Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball','Rhythmic Gymnastics', 'Rugby Sevens','Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    return fig

def weight_vs_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal',inplace = True)
    if sport == 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df  
    else:
        return athlete_df

def men_vs_women(df):

    temp_df = df.drop_duplicates(subset=['Name','region'])

    men  = temp_df[temp_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()

    women  = temp_df[temp_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    final.fillna(0,inplace=True)

    return final