import paho.mqtt.client as mqtt
from paho.mqtt.publish import single
import sqlite3
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA
from cryptography.hazmat.primitives.hashes import BLAKE2b
from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.oid import NameOID
from utils import load_cert_pub_priv


def write_to_db(db_path: str, packet: list) -> None:
    """Write auditor packet to sqlite db

    Args:
        db_path (str): Relative path to sqlite3 database
        packet (list): List representation of packet
    """
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()

        sqlite_insert_query = """INSERT INTO measures (
            aud_id,
            measured_timestamp,
            measure_type,
            measure
        )
        VALUES (?, ?, ?, ?);"""

        cursor.execute(sqlite_insert_query, packet)
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def on_connect(client, userdata, flags, rc):
    print("Connected through MQTT " + str(rc))
    client.subscribe("audits/measures/#", qos=0)



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


    if Path(f'../.test_certs/{user_id}.crt').is_file():

        with open(f'../.test_certs/{user_id}.crt', 'rb') as f:
            user_cert = load_pem_x509_certificate(f.read())
            pub_key = user_cert.public_key()

        try:
            pub_key.verify(signature,
                           packet.encode('utf-8'),
                           ECDSA(BLAKE2b(64)))
            vals = packet.split('/')

            write_to_db('../../db/measures.sqlite3', vals)
            print(f'Packet {packet} written to database')

        except:
            raise Exception('Invalid signature')

# GENERAL PARAMETERS
broker = "mqtt.mona-temp-test.com"
port = 8883
dev_name = 'database_licore'
database_cert, database_pub, database_key = load_cert_pub_priv(dev_name)
id = database_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value


def main():
    client = mqtt.Client(id, clean_session=True)
    client.tls_set(certfile='../.test_certs/database_licore.crt',
                keyfile='../.test_certs/database_licore.key',
                ca_certs='../.test_certs/ca-root-cert.crt')

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)
    # Test message of parameter update for bidirectional communication proof of concept
    tls_sets = {'ca_certs':"../.test_certs/ca-root-cert.crt",
                'certfile':"../.test_certs/database_licore.crt",
                'keyfile':"../.test_certs/database_licore.key"}

    test_message = '0.2'
    signature = database_key.sign(
            test_message.encode('utf-8'),
            ECDSA(BLAKE2b(64))
        )
    packet = test_message + "||" + signature.hex()

    single(topic='control_center/updates/auditor_mona/database_licore/SAMPLE_RATE',
        payload=packet, qos=2,
        hostname=broker, port = port,
        tls=tls_sets, retain=True)

    client.loop_forever(timeout=30, max_packets=3000)

if __name__ == '__main__':
    main()