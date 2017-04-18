import sys
from PyQt5.QtWidgets import QApplication

from AnalogClock import AnalogClock

def main():
	app = QApplication(sys.argv)
	analogClock = AnalogClock()
	analogClock.show()
	
	return app.exec_()


if __name__ == "__main__":
	main()