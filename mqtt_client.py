# -*- coding:utf-8 -*-
import paho.mqtt.client as mqtt

# mqtt server
mqtt_broker_ip = "192.168.1.11"
mqtt_broker_port = 1883
mqtt_username = ""
mqtt_password = ""
mqtt_client_id = "fooonoff_py"
mqtt_namespace = "fooonoff"
mqtt_topic = mqtt_namespace + "/ht"
mqtt_client_temp_ch = "/temp"
mqtt_qos = 0
mqtt_keepalive = 120 # 2 minutos

suscribe_cache = []

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # cacnal general
    client.subscribe(mqtt_topic)
    # canal de temperatura

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if msg.payload.startswith('HELO '):
        # es un mensage de inicio o conexión
        device_id = msg.payload.strip('HELO ')
        print('HELO >> %s' % device_id)

        if device_id not in suscribe_cache or 1:
            #intenta conectar al ch temp
            client.subscribe("%s/%s/%s" % (mqtt_namespace, device_id , mqtt_client_temp_ch))
            suscribe_cache.append(device_id)
            print("nuevo canal temp para %s" % device_id)


#client = mqtt.Client()
client = mqtt.Client(mqtt_client_id, mqtt_keepalive, mqtt_username, mqtt_password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_ip, mqtt_broker_port, mqtt_keepalive)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
