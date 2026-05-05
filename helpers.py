def fetch_years(df):
    years = df['year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    return years


def fetch_countries(df):
    countries = df['region'].dropna().unique().tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return countries


def display_medal_tally(df, year, region):
    medal_tally = df.drop_duplicates(subset=['team', 'noc', 'games', 'year', 'city', 'sport', 'event', 'medal'])
    if year != 'Overall' and region != 'Overall':
        medal_tally = medal_tally[(medal_tally['year'] == year) & (medal_tally['region'] == region)]
        medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                    ascending=False).reset_index()

    elif region != 'Overall':
        medal_tally = medal_tally[medal_tally['region'] == region]
        medal_tally = medal_tally.groupby('year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                  ascending=False).reset_index()

    elif year != 'Overall':
        medal_tally = medal_tally[medal_tally['year'] == year]
        medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                    ascending=False).reset_index()
    else:
        medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                    ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally


def fetch_sports(df):
    sports = df['sport'].unique().tolist()
    sports.insert(0, 'Overall')
    return sports


def fetch_most_successful_athlete(df,selected_sport):
    x = df.groupby(['id'])['medal'].count().sort_values(ascending=False).reset_index()
    x = df[['id', 'name', 'region', 'sport']].drop_duplicates().merge(x, on='id', how='right').drop(columns=['id'])
    x.rename(columns={'medal': 'total_medals'})

    if selected_sport == 'Overall':
        return x.head(10)
    else:
        return x[x['sport'] == selected_sport].head(10)


def fetch_top_10_athletes(df,selected_country):
    x = df.drop_duplicates(['id', 'year', 'season', 'city', 'sport', 'event', 'region', 'medal'])
    x = x[x['region'] == selected_country]

    x = x.groupby('id')['medal'].count().sort_values(ascending=False).reset_index().head(10)

    x = df[['id', 'name', 'sport']].drop_duplicates().merge(x, on='id', how='right').drop(columns=['id'])
    x.rename(columns={'medal': 'total_medals'}, inplace=True)

    return x.head(10)

