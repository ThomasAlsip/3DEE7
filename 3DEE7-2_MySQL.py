import time
import datetime
import pyfirmata
import mysql.connector

# debug text
cc = "No connection:\t"
c = "Connected to:\t"

# debug messages
def errorMessage():
	print("[ Error ]\t", cc, d)

def okMessage():
	print("[ OK ]\t\t", c, d)

# connect to database
try:
	db = mysql.connector.connect(
		host = "localhost",
		user = "root",
		password = "elev",
		database = "3dee7"
	)
	d = "Database"
	okMessage()
except:
	d = "Database"
	errorMessage()

# connect to arduino
try:
	board = pyfirmata.Arduino("COM4")
	it = pyfirmata.util.Iterator(board)
	it.start()
	d = "Arduino"
	okMessage()
except:
	d = "Arduino"
	errorMessage()

# setup, database and values
run_count = 0
my_cursor = db.cursor()
sql = "INSERT INTO pot_sensor(v, t) VALUES (%s,%s)"

# pins
a1 = board.get_pin("a:1:i")

# main
while True:
	# save value from A1 to variable
	a = a1.read()
	t = datetime.datetime.now()
	val = (a, t)

	# print readings and send to database
	run_count += 1
	print("| Packet: ", run_count, "\t\t| Voltage: ", a, "\t| Time: ", t)
	my_cursor.execute(sql, val)
	db.commit()

	time.sleep(1)