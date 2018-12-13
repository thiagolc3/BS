import paho.mqtt.publish as publish
import serial

ser = serial.Serial("/dev/ttyACM1", 115200)

while True:

	str = ser.readline()

	publish.single('influx', str, 1)
	#print str

ser.close()


