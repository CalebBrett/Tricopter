import os
import time
import math
import smbus
import pigpio
import threading

#Start GPIO on the pi
os.system ("sudo pigpiod")
time.sleep(1)

#Variables
m1 = 9
m2 = 10
m3 = 11
min_speed = 700
max_speed = 2000
is_running = True
speed_sp = min_speed
m1_speed = min_speed
m2_speed = min_speed
m3_speed = min_speed
pi = pigpio.pi();

#Registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
bus = smbus.SMBus(1)
address = 0x68

#Get i2c data for accelerometer
def read_word_2c(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    if (value >= 0x8000):
        return -((65535 - value) + 1)
    else:
        return value

#Balancing function that runs in the background, reads accelerometer and reduces the coresponding motor power to keep the drone level
def auto_balance():
	print "Balancing sequence starting"

	while is_running:
		bus.write_byte_data(address, power_mgmt_1, 0)

		#Set motor power to the set point that was inputed by the user in the main thread
		m1_speed = speed_sp
		m2_speed = speed_sp
		m3_speed = speed_sp

		try:
			#Get accelerations and rotations
			acceleration_x = read_word_2c(0x3b) / 16384.0
			acceleration_y = read_word_2c(0x3d) / 16384.0
			acceleration_z = read_word_2c(0x3f) / 16384.0
			rotation_x = math.degrees(math.atan2(acceleration_y, math.sqrt((acceleration_x*acceleration_x)+(acceleration_z*acceleration_z))))
			rotation_y = -math.degrees(math.atan2(acceleration_x, math.sqrt((acceleration_y*acceleration_y)+(acceleration_z*acceleration_z))))

			#Adjust motor power acordingly
			if(rotation_x > 2 and rotation_y > 2):
				m1_speed = m1_speed - abs(rotation_y)
			if(rotation_x < 2 and rotation_x > -2 and rotation_y < -2):
				m2_speed = m2_speed - abs(rotation_y)
			if(rotation_x < -2 and rotation_y > 2):
				m3_speed = m3_speed - abs(rotation_y)
		except:
			print "Fault"

		#Set motor power
		pi.set_servo_pulsewidth(m1, m1_speed)
		pi.set_servo_pulsewidth(m2, m2_speed)
		pi.set_servo_pulsewidth(m3, m3_speed)

#Calibrate ESC's
if(raw_input("Calibrate? (Y/N) ") == "Y"):
	print "Starting calibration"
	pi.set_servo_pulsewidth(m1, 0)
	pi.set_servo_pulsewidth(m2, 0)
	pi.set_servo_pulsewidth(m3, 0)
	time.sleep(1)
	pi.set_servo_pulsewidth(m1, max_speed)
	pi.set_servo_pulsewidth(m2, max_speed)
	pi.set_servo_pulsewidth(m3, max_speed)
	time.sleep(1)
	pi.set_servo_pulsewidth(m1, min_speed)
	pi.set_servo_pulsewidth(m2, min_speed)
	pi.set_servo_pulsewidth(m3, min_speed)
	time.sleep(1)
	pi.set_servo_pulsewidth(m1, 0)
	pi.set_servo_pulsewidth(m2, 0)
	pi.set_servo_pulsewidth(m3, 0)
	time.sleep(1)
	pi.set_servo_pulsewidth(m1, min_speed)
	pi.set_servo_pulsewidth(m2, min_speed)
	pi.set_servo_pulsewidth(m3, min_speed)
	print "Calibration completed"

#Flight program
print "Flight starting"
balance = threading.Thread(target=auto_balance)
balance.start()
time.sleep(1)
while is_running:
	command = raw_input("Enter a command: ")
	if(command == "speed"):
		speed_sp = int(raw_input("Enter a speed: "))
	elif(command == "stop"):
		is_running = False
	else:
		print "Command invalid. Try speed or stop."

#Clean up
pi.set_servo_pulsewidth(m1, 0)
pi.set_servo_pulsewidth(m2, 0)
pi.set_servo_pulsewidth(m3, 0)
balance.join()
os.system ("sudo killall pigpiod")
print "Goodbye!"
