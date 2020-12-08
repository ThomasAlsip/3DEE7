import time
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata

run_count = 0
ADAFRUIT_IO_USERNAME = "timjim"
ADAFRUIT_IO_KEY = "aio_FwfD23kyaeXCieHcpUNCLaptWErm"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

board = pyfirmata.Arduino("COM4")

it = pyfirmata.util.Iterator(board)
it.start()

# pins
pin13 = board.get_pin("d:13:o")
ana01 = board.get_pin("a:1:i")

# use feeds, create if non-existent
try:
	analog = aio.feeds("analog")
	digital = aio.feeds("digital")

except RequestError:
	feedA = Feed(name="analog")
	analog = aio.create_feed(feedA)
	feedD = Feed(name="digital")
	digital = aio.create_feed(feedD)

# main
while True:
	# get digital key and save value from A1 to variable
	data = aio.receive(digital.key)
	ana_tele = ana01.read()

	# LED switch
	# if data.value == "ON":
	# 	pin13.write(True)
	# else:
	# 	pin13.write(False)
	
	# send data to feeds
	aio.send_data("analog", ana_tele)

	# footer
	run_count += 1
	print("Packet: ", run_count, "\tVoltage: ", ana_tele)

	time.sleep(1.1)