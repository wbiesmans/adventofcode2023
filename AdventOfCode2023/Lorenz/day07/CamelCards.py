import pandas as pd

order = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}
df = pd.read_csv('./input.txt', sep=' ', header=None)
df.columns = ['hand', 'bid']

df = pd.concat(
    [
        df,
        df.hand.apply(lambda x: pd.Series([*x])),
    ],
    axis='columns'
)

df_counts = df.apply(lambda x: pd.Series([*x.hand]).value_counts(), axis='columns').fillna(0.0)

five = df[(df_counts==5).any(axis='columns')].sort_values([0,1,2,3,4], ascending=False, key= lambda x: x.map(order))
four = df[(df_counts==4).any(axis='columns')].sort_values([0,1,2,3,4], ascending=False, key= lambda x: x.map(order))
full = df[(df_counts==3).any(axis='columns') & (df_counts==2).any(axis='columns')].sort_values([0,1,2,3,4], ascending=False, key= lambda x: x.map(order))
three = df[(df_counts==3).any(axis='columns') & ~(df_counts==2).any(axis='columns')].sort_values([0,1,2,3,4], ascending=False, key= lambda x: x.map(order))
two = df[(df_counts==2).sum(axis='columns')==2].sort_values([0,1,2,3,4], ascending=False, key= lambda x: x.map(order))
one = df[~(df_counts==3).any(axis='columns') &(df_counts==2).sum(axis='columns')==1].sort_values([0,1,2,3,4], ascending=False, key= lambda x: x.map(order))
high = df[(df_counts<2).all(axis='columns')].sort_values([0,1,2,3,4], ascending=False, key= lambda x: x.map(order))

df_hands_ordered = pd.concat(
    [
        five,
        four,
        full,
        three,
        two,
        one,
        high,
    ]
)
df_hands_ordered['rang'] = list(range(1, df_hands_ordered.shape[0]+1))[::-1]
print((df_hands_ordered.bid * df_hands_ordered.rang).sum())