# Car

Tests time to collision for autonomous cars.

## How to Run
To run the simulation, use the following command:
```bash
python3 simulator.py
```

## File Descriptions
- **Template.py**: Contains all the general functions.
- **Constant.py**: Contains all the constants.
- **Car.py**: Contains the `Car` class.
- **Simulator.py**: Implements the decision function and simulator for time to collision.

## Scenario Description
The simulation considers the following scenario:

- **myCar** is in lane 1, traveling in the same direction as **car1**.
- **car2** is in lane 0, traveling in the opposite direction of **myCar**.

### Speed and Position Configuration
The speed and position of the cars can be edited in the top section of `simulator.py` under the following block:

```python
############## SPEED and POSITIONS ############## 

# Units: meter and second

myCar_SPEED = 15.2
car1_SPEED = 14
car2_SPEED = -14.5

myCar_POSITION = 0
car1_POSITION = 60
car2_POSITION = 120
```

Adjust these values as needed to simulate different scenarios.
