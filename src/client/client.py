import paho.mqtt.client as mqtt


broker = "mqtt.mona-temp-test.com"
port = 1883


client = mqtt.Client()
client.connect(broker, port, 60)
client.username_pw_set("mona", "mona")

client.publish("ALSW/temp", "20")

client.disconnect()
