import adafruit_dht
import time
import board
from datetime import datetime
import csv
import requests

# --------- User Settings ---------
SENSOR_LOCATION_NAME = "C36"
MINUTES_BETWEEN_READS = 10
METRIC_UNITS = True
# ---------------------------------

def sendmessage(msg):
	

def writeToCSV(humidity, temp):
	now = datetime.now()
	dt = now.strftime("%d/%m/%Y %H:%M:%S")
	row = [dt, humidity, temp]
	with open('temphistory', 	'a') as f:
		writer = csv.writer(f)
		writer.writerow(row)
	
def checkLast(num):
	with open('temphistory', 'r') as f:
		reader = csv.reader(f)
		lastFive = list(reader)[-num:]

	for i in range(len(lastFive)):
		if(lastFive[i][1] > 50):
			sendmessage("WARNING: HIGH HUMIDITY")
		if(lastFive[i][2] > 25):
			sendmessage("WARNING: HIGH TEMP")
		if(lastFive[i][2] < 0):
			sendmessage("WARNING: LOW TEMP")
		print("\n")

		
	return lastFive


def main():
	dhtSensor = adafruit_dht.DHT22(board.D4)

	while True:
			try:
					humidity = dhtSensor.humidity
					temp_c = dhtSensor.temperature
			except RuntimeError:
					print("RuntimeError, trying again...")
					continue
			print(SENSOR_LOCATION_NAME + " Temperature(C)", temp_c)
			humidity = format(humidity,".2f")
			print(SENSOR_LOCATION_NAME + " Humidity(%)", humidity)
			writeToCSV(humidity, temp_c)
			checkLast(3)
			time.sleep(60*MINUTES_BETWEEN_READS)

if __name__ == "__main__":
	main()


