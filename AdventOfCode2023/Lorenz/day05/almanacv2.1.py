import pandas as pd

# opening and reading the lines from the input
with open('./input.txt', 'r') as f:
    lines = f.readlines()

seed_ranges = [int(x) for x in lines[0].split(':')[-1].split(' ') if x != '']

seed_bank = pd.DataFrame(
    zip(seed_ranges[::2], seed_ranges[1::2]),
    columns=['start', 'range']
).sort_values('start')
seed_bank['end'] = seed_bank.start + seed_bank.range -1

mapping = {}
curr_map = None
data = []

for line in lines[2:]:

    if line.endswith(' map:\n'):
        curr_map = line.split(' ')[0]
        continue

    if line == '\n':
        continue

    data.append([curr_map, *[int(x) for x in line[:-1].split(' ')]])

df_map = pd.DataFrame(data, columns=['mapping', 'start_dest', 'start_source', 'range'])


def fill_missing(x):
    x = x.sort_values('start_source')

    x['missing'] = (x.start_source.shift(-1) - (x.start_source + x.range)).fillna(0).astype(int)
    missing = x[x.missing>0].copy()
    missing.start_source += missing.range
    missing.start_dest = missing.start_source
    missing.range = missing.missing

    dfs = [x, missing]
    if x.start_source.min()>0:
        dfs.append(
            pd.DataFrame(
                [[x.mapping.unique()[0], 0, 0, x.start_source.min()]],
                columns=['mapping', 'start_dest', 'start_source', 'range'])
        )

    return pd.concat(dfs).drop(columns=['missing']).sort_values('start_source')

df_map = df_map.groupby('mapping').apply(fill_missing)

df_map['end_source'] = df_map.start_source + df_map.range - 1
df_map['end_dest'] = df_map.start_dest + df_map.range - 1
df_map['delta'] = df_map.start_dest - df_map.start_source

sequence = [
    'seed-to-soil',
    'soil-to-fertilizer',
    'fertilizer-to-water',
    'water-to-light',
    'light-to-temperature',
    'temperature-to-humidity',
    'humidity-to-location',
]


def propagate(x, mapping):
    filter_map = mapping[
        mapping.start_source.between(x.start, x.end) |  # starts in map
        ((mapping.start_source <= x.start) & (mapping.end_source >= x.end)) |  # completely overlaps
        mapping.end_source.between(x.start, x.end)  # ends in map
        ]
    return pd.DataFrame(
        {
            'start': filter_map.start_source.clip(lower=x.start) + filter_map.delta,
            'end': filter_map.end_source.clip(upper=x.end) + filter_map.delta
        }
    )


df = seed_bank.drop(columns=['range'])

for step in sequence:
    df = pd.concat(
        df.apply(
            lambda x: propagate(
                x,
                df_map.loc[step].sort_values('start_source')),
            axis='columns'
        ).values.tolist()
    )

print(df.start.min())