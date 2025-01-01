from template import *
from constant import *

class car:
	def __init__(self, speed, position, height, lane):
		self.speed = speed
		self.position = position
		self.height = height
		self.lane = lane

	def crash_test(self, other):
		return (self.lane == other.lane) and collide((self.position, self.position + self.height), (other.position, other.position + other.height))

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
			return (other.position - self.position - self.height) / (self.speed - other.speed)
		meet = other.time_to_collide(self)
		return -meet

	def accelerate(self, acc):
		self.speed += acc / FPS
		self.speed = min(MAX_SPEED, max(self.speed, 0))

	def update(self):
		self.position += self.speed / FPS

	def switch_lane(self):
		self.lane = 1 - self.lane

def crash_test():
	for car in Cars[1:]:
		if Cars[0].crash_test(car) is True:
			return True
	return False
