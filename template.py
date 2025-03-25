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



####### INPUT 2 ########



import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QScrollArea, QMessageBox
)

class CarInputWidget(QWidget):
    def __init__(self, car_number, parent=None):
        super().__init__(parent)
        self.car_number = car_number
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        # Title for the car panel
        title_label = QLabel(f"Car {self.car_number}")
        title_label.setStyleSheet("font-weight: bold; font-size: 14pt;")
        layout.addWidget(title_label)
        
        # Parameters and their default values
        self.fields = {}
        parameters = [("Speed", "60"), ("Position", "0"), ("Height", "2"),
                      ("Lane", "1"), ("Direction", "1"), ("Max Speed", "120")]
        for param, default in parameters:
            row_layout = QHBoxLayout()
            param_label = QLabel(param)
            line_edit = QLineEdit(default)
            row_layout.addWidget(param_label)
            row_layout.addWidget(line_edit)
            layout.addLayout(row_layout)
            self.fields[param] = line_edit
        
        self.setLayout(layout)
    
    def get_data(self):
        try:
            speed = float(self.fields["Speed"].text())
            position = float(self.fields["Position"].text())
            height = float(self.fields["Height"].text())
            lane = int(self.fields["Lane"].text())
            direction = int(self.fields["Direction"].text())
            max_speed = float(self.fields["Max Speed"].text())
            return (speed, position, height, lane, direction, max_speed)
        except ValueError:
            raise ValueError(f"Invalid input in Car {self.car_number}. Please check your values.")

class CarInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.car_widgets = []
        self.car_data = []
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Car Parameters Input")
        self.resize(700, 500)
        
        main_layout = QVBoxLayout(self)
        
        # Main title label
        title = QLabel("Enter Car Parameters")
        title.setStyleSheet("font-size: 16pt; margin-bottom: 10px;")
        main_layout.addWidget(title)
        
        # Scroll area for car panels
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.cars_container = QWidget()
        self.cars_layout = QVBoxLayout()
        self.cars_container.setLayout(self.cars_layout)
        self.scroll_area.setWidget(self.cars_container)
        main_layout.addWidget(self.scroll_area)
        
        # Button layout
        buttons_layout = QHBoxLayout()
        add_button = QPushButton("Add Car")
        add_button.clicked.connect(self.add_car)
        remove_button = QPushButton("Remove Car")
        remove_button.clicked.connect(self.remove_car)
        done_button = QPushButton("Done")
        done_button.clicked.connect(self.on_done)  # Changed here
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(remove_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(done_button)
        main_layout.addLayout(buttons_layout)
        
        # Add one car panel by default
        self.add_car()
    
    def add_car(self):
        car_number = len(self.car_widgets) + 1
        widget = CarInputWidget(car_number)
        self.car_widgets.append(widget)
        self.cars_layout.addWidget(widget)
    
    def remove_car(self):
        if self.car_widgets:
            widget = self.car_widgets.pop()
            self.cars_layout.removeWidget(widget)
            widget.deleteLater()
        else:
            QMessageBox.warning(self, "Warning", "No car panel to remove.")
    
    def on_done(self, checked=False):  # Renamed slot method
        self.car_data = []
        print("INPUT COMPLETED")
        for widget in self.car_widgets:
            try:
                data = widget.get_data()
                self.car_data.append(data)
            except ValueError as e:
                QMessageBox.critical(self, "Input Error", str(e))
                return
        self.accept()  # Close the dialog with an accepted status

def INPUT2():
    """
    Launches a PyQt5-based input panel for car parameters.
    Returns a list of tuples containing the car data.
    """
    app = QApplication(sys.argv)
    dialog = CarInputDialog()
    if dialog.exec_() == QDialog.Accepted:
        return dialog.car_data
    return None