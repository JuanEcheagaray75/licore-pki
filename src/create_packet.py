import pandas as pd
import time


def create_packets(csv_file: str) -> list:
    df = pd.read_csv(csv_file)
    df['packet'] = df['id'] \
        + '/' + df['datetime'] \
        + '/' + df['type'].astype(str) \
        + '/' + df['value'].astype(str)
    df.sort_values(by=['datetime'], inplace=True)

    return df['packet'].tolist()


def test_send_packets(packets: list) -> None:
    for packet in packets:
        print(packet)
        time.sleep(1)


def main():

    packets = create_packets('db/processed/Prosumer_ABC.csv')
    test_send_packets(packets)


if __name__ == '__main__':
    main()