import pandas as pd

def convert_price_history_dict_to_dataframe(price_history_dict: dict) -> pd.DataFrame:
    df = pd.DataFrame.from_dict(price_history_dict).transpose()
    return df
