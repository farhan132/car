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


def process_log(Log, mod = 1):
    Log = Log[mod-1::mod]
    Compressed = [(Log[0], 1)]
    for log in Log:
        if Compressed[-1][0] == log:
            Compressed[-1] = (log, Compressed[-1][1] + 1)
        else:
            Compressed.append((log, 1))
    print(f"Total Time = {len(Log) / FPS}s\n")
    for cur in Compressed:
        print(f"{cur[0]} {cur[1]/FPS}s")


def fit(x, l, r):
    if l > r:
        l, r = r, l
    if x < l:
        return l
    if x > r:
        return r
    return x

def INPUT():
	# Open and read the file
	with open("input.txt", "r") as file:
	    # Read all lines from the file
	    lines = file.readlines()

	# Parse the remaining lines to create a list of lists
	data = []
	for line in lines:
	    # Convert each line to a list of numbers (float or int)
	    row = []
	    for value in line.split():
	        try:
	            num = float(value)
	            # Convert to int if it's a whole number
	            num = int(num) if num.is_integer() else num
	            row.append(num)
	        except ValueError:
	            print(f"Warning: Skipping invalid value {value}")
	    data.append(row)
	return data

