import pandas as pd
from pathlib import Path
from cryptography import x509
from cryptography.x509 import load_pem_x509_certificate, Certificate
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey, EllipticCurvePrivateKey, generate_private_key, SECP256R1
from datetime import datetime, timedelta
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


def sign_certificate_request(csr_cert: Certificate,
                             ca_cert: Certificate,
                             private_ca_key: EllipticCurvePrivateKey) -> bytes:
    """Helper function to sign certificate request

    Args:
        csr_cert (Certificate): CSR from auditor
        ca_cert (Certificate): CA certificate
        private_ca_key (EllipticCurvePrivateKey): CA private key

    Returns:
        bytes: Public bytes of signed certificate in PEM format
    """
    cert = x509.CertificateBuilder().subject_name(
        csr_cert.subject
    ).issuer_name(
        ca_cert.subject
    ).public_key(
        csr_cert.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        # Our certificate will be valid for 10 days
        datetime.utcnow() + timedelta(days=365)
    # Sign our certificate with our private key
    ).sign(private_ca_key, hashes.SHA256())

    # return DER certificate
    return cert.public_bytes(serialization.Encoding.PEM)


def register_auditor(dev_name: str,
                     state: str,
                     locality: str,
                     postal_code: str) -> None:
    """Helper function to register auditor

    Args:
        dev_name (str): Device Name as per registered in LiCore
        state (str): Geographical State of the auditor
        locality (str): Geographical Locality of the auditor
        postal_code (str): Postal Code of the auditor
    """

    key = generate_private_key(curve=SECP256R1())
    private_key = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open(f'../.test_certs/{dev_name}.key', 'wb') as f:
        f.write(private_key)

    csr = x509.CertificateSigningRequestBuilder().subject_name(
        x509.Name(
            [x509.NameAttribute(NameOID.COUNTRY_NAME, "MX"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
            x509.NameAttribute(NameOID.POSTAL_CODE, postal_code),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Tec de Monterrey"),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "IDM"),
            x509.NameAttribute(NameOID.COMMON_NAME, dev_name)
            ]
        )
    ).sign(key, hashes.SHA256())

    with open(f"../.test_certs/{dev_name}-request.csr", "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))

    # load_pem_x509_csr(csr.public_bytes(serialization.Encoding.PEM)).subject
    with open(f'../.test_certs/ca-root-cert.crt', 'rb') as f:
        ca_cert = load_pem_x509_certificate(f.read())

    with open(f'../.test_certs/ca.key', 'rb') as f:
        ca_key = load_pem_private_key(f.read(), password=None)

    client_cert = sign_certificate_request(ca_cert=ca_cert,
                                        private_ca_key=ca_key,
                                        csr_cert=csr)

    with open(f'../.test_certs/{dev_name}.crt', 'wb') as f:
        f.write(client_cert)

def batch_register(registry_list: str) -> None:
    """Helper function to batch register auditors

    Args:
        registry_list (str): Path to csv file with registry list
    """    

    df = pd.read_csv(registry_list)

    for aud in df.to_dict(orient='records'):
        dev_name = aud['device']
        state = aud['state']
        locality = aud['locality']
        postal_code = str(aud['postal_code'])
        register_auditor(dev_name=dev_name,
                    state=state,
                    locality=locality,
                    postal_code=postal_code)