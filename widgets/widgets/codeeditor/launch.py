import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject

from codeeditor import CodeEditor

def main():
	app = QApplication(sys.argv)
	codeeditor = CodeEditor()
	codeeditor.setWindowTitle(app.tr("Code editor example"))
	codeeditor.show()
	
	return app.exec_()


if __name__ == "__main__":
	main()