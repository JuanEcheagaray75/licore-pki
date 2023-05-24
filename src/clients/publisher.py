import paho.mqtt.client as mqtt
from time import sleep
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA
from cryptography.hazmat.primitives.hashes import BLAKE2b
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.oid import NameOID
from utils import create_packets


# TODO: Change this name accordingly, for dev purposes we use
# the python database client script to test the general sending
# of parameter updates.
CONTROL_CENTER_NAME = 'database_licore'

# Load Certificates
with open('../.test_certs/auditor_mona.key', 'rb') as f:
    auditor_key = load_pem_private_key(f.read(), password=None)

with open('../.test_certs/auditor_mona.crt', 'rb') as f:
    auditor_cert = load_pem_x509_certificate(f.read())
    pub_key = auditor_cert.public_key()


def on_connect(client, userdata, flags, rc):
    print("Connected through MQTT " + str(rc))
    client.subscribe("control_center/updates/#", qos=0)


def on_message(client: mqtt, userdata, msg):
    """On message utility of MQTT publisher client

    Args:
        client (mqtt): MQTT client
        userdata (_type_): Userdata representation of client
        msg (_type_): Message to publish

    Raises:
        Exception: Invalid
    """

    received_message = msg.payload.decode('utf-8')
    user_id = msg.topic.split('/')[2]
    packet = received_message.split('||')[0]
    signature = bytes.fromhex(received_message.split('||')[-1])


    if Path(f'../.test_certs/{user_id}.crt').is_file() and user_id == CONTROL_CENTER_NAME:

        with open(f'../.test_certs/{user_id}.crt', 'rb') as f:
            user_cert = load_pem_x509_certificate(f.read())
            pub_key = user_cert.public_key()

        try:
            pub_key.verify(signature,
                           packet.encode('utf-8'),
                           ECDSA(BLAKE2b(64)))

            print(f'Received parameter update as: {packet}')
        except:
            raise Exception('Invalid signature')


# GENERAL PARAMETERS
broker = "mqtt.mona-temp-test.com"
port = 8883
id = auditor_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value


# Client setup
client = mqtt.Client("auditor_mona", clean_session=False)
client.tls_set(certfile='../.test_certs/auditor_mona.crt',
               keyfile='../.test_certs/auditor_mona.key',
               ca_certs='../.test_certs/ca-root-cert.crt')

client.on_connect = on_connect
client.on_message = on_message

client.tls_insecure_set(False)
client.connect(broker, port, 2*60)

packets = create_packets('../../db/processed/Prosumer_ABC.csv')

client.loop_start()
print('Publishing packets...')
for packet in packets:

    # IMPORTANT: Hash length of Blake2b
    # Signature algorithm is in pair with FIPS 186-4
    # https://csrc.nist.gov/publications/detail/fips/186/4/final
    # The source code is written in Rust, it does chop the hash, if
    # the len of the digest is greater than 256 bits
    # The standard imposes this behavior
    signature = auditor_key.sign(
        packet.encode('utf-8'),
        ECDSA(BLAKE2b(64))
    )
    payload = packet + '||' + signature.hex()
    client.publish(topic=f'audits/measures/{id}',
                   payload=payload,
                   qos=2)

    print(f'Packet {packet} published')
    sleep(0.2)

print('Done!')
client.loop_stop()
client.disconnect()
