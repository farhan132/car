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
    
    # Pass_Constant = 7

    # if time_to_car3 <= Pass_Constant:
    #      myCar.accelerate(-ACC_CAR)
    #      return "Deaccelerate"

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
            car1 = myCar.immediate(Cars)
            myCar.switch_lane()
            car2 = myCar.immediate(Cars)
            myCar.change_direction()
            car3 = myCar.immediate(Cars)
            myCar.switch_lane()
            myCar.change_direction()

            time_to_car1 = myCar.time_to_collide(car1)
            time_to_car2 = myCar.time_to_collide(car2)
            time_to_car3 = myCar.time_to_collide(car3)

            Log.append(decision(myCar, time_to_car1, time_to_car2, time_to_car3))



        for cars in Cars:
            cars.update()

    print(attempt_success)

    process_log(Log)


run()
