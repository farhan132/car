# Time: second
# Position: meters

from template import *
from constant import *
from car import *
import random

############## DECISION TEMPLATE ##############


def decision(myCar, time_to_car1, time_to_car2, time_to_car3):

    # First check if any car is trying to overtake

    # Safe Pass Time Constant
    
    Pass_Constant = 7

    if -time_to_car3 <= Pass_Constant:
         myCar.accelerate(-ACC_CAR)
         return "Deaccelerate"

    # Crossover Constant
    # This Variable Will Be Adjusted Via Machine Learning
    Crossover_Constant = 3 * LEN_CAR / myCar.speed

    # Risk Constant (Minimum Time Space Needs To Attempt A Crossover)
    Risk_Constant = Crossover_Constant * 1.5

    # Safe Time Constant
    Safe_Constant = 15

    # Already Switched Lanes
    if myCar.lane == 0:

        # Already Crossed The Car
        if time_to_car1 < 0:
            myCar.switch_lane()
            return "Crossed Back"

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
            return "Crossed Back"

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

    attempt_success = "Success"

    build_cars()
    add_endpoints()

    player = [Cars[0]]

    FRAME = 0

    while FRAME < MAX_FRAME:
        FRAME += 1
        if crash_test().split()[-1] == "Crash":
            attempt_success = crash_test()
            break
        
        for myCar in player: 

            myCar.hypo_lane()

            car1 = myCar.immediate(Cars)
            myCar.switch_lane()
            car2 = myCar.immediate(Cars)
            myCar.change_direction()
            car3 = myCar.immediate(Cars)
            myCar.switch_lane()
            myCar.change_direction()

            myCar.hypo_lane()

            time_to_car1 = myCar.time_to_collide(car1)
            time_to_car2 = myCar.time_to_collide(car2)
            time_to_car3 = myCar.time_to_collide(car3)

            #print(car1.speed, car2.speed, car3.speed)

            Log.append(decision(myCar, time_to_car1, time_to_car2, time_to_car3))

        
        data_cars = []

        for cars in Cars[:-4]:
            data_cars.append((cars.position, cars.lane))

        for cars in Cars:
            cars.update()
        
        Simulation_Log.append(data_cars)

    print(attempt_success)

    process_log(Log)


run()

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np
import constant  # Ensure constant.py defines Simulation_Log

# Car properties.
car_length = 4.7  # Length of each car in meters.
car_height = 0.1  # Visual height of the car.

# Retrieve the simulation log.
simulation_log = constant.Simulation_Log

# Determine number of cars from the first time step.
n_cars = len(simulation_log[0]) if simulation_log else 0

# Create a colormap for unique car colors.
cmap = plt.get_cmap('tab10', n_cars)
colors = [cmap(i) for i in range(n_cars)]

# Create the figure and axis.
fig, ax = plt.subplots(figsize=(10, 3))

# Create rectangle patches for each car using the starting frame.
car_rects = []
xs = []
if simulation_log:
    start_frame = simulation_log[0]
    for j, (pos, lane) in enumerate(start_frame):
        # The logged position is assumed to be the front of the car.
        x = pos - car_length  # Left edge of the car.
        y = lane - car_height / 2  # Center the car vertically in its lane.
        rect = patches.Rectangle((x, y), car_length, car_height, color=colors[j])
        ax.add_patch(rect)
        car_rects.append(rect)
        xs.extend([x, pos])
else:
    start_frame = []

# Set y-axis limits to cover the two lanes.
ax.set_ylim(-0.5, 1.5)

# Compute fixed x-axis limits from the starting frame.
if xs:
    min_x = min(xs)
    max_x = max(xs)
    margin = (max_x - min_x) * 0.1 if (max_x - min_x) > 0 else 1
    ax.set_xlim(min_x - margin, max_x + margin)
else:
    ax.set_xlim(0, 10)

# Animation update function.
def animate(i):
    time_step = simulation_log[i]
    for j, (pos, lane) in enumerate(time_step):
        # Update the rectangle's position.
        x = pos - car_length
        y = lane - car_height / 2
        car_rects[j].set_xy((x, y))
    ax.set_title(f"Time Step: {i}")
    return car_rects

# Create the animation; note blit is disabled.
ani = animation.FuncAnimation(
    fig, animate, frames=len(simulation_log),
    interval=2, blit=False, repeat=True
)

ax.set_xlabel("Position (meters)")
ax.set_ylabel("Lane")
plt.tight_layout()
plt.show()
