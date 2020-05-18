from glob import glob
import pandas as pd

def remove_white_space(x):
    return (x.replace(' .', '.')
            .replace(' .', '.')
            .replace(' ,', ',')
            .replace(' ?', '?')
            .replace(' !', '!')
            )

def jsonl_list_to_dataframe(file_list, columns=[
        'response', 'context', 'context/0', 'context/1',
        'context/2', 'context/3', 'context/4', 'context/5',
        'context/6', 'context/7', 'context/8', 'context/9'
    ]):
    """Load a list of jsonl.gz files into a pandas DataFrame."""
    return pd.concat([pd.read_json(f,
                                   orient='records', encoding='utf-8',
                                   lines=True)[columns]
                      for f in file_list], sort=False)

df = jsonl_list_to_dataframe(glob("output/train*.json"), ).dropna()
df = df.drop_duplicates()
df = df.applymap(remove_white_space)
df.head()
df.to_csv('./conversation_indo_formatted.csv', index=False, encoding = 'utf-8')
