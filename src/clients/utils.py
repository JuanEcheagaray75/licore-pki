import pandas as pd
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def create_packets(csv_file: str) -> list:
    df = pd.read_csv(csv_file)
    df['packet'] = df['id'] \
        + '/' + df['datetime'] \
        + '/' + df['type'].astype(str) \
        + '/' + df['value'].astype(str)
    df.sort_values(by=['datetime'], inplace=True)

    return df['packet'].tolist()

def load_cert_pub_priv(device_name: str):


    # Load Certificates
    with open(f'../.test_certs/{device_name}.key', 'rb') as f:
        client_priv_key = load_pem_private_key(f.read(), password=None)

    with open(f'../.test_certs/{device_name}.crt', 'rb') as f:
        client_cert = load_pem_x509_certificate(f.read())
        client_pub_key = client_cert.public_key()

    return client_cert, client_pub_key, client_priv_key