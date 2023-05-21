import paho.mqtt.client as mqtt


broker = "mqtt.mona-temp-test.com"
port = 8883


client = mqtt.Client()
client.tls_set(ca_certs="ca-root-cert.crt")
client.connect(broker, port, 60)
client.username_pw_set("mona", "mona")

client.publish("ALSW/temp", "20")

client.disconnect()
