import pandas as pd
from pathlib import Path
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey, EllipticCurvePrivateKey
from cryptography.x509 import Certificate
from typing import Tuple


AuditorCredentials = Tuple[Certificate, EllipticCurvePublicKey, EllipticCurvePrivateKey]


def create_packets(csv_file_path: str) -> list:
    """Helper function to create packets from csv file

    Args:
        csv_file_path (str): path to db provided by LiCore

    Raises:
        Exception: If file does not exist

    Returns:
        list: List of MQTT formatted packets
    """

    # Check if file exists
    if not Path(csv_file_path).is_file():
        raise Exception('File does not exist')

    df = pd.read_csv(csv_file_path)
    df['packet'] = df['id'] \
        + '/' + df['datetime'] \
        + '/' + df['type'].astype(str) \
        + '/' + df['value'].astype(str)
    df.sort_values(by=['datetime'], inplace=True)

    return df['packet'].tolist()


def load_cert_pub_priv(device_name: str) -> AuditorCredentials:
    """Helper function to load certificate, pub and priv key

    Args:
        device_name (str): Device Name as per registered in LiCore

    Returns:
        AuditorCredentials: Tuple of Certificate, Pub and Priv key
    """

    client_cert: Certificate = None
    client_pub_key: EllipticCurvePublicKey = None
    client_priv_key: EllipticCurvePrivateKey = None

    # Load Certificates
    with open(f'../.test_certs/{device_name}.key', 'rb') as f:
        client_priv_key = load_pem_private_key(f.read(), password=None)

    with open(f'../.test_certs/{device_name}.crt', 'rb') as f:
        client_cert = load_pem_x509_certificate(f.read())
        client_pub_key = client_cert.public_key()

    return client_cert, client_pub_key, client_priv_key