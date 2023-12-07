import pandas as pd

order = {
    'J': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
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

j_s = df_counts['J']
df_counts = df_counts.drop(columns=['J'])
df_counts_joker = df_counts.apply( lambda x: x+ j_s)

five = df.loc[
    (df_counts_joker==5).any(axis='columns') # you have five counts including jokers
].sort_values([0,1,2,3,4], ascending=False, key= lambda x: x.map(order))

four = df.loc[
    (
        (j_s == 3) &  # you have three jokers
        (df_counts<2).all(axis='columns') # no pairs
    ) |
    ((df_counts_joker==4).sum(axis='columns')==1) # there is exactly one combination of four of a kind with jokers
].sort_values([0,1,2,3,4], ascending=False, key= lambda x: x.map(order))


full = df.loc[
    (
        (j_s==1) & # you have a joker
        ((df_counts==2).sum(axis='columns')==2) # and 2 pairs
    ) |
    (
        (j_s==0) & # dont have a joker
        ((df_counts==3).any(axis='columns')) & # have a three
        ((df_counts==2).any(axis='columns')) # and a two
    )
].sort_values([0,1,2,3,4], ascending=False, key= lambda x: x.map(order))

three = df.loc[
    (
        ((j_s==2)) & # you have 2 jokers
        ((df_counts<2).all(axis='columns')) # and no pairs
    ) |
    (
        (j_s==1) & # you have 1 joker
        (~(df_counts==3).any(axis='columns')) & # no three
        ((df_counts==2).sum(axis='columns')==1) # and 1 pair
    ) |
    (
        (j_s==0) & # you have 0 jokers
        (df_counts==3).any(axis='columns') & # and three of a kind
        (~(df_counts==2).any(axis='columns')) # but no pair
    )
].sort_values([0,1,2,3,4], ascending=False, key= lambda x: x.map(order))

two = df.loc[
    (
        (j_s==0) & # you cannot have a joker
        ((df_counts==2).sum(axis='columns')==2) # and have two pairs
    )
].sort_values([0,1,2,3,4], ascending=False, key= lambda x: x.map(order))

one = df.loc[
    (
        (j_s==1) & # you have a joker
        ((df_counts<2).all(axis='columns')) # no pairs
    ) |
    (
        (j_s==0) & # you have no jokers
        (~(df_counts==3).any(axis='columns')) & # no threes of a kind
        ((df_counts==2).sum(axis='columns')==1) # exactly one pair
    )
].sort_values([0,1,2,3,4], ascending=False, key= lambda x: x.map(order))

high = df[
    (j_s==0) & # no jokers
    (df_counts<2).all(axis='columns') # no pairs
].sort_values([0,1,2,3,4], ascending=False, key= lambda x: x.map(order))

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
