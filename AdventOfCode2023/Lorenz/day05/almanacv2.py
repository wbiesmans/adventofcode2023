import logging

import pandas as pd

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(relativeCreated)6d %(threadName)s %(levelname)-8s %(message)s')

# opening and reading the lines from the input
with open('./input.txt', 'r') as f:
    lines = f.readlines()

seed_ranges = [int(x) for x in lines[0].split(':')[-1].split(' ') if x != '']

seed_bank = pd.DataFrame(
    zip(seed_ranges[::2], seed_ranges[1::2]),
    columns=['start', 'range']
).sort_values('start')


class FoundException(Exception):
    def __init__(self, seed_id):
        self.seed_id = seed_id
        self.message = f'found seed with id: {seed_id}'
        super().__init__(self.message)

class Slice(object):
    def __init__(self, type, start, end):
        self.type = type
        self.start = start
        self.end = end

    def lookup(self, df_map):
        if self.type == 'seed':
            # check if this slice starts in a slice from the seed bank
            seed_slice = seed_bank[seed_bank.start<self.start].iloc[-1]
            if seed_slice.start+seed_slice.range > self.start:
                raise FoundException(self.start)
            # check if a slice from the seed bank starts in this slice
            seed_slice = seed_bank[seed_bank.start > self.start].iloc[0]
            if seed_slice.start < self.end:
                raise FoundException(seed_slice.start)
        else:
            logger.info(self)
            mapping = df_map.loc[df_map.mapping.str.endswith(self.type)]
            to, _, current = mapping.mapping.unique()[0].split('-')

            single_map = mapping[(mapping.start_dest<=self.start) & (mapping.end_dest>=self.end)]
            if single_map.empty:
                multi_map = mapping[
                    mapping.start_dest.between(self.start, self.end) |
                    mapping.end_dest.between(self.start, self.end)
                ]
                next_list = []
                for idx, slice in multi_map.iterrows():
                    next_list.append(
                        Slice(type=to, start=max(self.start, slice.start_dest)-slice.delta, end=min(self.end, slice.end_dest)-slice.delta)
                    )
            else:
                single_map = single_map.iloc[0]
                next_list = [Slice(type=to, start=self.start-single_map.delta, end=self.end-single_map.delta)]

            if len(next_list) == 0:
                print()
            for x in next_list:
                x.lookup(df_map)

    def __repr__(self):
        return f'{self.type} - start: {self.start} - end: {self.end}'

def decode(x, mapping):
    map = mapping[(mapping.start_source<=x) & (mapping.end_source>=x)]
    if map.empty:
        return x
    else:
        # we assume there is only one correct map in the filter
        return x + map.iloc[0].delta

def encode(x, mapping):
    map = mapping[(mapping.start_dest<=x) & (mapping.end_dest>=x)]
    if map.empty:
        return x
    else:
        # we assume there is only one correct map in the filter
        return x - map.iloc[0].delta


# for start, length in zip(seed_ranges[::2], seed_ranges[1::2]):
#     seeds.append(Slice('seed', start, length))

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

df = pd.DataFrame({'location': range(1_000)})

locations = df_map[df_map.mapping == 'humidity-to-location'].sort_values(by='start_dest')
locations = locations.apply(lambda x: Slice('location', x.start_dest, x.end_dest), axis='columns').tolist()

for location in locations:
    try:
        location.lookup(df_map)
    except FoundException as e:
        df = pd.DataFrame({'seed': [e.seed_id]})

        for step in [
            'seed-to-soil',
            'soil-to-fertilizer',
            'fertilizer-to-water',
            'water-to-light',
            'light-to-temperature',
            'temperature-to-humidity',
            'humidity-to-location',
        ]:
            source, _, dest = step.split('-')
            df[dest] = df[source].apply(lambda x: decode(x, df_map.loc[step]))
            logger.info(f'processed {step}')

        print(df.location[0])