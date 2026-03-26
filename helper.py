def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year',
                                             'Medal', 'City', 'Sport', 'Event'])

    medal_tally = medal_tally.groupby('region').sum()[
        ['Gold', 'Silver', 'Bronze']
    ].sort_values('Gold', ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years, country


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Medal', 'City', 'Sport', 'Event'])

    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df

    if year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
        flag = 1

    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]

    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == year)]

    if flag:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x


def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().sort_index().reset_index()
    nations_over_time.rename(columns={'Year':'year','count':col}, inplace=True)
    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df.groupby('Name').count()['Medal'].sort_values(ascending=False).reset_index()
    x.rename(columns={'Medal': 'total_medals'}, inplace=True)

    x = x.merge(df[['Name', 'region', 'Sport']].drop_duplicates(), on='Name', how='left')

    return x.head(15)


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Medal', 'City', 'Sport', 'Event'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Medal', 'City', 'Sport', 'Event'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index="Sport", columns="Year", values="Medal", aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df.groupby('Name').count()['Medal'].sort_values(ascending=False).reset_index()
    x.rename(columns={'Medal': 'total_medals'}, inplace=True)

    x = x.merge(df[['Name', 'Sport']].drop_duplicates(), on='Name', how='left')

    return x.head(10)














