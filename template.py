from constant import *

class position:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def x(self):
		return self.x
	def y(self):
		return self.y
	def add(self, x, y):
		self.x += x
		self.y += y

def collide(pointA, pointB):
	if (pointA[1] < pointB[0]) or (pointB[1] < pointA[0]):
		return False
	return True

def process_log(Log):
	Compressed = [(Log[0], 1)]
	for log in Log:
		if Compressed[-1][0] == log:
			Compressed[-1] = (log, Compressed[-1][1] + 1)
		else:
			Compressed.append((log, 1))
	print(f"Total Time = {len(Log) / FPS}s\n")
	for cur in Compressed:
		print(f"{cur[0]} {cur[1]/FPS}s")


