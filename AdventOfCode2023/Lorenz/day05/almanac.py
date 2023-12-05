import pandas as pd


def decode(x, mapping):
    map = mapping[(mapping.start_source<=x) & (mapping.end_source>=x)]
    if map.empty:
        return x
    else:
        # we assume there is only one correct map in the filter
        return x + map.iloc[0].delta

# opening and reading the lines from the input
with open('./input.txt', 'r') as f:
    lines = f.readlines()

seeds = [int(x) for x in lines[0].split(':')[-1].split(' ') if x != '']
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
df_map['end_source'] = df_map.start_source + df_map.range - 1
df_map['delta'] = df_map.start_dest - df_map.start_source

df = pd.DataFrame({'seed': seeds})


for map in [
    'seed-to-soil',
    'soil-to-fertilizer',
    'fertilizer-to-water',
    'water-to-light',
    'light-to-temperature',
    'temperature-to-humidity',
    'humidity-to-location',
]:
    source, _, dest = map.split('-')
    df[dest] = df[source].apply(lambda x: decode(x, df_map[df_map.mapping == map]))

print(df.location.min())