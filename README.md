# Car Simulation

**Tests time to collision (TTC) for autonomous cars and simulates lane-crossing decisions.**

## Features
- Basic simulation computing TTC and lane-switch decisions.
- Advanced simulation with logging and matplotlib animation.
- Optional GUI input for car parameters via PyQt5.

## Requirements
- Python 3.7 or higher
- Python packages:
  - matplotlib
  - numpy
  - PyQt5

Install dependencies:
```
pip install matplotlib numpy PyQt5
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/farhan132/car.git
   cd car
   ```

## Usage

### CLI Simulation
Run the basic simulator:
```
python3 simulator.py
```

### Complex Simulation with Animation
Run the advanced simulator:
```
python3 complex_simulator.py
```

### GUI Input (Optional)
To use the PyQt5-based car input dialog:
1. In `complex_simulator.py`, replace `build_cars()` with `Cars.extend(INPUT2())`.
2. Ensure PyQt5 is installed.
3. Run `complex_simulator.py`.

## Configuration
Edit speed and position parameters at the top of `simulator.py` and `complex_simulator.py`:
```python
# Example in simulator.py
myCar_SPEED = 15.2
car1_SPEED = 15
car2_SPEED = 14.5
```

## File Structure
- `car.py`               : Defines the `car` class and collision logic.
- `constant.py`          : Global constants and simulation logs.
- `template.py`          : Utility functions, logging, input parsing, and GUI components.
- `simulator.py`         : Basic TTC simulation with lane-switch decisions.
- `complex_simulator.py` : Advanced simulation with logging and animation.
- `input.txt`            : Sample input data for `simulator.py`.
- `.vscode/`, `__pycache__/`: Configuration and cache directories.

## Logging and Output
- Logs are printed to the console.
- Use `process_log(Log)` to summarize events and total simulation time.

## Contributing
Feel free to submit issues and pull requests.

## Author
farhan132 (https://github.com/farhan132)
