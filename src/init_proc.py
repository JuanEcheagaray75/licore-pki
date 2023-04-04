import pandas as pd
from pathlib import Path


def initial_processing(data_path: str) -> pd.DataFrame:
    """Initial processing of raw csv file provided by LiCore.

    Args:
        data_path (str): Path to raw csv file.

    Raises:
        FileNotFoundError: If the file is not found.

    Returns:
        pd.DataFrame: Pandas DataFrame with the processed data, to be saved later.
    """

    # Check if the file exists, if not raise an error
    if not Path(data_path).is_file():
        raise FileNotFoundError(f'File {data_path} not found')

    df = pd.read_csv(data_path, sep=";")
    df = pd.melt(df, id_vars=['ID', 'Consumo (0) / Producción (1)', 'Dia', 'Mes ', 'Año'])

    # As a result for the melt function, the variable column is a string
    # which encodes time changes in 15 minute intervals
    df['variable'] = pd.to_numeric(df['variable'])
    df['variable'] *= 15

    # String parsing to get the hour and minute
    df['time'] = pd.to_datetime(df['variable'], unit='m').dt.strftime('%H:%M')
    df['hour'] = df['time'].str.split(':').str[0]
    df['minute'] = df['time'].str.split(':').str[1]

    # Create a new column with the datetime
    df['datetime'] = pd.to_datetime(df['Año'].astype(str)
                                    + '-' + df['Mes '].astype(str)
                                    + '-' + df['Dia'].astype(str)
                                    + ' ' + df['time'])
    df.drop(
        ['variable', 'time', 'hour', 'minute', 'Dia', 'Mes ', 'Año'],
        axis=1, inplace=True
    )

    df.rename(columns={'Consumo (0) / Producción (1)': 'type', 'ID': 'id', 'value': 'value'}, inplace=True)
    df.sort_values(by='datetime', inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def main():

    print('Processing raw data...')
    df = initial_processing('db/raw/Prosumer_ABC.csv')

    # Save to csv
    df.to_csv('db/processed/Prosumer_ABC.csv', index=False)
    print('Done!')


if __name__ == '__main__':
    main()