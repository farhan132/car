# Time: second
# Position: meters

from template import *
from constant import *
from car import *
import random

############## SPEED and POSITIONS ############## 

# Units: meter and second
# Acceleration: m/s^2

myCar_SPEED = 15.2
car1_SPEED = 15
car2_SPEED = 14.5

myCar_POSITION = 0
car1_POSITION = 50
car2_POSITION = 420

car1_ACC = 0.04 
car1_DEACC = 0.01

car2_ACC = 0.05
car2_DEACC = 0.01

############## DECISION TEMPLATE ##############

def decision(myCar, time_to_car1, time_to_car2):

	# if time_to_car2 < 0:
	# 	# print(time_to_car2)
	# 	return "Had To Wait"

	# Crossover Constant
	# This Variable Will Be Adjusted Via Machine Learning
	Crossover_Constant = 3 * LEN_CAR / myCar.speed 

	# Risk Constant (Minimum Time Space Needs To Attempt A Crossover)
	Risk_Constant = Crossover_Constant * 1.5

	# Safe Distance Constant
	Safe_Constant = 15

	# Already Switched Lanes
	if myCar.lane == 0:

		# Already Crossed The Car
		if time_to_car1 < 0: 
			myCar.switch_lane()
			return "Successful Crossing"

		# Parrallel To The Car1
		if time_to_car1 == 0:

			# Not Enough Time To Cross
			if time_to_car2 < Risk_Constant:
				myCar.accelerate(-ACC_CAR)
				return "Deaccelerate"

			# Enough Time To Cross
			myCar.accelerate(ACC_CAR)
			return "Accelerate"

		# Not Enough Time To Cross
		if time_to_car2 < Risk_Constant:
			myCar.switch_lane()
			return "Unsuccessful Crossing"

		# Enough Time To Cross
		myCar.accelerate(ACC_CAR)
		return "Accelerate"

	# Have Not Switched Lanes

	# Car1 Is Moving Faster Than MyCar
	if time_to_car1 == INF:
		myCar.accelerate(ACC_CAR)
		return "Accelerate"

	# MyCar Is Too Close To Car1
	if time_to_car1 < Safe_Constant:

		# Safe To Pass
		if time_to_car2 > Risk_Constant:
			myCar.switch_lane()
			return "Attempt Started"

		# Not Safe to Pass
		myCar.accelerate(-ACC_CAR)
		return "Deaccelerate"

	# Car1 Is Far Away. Could Speed Up
	myCar.accelerate(ACC_CAR)
	return "Accelerate"

def random_car_acceration(car, acc, stay, dec):
	assert (acc + stay + dec) == 1
	
	key = random.uniform(0.0, 1.0)

	# Accelerate 
	if key <= acc:
		car.accelerate(ACC_CAR)
		return ACC_CAR

	# No Accelerate
	if key <= acc + stay:
		return 0

	# Deacceleration
	car.accelerate(-ACC_CAR)
	return -ACC_CAR




############ MAIN ##############
def run():
	myCar = car(myCar_SPEED, myCar_POSITION, LEN_CAR, 1, 1, MAX_SPEED)
	car1 = car(car1_SPEED, car1_POSITION, LEN_CAR, 1, 1, MAX_SPEED)
	car2 = car(car2_SPEED, car2_POSITION, LEN_CAR, 0, -1, MAX_SPEED)

	Cars.extend([myCar, car1, car2])

	attempt_success = "Success"

	FRAME = 0

	while FRAME < MAX_FRAME:
		FRAME += 1
		if crash_test().split()[-1] == "Crash":
			attempt_success = crash_test()
			break
		time_to_car1 = myCar.time_to_collide(car1)
		time_to_car2 = myCar.time_to_collide(car2)

		Log.append(decision(myCar, time_to_car1, time_to_car2))

		random_car_acceration(car1, car1_ACC, 1 - car1_ACC - car1_DEACC, car1_DEACC)
		random_car_acceration(car2, car2_ACC, 1 - car2_ACC - car2_DEACC, car2_DEACC)

		for cars in Cars:
			cars.update()

		if Log[-1] in ["Successful Crossing", "Unsuccessful Crossing", "Had To Wait"]:
			break

	print(attempt_success)

	process_log(Log)

run()



