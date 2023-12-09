import pandas as pd

df = pd.read_csv('./input.txt', sep=' ', header=None)


def predict_next(row):
    diff = row.diff()

    values = [row.iloc[-1]]
    while not (diff.fillna(0.0) == 0).all():
        # keep the last value
        values.append(diff.iloc[-1])
        # take the diff
        diff = diff.diff()

    return int(sum(values))

predictions = df.apply(predict_next, axis='columns')
print(predictions.sum())