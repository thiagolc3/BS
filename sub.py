import paho.mqtt.client as mqtt
import json

from influxdb import client as influxdb
db=influxdb.InfluxDBClient('localhost', 8086, 'admin', 'admin', 'wl')

def BStoDB(id, wl, pwr):

	return [
        {
            "measurement": "sensorsLogger",
            "tags": {
                "id": id
             },
             "fields": {
                "wl": wl,
                "pwr": pwr
            }
        }
    ]


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('influx')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    try:
        strJson = json.loads(msg.payload)

        for x in range(0, strJson['qty']):
            id = strJson['peaks'][x]['id']
            wl = strJson['peaks'][x]['wl']
            pw = strJson['peaks'][x]['pwr']

            print id, wl, pw
            db.write_points(BStoDB(id, wl, pw))

    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print 'Decoding JSON has failed'


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('localhost', 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

