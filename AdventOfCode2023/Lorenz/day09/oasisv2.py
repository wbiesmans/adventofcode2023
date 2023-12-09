import pandas as pd

df = pd.read_csv('./input.txt', sep=' ', header=None)


def predict_previous(row):
    diff = row[::-1].diff()

    values = [row.iloc[0]]
    while not (diff.fillna(0.0) == 0).all():
        # keep the last value
        values.append(diff.iloc[-1])
        # take the diff
        diff = diff.diff()

    return int(sum(values))

predictions = df.apply(predict_previous, axis='columns')
print(predictions.sum())