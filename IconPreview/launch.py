import sys
from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow

def main():
	app = QApplication(sys.argv)
	app.setApplicationName("Icons")
	app.setApplicationVersion("1.0")
	mainWin = MainWindow()
	mainWin.show()
	
	return app.exec_()


if __name__ == "__main__":
	main()