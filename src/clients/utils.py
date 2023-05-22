import pandas as pd


def create_packets(csv_file: str) -> list:
    df = pd.read_csv(csv_file)
    df['packet'] = df['id'] \
        + '/' + df['datetime'] \
        + '/' + df['type'].astype(str) \
        + '/' + df['value'].astype(str)
    df.sort_values(by=['datetime'], inplace=True)

    return df['packet'].tolist()
