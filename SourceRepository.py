import pandas as pd


def fetch_data(file_name: str):
      return pd.read_csv(file_name, sep='|', header=0)

