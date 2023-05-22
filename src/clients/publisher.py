import paho.mqtt.client as mqtt
from time import sleep
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA
from cryptography.hazmat.primitives.hashes import BLAKE2b
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.oid import NameOID
from utils import create_packets


with open('../.test_certs/auditor_mona.key', 'rb') as f:
    auditor_key = load_pem_private_key(f.read(), password=None)

with open('../.test_certs/auditor_mona.crt', 'rb') as f:
    auditor_cert = load_pem_x509_certificate(f.read())
    pub_key = auditor_cert.public_key()

# GENERAL PARAMETERS
broker = "mqtt.mona-temp-test.com"
port = 8883
id = auditor_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

# Client setup
client = mqtt.Client("auditor_mona", clean_session=False)
client.tls_set(certfile='../.test_certs/auditor_mona.crt',
               keyfile='../.test_certs/auditor_mona.key',
               ca_certs='../.test_certs/ca-root-cert.crt')

client.tls_insecure_set(False)
client.connect(broker, port, 2*60)

packets = create_packets('../../db/processed/Prosumer_ABC.csv')

print('Publishing packets...')
for packet in packets:

    signature = auditor_key.sign(
        packet.encode('utf-8'),
        ECDSA(BLAKE2b(64))
    )
    payload = packet + '||' + signature.hex()
    client.publish(topic=f'audits/measures/{id}',
                   payload=payload,
                   qos=0)

    print(f'Packet {packet} published')
    sleep(0.2)

print('Done!')
client.disconnect()
