from template import *
from constant import *

class car:
	def __init__(self, speed, position, height, lane, direction, max_speed):
		self.speed = speed * direction
		self.position = position
		self.height = height / 2
		self.lane = lane
		self.direction = direction
		self.max_speed = max_speed

	def __eq__(self, other):
		return (self.position, self.lane) == (other.position, other.lane)

	def __str__(self):
		return str("(" + str(self.position) + ", " + str(self.speed) + ")") 

	def crash_test(self, other):
		return (self.lane == other.lane) and collide((self.position - self.height, self.position + self.height), (other.position - other.height, other.position + other.height))

	def time_to_collide(self, other):
		if self.crash_test(other):
			return 0 
		self.switch_lane()
		if self.crash_test(other):
			self.switch_lane()
			return 0 
		self.switch_lane()
		if self.position < other.position:
			if self.speed <= other.speed:
				return INF
			return (other.position - self.position - self.height - other.height) / (self.speed - other.speed)
		return -other.time_to_collide(self)

	def accelerate(self, acc):
		self.speed += acc * self.direction / FPS
		self.speed = fit(self.speed, self.max_speed * self.direction, 0)

	def update(self):
		self.position += self.speed / FPS

	def switch_lane(self):
		self.lane = 1 - self.lane
	def change_direction(self):
		self.direction *= -1

	def immediate(self, Cars):
		if self.direction == 1: 
			min_position = INF
			ans = None
			last = self.position - self.height
			for cars in Cars:
				if self == cars:
					continue
				last_car = cars.position + cars.height
				if self.lane == cars.lane and last_car > last and min_position > last_car:
					min_position = last_car
					ans = cars

		if self.direction == -1: 
			min_position = -INF
			ans = None
			last = self.position + self.height
			for cars in Cars:
				if self == cars:
					continue
				last_car = cars.position - cars.height
				if self.lane == cars.lane and last_car < last and min_position < last_car:
					min_position = last_car
					ans = cars

		return ans

def crash_test():
	for cars in Cars[1:]:
		if Cars[0].crash_test(cars) is True:
			return "Crash"
	for i in range(1, len(Cars)):
		for j in range(i + 1, len(Cars)):
			if Cars[i].crash_test(Cars[j]) is True:
				return "System Crash"
	return "False"

def build_cars():

	data = INPUT()

	for row in data: 
		curCar = car(*row)
		Cars.append(curCar)


def add_endpoints():
	Cars.append(car(0, -INF/2, LEN_CAR, 0, 1, MAX_SPEED))
	Cars.append(car(0, -INF/2, LEN_CAR, 1, -1, MAX_SPEED))
	Cars.append(car(0, INF/2, LEN_CAR, 0, 1, MAX_SPEED))
	Cars.append(car(0, INF/2, LEN_CAR, 1, -1, MAX_SPEED))

