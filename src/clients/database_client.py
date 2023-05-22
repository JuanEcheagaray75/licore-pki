import paho.mqtt.client as mqtt
import sqlite3
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA
from cryptography.hazmat.primitives.hashes import BLAKE2b
from cryptography.x509 import load_pem_x509_certificate


def write_to_db(db_path: str, packet: list) -> None:
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


def on_message(client, userdata, msg):
    

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



client = mqtt.Client("database_licore", clean_session=False)
client.tls_set(certfile='../.test_certs/database_licore.crt',
               keyfile='../.test_certs/database_licore.key',
               ca_certs='../.test_certs/ca-root-cert.crt')

client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.mona-temp-test.com", 8883, 60)
client.loop_forever(timeout=30, max_packets=3000)
