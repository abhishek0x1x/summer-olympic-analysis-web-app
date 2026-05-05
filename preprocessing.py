import pandas as pd


def preprocessor(df,region_df):
    df = df[df['Season'] == 'Summer']

    df = df.merge(region_df, on='NOC', how='left')

    df = df.drop(columns=['Height', 'Weight', 'notes'])

    df.columns = df.columns.str.lower()

    df.drop_duplicates(inplace=True)

    dummies_medal = pd.get_dummies(df['medal'], dtype=int)
    df = pd.concat([df, dummies_medal], axis=1)

    return df
