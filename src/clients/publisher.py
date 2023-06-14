import paho.mqtt.client as mqtt
from time import sleep
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA
from cryptography.hazmat.primitives.hashes import BLAKE2b
from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.oid import NameOID
from utils import create_packets, load_cert_pub_priv

# GENERAL PARAMETERS
broker = "mqtt.mona-temp-test.com"
port = 8883
dev_name = 'auditor_mona'
auditor_cert, auditor_pub, auditor_key = load_cert_pub_priv(dev_name)
id = auditor_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
SAMPLE_RATE = 1

# TODO: Change this name accordingly, for dev purposes we use
# the python database client script to test the general sending
# of parameter updates.
CONTROL_CENTER_NAME = 'database_licore'

def on_connect(client: mqtt, userdata: dict, flags: dict, rc: int) -> None:
    """On connect utility of MQTT publisher client

    Args:
        client (mqtt): MQTT Client
        userdata (dict): Private User data
        flags (dict): Extra flags for communication
        rc (int): Return code, 0 if successful, else error code
    """
    print("Connected through MQTT " + str(rc))
    client.subscribe(f"control_center/updates/{dev_name}/#", qos=2)


def on_message(client: mqtt, userdata: dict, msg: mqtt.MQTTMessage) -> None:
    """On message utility to validate parameter updates

    Args:
        client (mqtt): MQTT Client
        userdata (dict): Private User data
        msg (mqtt.MQTTMessage): MQTT Message to process

    Raises:
        Exception: If signature is invalid
    """

    received_message = msg.payload.decode('utf-8')
    user_id = msg.topic.split('/')[3]
    parameter_update = msg.topic.split('/')[-1]
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

            if parameter_update == 'SAMPLE_RATE':
                global SAMPLE_RATE
                SAMPLE_RATE = float(packet)
                print(f'New sample rate: {SAMPLE_RATE}')
        except:
            raise Exception('Invalid signature')



def main():
    # Client setup
    client = mqtt.Client("auditor_mona", clean_session=True)
    client.tls_set(certfile='../.test_certs/auditor_mona.crt',
                keyfile='../.test_certs/auditor_mona.key',
                ca_certs='../.test_certs/ca-root-cert.crt')

    client.on_connect = on_connect
    client.on_message = on_message

    client.tls_insecure_set(False)
    client.connect(broker, port, 2*60)

    packets = create_packets('../../db/processed/Prosumer_ABC.csv')

    try:
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
                        qos=0)

            print(f'Packet {packet} published')
            sleep(SAMPLE_RATE)

        print('Done!')
        client.loop_stop()
        client.disconnect()

    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == '__main__':
    main()