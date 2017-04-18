from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QFrame
from PyQt5.QtGui import QIcon, QPalette, QWindow, QPixmap, QImage

class IconPreviewArea(QWidget):
	
	NumModes = 4
	NumStates = 2
	size = 0
	icon = None
	
	def __init__(self, *args):
		super(QWidget, self).__init__(*args)
		
		self.mainLayout = QGridLayout(self)
		self.stateLabels = [None for i in range(self.NumStates)]
		self.modeLabels = [None for i in range(self.NumModes)]
		self.pixmapLabels = [[None for x in range(self.NumStates)] for y in range(self.NumModes)]
		
		self.icon = QIcon()
		
		for row in range(self.NumStates):
			self.stateLabels[row] = self.createHeaderLabel(self.iconStateNames()[row])
			self.mainLayout.addWidget(self.stateLabels[row], row + 1, 0)
		
		for column in range(self.NumModes):
			self.modeLabels[column] = self.createHeaderLabel(self.iconModeNames()[column])
			self.mainLayout.addWidget(self.modeLabels[column], 0, column + 1)
		
		for column in range(self.NumModes):
			for row in range(self.NumStates):
				self.pixmapLabels[column][row] = self.createPixmapLabel()
				self.mainLayout.addWidget(self.pixmapLabels[column][row], row + 1, column + 1)
		
	def createHeaderLabel(self, text):
		label = QLabel("<b>{}</b>".format(text))
		label.setAlignment(Qt.AlignCenter)
		return label
		
	
	def createPixmapLabel(self):
		label = QLabel()
		label.setEnabled(False)
		label.setAlignment(Qt.AlignCenter)
		label.setFrameShape(QFrame.Box)
		label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		label.setBackgroundRole(QPalette.Base)
		label.setAutoFillBackground(True)
		label.setMinimumSize(132, 132)
		return label
	
	@staticmethod
	def iconModes():
		return (QIcon.Normal, QIcon.Active, QIcon.Disabled, QIcon.Selected)
	
	@staticmethod
	def iconStates():
		return (QIcon.Off, QIcon.On)
	
	@staticmethod
	def iconModeNames():
		return ("Normal", "Active", "Disabled", "Selected")
	
	@staticmethod
	def iconStateNames():
		return ("Off", "On")
	
	def setIcon(self, icon):
		self.icon = icon
		self.updatePixmapLabels()
		
	def setSize(self, size):
		if self.size != size:
			self.size = size
			self.updatePixmapLabels()
	
	def updatePixmapLabels(self):
		window = None
		nativeParent = self.nativeParentWidget()
		
		if nativeParent is not None:
			window = nativeParent.windowHandle()
			
		for column in range(self.NumModes):
			for row in range(self.NumStates):
				pixmap = self.icon.pixmap(window, self.size, self.iconModes()[column], self.iconStates()[row])
				pixmapLabel = self.pixmapLabels[column][row]
				pixmapLabel.setPixmap(pixmap)
				pixmapLabel.setEnabled(not pixmap.isNull())
				toolTip = None
				if not pixmap.isNull():
					actualSize = self.icon.actualSize(self.size)
					tooltip = "Size: {}x{}\nActual size: {}x{}\nDevice pixel ratio: {}".format(self.size.width(), self.size.height(), actualSize.width(), actualSize.height(), pixmap.devicePixelRatioF())
					#print(tooltip)
				pixmapLabel.setToolTip(toolTip)