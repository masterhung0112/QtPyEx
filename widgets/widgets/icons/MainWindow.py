from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGroupBox, QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy, QStyleFactory, QMessageBox, QButtonGroup, QTableWidget, QAbstractItemView, QHeaderView, QRadioButton, QStyle, QSpinBox, QHBoxLayout, QActionGroup, QAction, QFileDialog, QDialog, QTableWidgetItem, QComboBox, QItemDelegate
from PyQt5.QtGui import QKeySequence, QImageReader, QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QRegularExpression, QSize, QFileInfo, QDir, pyqtSignal

from IconPreviewArea import IconPreviewArea


class IconSizeSpinBox(QSpinBox):
	def __init__(self, *args):
		super(QSpinBox, self).__init__(*args)
		
	def textFromValue(self, value):
		return "{} x {}".format(value, value)
		
	def valueFromText(text):
		regExp = QRegularExpression("(\\d+)(\\s*[xx]\\s*\\d+)?")
		match = regExp.match(text)
		if match.isValid():
			return match.captured(1).toInt()
		return 0

class ImageDelegate(QItemDelegate):
	commitData = pyqtSignal()
	
	def __init__(self, *args):
		super(QItemDelegate, self).__init__(*args)
	
	def createEditor(self, parent, option, index):
		comboBox = QComboBox(parent)
		if index.column() == 1:
			comboBox.addItems(IconPreviewArea.iconModeNames())
		elif index.column() == 2:
			comboBox.addItems(IconPreviewArea.iconStateNames())
		comboBox.activated.connect(self.emitCommitData)
		return comboBox
		
	def emitCommitData(self):
		print("emitCommitData")
		self.commitData.emit()
	
	def setEditorData(self, comboBox, index):
		if comboBox is None:
			return
		pos = comboBox.findText(index.model().data(index), Qt.MatchExactly)
		comboBox.setCurrentIndex(pos)
		
	def setModelData(self, comboBox, model, index):
		if comboBox is None:
			return
		
		model.setData(index, comboBox.currentText())
	
class MainWindow(QMainWindow):
	
	sizeButtonGroup = None
	OtherSize = QStyle.PM_CustomBase
	otherSpinBox = None
	
	def createImagesGroupBox(self):
		imagesGroupBox = QGroupBox("Images")
		labels = ("Images", "Mode", "State")
		
		self.imagesTable = QTableWidget()
		self.imagesTable.setSelectionMode(QAbstractItemView.NoSelection)
		self.imagesTable.setItemDelegate(ImageDelegate(self))
		self.imagesTable.horizontalHeader().setDefaultSectionSize(90)
		self.imagesTable.setColumnCount(3)
		self.imagesTable.setHorizontalHeaderLabels(labels)
		self.imagesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.imagesTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
		self.imagesTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
		self.imagesTable.verticalHeader().hide()
		self.imagesTable.itemChanged.connect(self.changeIcon)
		
		layout = QVBoxLayout(imagesGroupBox)
		layout.addWidget(self.imagesTable)
		return imagesGroupBox
	
	def createIconSizeGroupBox(self):
		iconSizeGroupBox = QGroupBox("Icon Size")
		self.sizeButtonGroup = QButtonGroup(iconSizeGroupBox)
		self.sizeButtonGroup.setExclusive(True)
		
		self.sizeButtonGroup.buttonToggled.connect(self.triggerChangeSize)
		
		smallRadioButton = QRadioButton()
		smallRadioButton.setChecked(True)
		self.sizeButtonGroup.addButton(smallRadioButton, QStyle.PM_SmallIconSize)
		largeRadioButton = QRadioButton()
		self.sizeButtonGroup.addButton(largeRadioButton, QStyle.PM_LargeIconSize)
		toolBarRadioButton = QRadioButton()
		self.sizeButtonGroup.addButton(toolBarRadioButton, QStyle.PM_ToolBarIconSize)
		iconViewRadioButton = QRadioButton()
		self.sizeButtonGroup.addButton(iconViewRadioButton, QStyle.PM_IconViewIconSize)
		listViewRadioButton = QRadioButton()
		self.sizeButtonGroup.addButton(listViewRadioButton, QStyle.PM_ListViewIconSize)
		tabBarRadioButton = QRadioButton()
		self.sizeButtonGroup.addButton(tabBarRadioButton, QStyle.PM_TabBarIconSize)
		otherRadioButton = QRadioButton("Other:")
		self.sizeButtonGroup.addButton(otherRadioButton, self.OtherSize)
		self.otherSpinBox = IconSizeSpinBox()
		self.otherSpinBox.setRange(8, 256)
		spinBoxToolTip = "Enter a custom size within {}..{}".format(self.otherSpinBox.minimum(), self.otherSpinBox.maximum())
		self.otherSpinBox.setValue(64)
		self.otherSpinBox.setToolTip(spinBoxToolTip)
		otherRadioButton.setToolTip(spinBoxToolTip)
		
		self.otherSpinBox.valueChanged.connect(self.triggerChangeSize)
		
		otherSizeLayout = QHBoxLayout()
		otherSizeLayout.addWidget(otherRadioButton)
		otherSizeLayout.addWidget(self.otherSpinBox)
		otherSizeLayout.addStretch()
		
		layout = QGridLayout(iconSizeGroupBox)
		layout.addWidget(smallRadioButton, 0, 0)
		layout.addWidget(largeRadioButton, 1, 0)
		layout.addWidget(toolBarRadioButton, 2, 0)
		layout.addWidget(listViewRadioButton, 0, 1)
		layout.addWidget(iconViewRadioButton, 1, 1)
		layout.addWidget(tabBarRadioButton, 2, 1)
		layout.addLayout(otherSizeLayout, 3, 0, 1, 2)
		layout.setRowStretch(4, 1)
		
		return iconSizeGroupBox
	
	def loadImages(self, fileNames):
		for fileName in fileNames:
			row = self.imagesTable.rowCount()
			self.imagesTable.setRowCount(row + 1)
			fileInfo = QFileInfo(fileName)
			imageName = fileInfo.baseName()
			fileImage2x = fileInfo.absolutePath() + '/' + imageName + "@2x." + fileInfo.suffix()
			fileInfo2x = QFileInfo(fileImage2x)
			image = QImage(fileName)
			toolTip = "Directory: {}\nFile: {}\nFile@2x: {}\nSize: {}x{}".format(
				QDir.toNativeSeparators(fileInfo.absolutePath()), fileInfo.fileName(),
				fileInfo2x.fileName() if fileInfo2x.exists else "<None>",
				image.width(), image.height()
			)
			fileItem = QTableWidgetItem(imageName)
			fileItem.setData(Qt.UserRole, fileName)
			fileItem.setIcon(QIcon(QPixmap.fromImage(image)))
			fileItem.setFlags((fileItem.flags() | Qt.ItemIsUserCheckable)& ~Qt.ItemIsEditable)
			fileItem.setToolTip(toolTip)
			self.imagesTable.setItem(row, 0, fileItem)
			
			mode = QIcon.Normal
			state = QIcon.Off
			
			if self.guessModeStateAct.isChecked():
				if "_act" in imageName:
					mode = QIcon.Active
				elif "_dis" in imageName:
					mode = QIcon.Disabled
				elif "_sel" in imageName:
					mode = QIcon.Selected
				
				if "_on" in imageName:
					mode = QIcon.On
					
			modeItem = QTableWidgetItem(IconPreviewArea.iconModeNames()[IconPreviewArea.iconModes().index(mode)])
			modeItem.setToolTip(toolTip);
			self.imagesTable.setItem(row, 1, modeItem)
			stateItem = QTableWidgetItem(IconPreviewArea.iconStateNames()[IconPreviewArea.iconStates().index(state)])
			stateItem.setToolTip(toolTip);
			self.imagesTable.setItem(row, 2, stateItem)
			self.imagesTable.openPersistentEditor(modeItem)
			self.imagesTable.openPersistentEditor(stateItem)
			fileItem.setCheckState(Qt.Checked)
	
	def addImages(self, directory):
		fileDialog = QFileDialog(self, "Open Images", directory)
		mimeTypeFilters = []
		for mimeTypeName in QImageReader.supportedMimeTypes():
			mimeTypeFilters.append(str(mimeTypeName))
		mimeTypeFilters.sort()
		fileDialog.setMimeTypeFilters(mimeTypeFilters)
		fileDialog.selectMimeTypeFilter('image/png')
		fileDialog.setAcceptMode(QFileDialog.AcceptOpen)
		fileDialog.setFileMode(QFileDialog.ExistingFiles)
		if not self.nativeFileDialogAct.isChecked():
			fileDialog.setOption(QFileDialog.DontUseNativeDialog)
		if fileDialog.exec_() == QDialog.Accepted:
			self.loadImages(fileDialog.selectedFiles())
		
	def addSampleImages(self):
		self.addImages("C:/Users/hungbn/Pictures")
	
	def addOtherImages(self):
		pass
	
	def removeAllImages(self):
		self.imagesTable.setRowCount(0)
		self.changeIcon()
	
	def createActions(self):
		fileMenu = self.menuBar().addMenu("&File")
		addSampleImagesAct = QAction("Add &Sample Images...", self)
		addSampleImagesAct.triggered.connect(self.addSampleImages)
		fileMenu.addAction(addSampleImagesAct)
		
		addOtherImagesAct = QAction("&Add Images...", self)
		addOtherImagesAct.setShortcut(QKeySequence.Open)
		addOtherImagesAct.triggered.connect(self.addOtherImages)
		fileMenu.addAction(addOtherImagesAct)
		
		removeAllImagesAct = QAction("&Remove All Images", self)
		removeAllImagesAct.setShortcut("CTRL+R")
		removeAllImagesAct.triggered.connect(self.removeAllImages)
		fileMenu.addAction(removeAllImagesAct)
		
		fileMenu.addSeparator()
		
		exitAct = QAction("&Quit", self)
		exitAct.triggered.connect(QWidget.close)
		exitAct.setShortcuts(QKeySequence.Quit)
		fileMenu.addAction(exitAct)
		
		viewMenu = self.menuBar().addMenu("&View")
		
		self.styleActionGroup = QActionGroup(self)
		for styleName in QStyleFactory.keys():
			action = QAction("{} Style".format(styleName), self.styleActionGroup)
			action.setData(styleName)
			action.setCheckable(True)
			action.triggered.connect(self.changeStyle)
			viewMenu.addAction(action)
		
		settingsMenu = self.menuBar().addMenu("&Settings")
		
		self.guessModeStateAct = QAction("&Guess Image Mode/State", self)
		self.guessModeStateAct.setCheckable(True)
		self.guessModeStateAct.setChecked(True)
		settingsMenu.addAction(self.guessModeStateAct)
		
		self.nativeFileDialogAct = QAction("&Use Native File Dialog", self)
		self.nativeFileDialogAct.setCheckable(True)
		self.nativeFileDialogAct.setChecked(True)
		settingsMenu.addAction(self.nativeFileDialogAct)
		
	
	def __init__(self, *args):
		super(QMainWindow, self).__init__(*args)
		
		centerWidget = QWidget(self)
		
		self.setCentralWidget(centerWidget)
		
		mainLayout = QGridLayout(centerWidget)
		
		previewGroupBox = QGroupBox("Preview")
		self.previewArea = IconPreviewArea(previewGroupBox)
		previewLayout = QVBoxLayout(previewGroupBox)
		previewLayout.addWidget(self.previewArea)
		
		mainLayout.addWidget(previewGroupBox, 0, 0, 1, 2)
		mainLayout.addWidget(self.createImagesGroupBox(), 1, 0)
		
		vbox = QVBoxLayout()
		vbox.addWidget(self.createIconSizeGroupBox())
		#vbox.addWidget(self.createHighDpiIconSizeGroupBox())
		vbox.addItem(QSpacerItem(0, 0, QSizePolicy.Ignored, QSizePolicy.MinimumExpanding))
		mainLayout.addLayout(vbox, 1, 1)
		
		self.createActions()
		
		self.setWindowTitle("Icons")
		self.checkCurrentStyle()
		
		
	
	def about(self):
		QMessageBox.about(self, "About Icons"
			"The <b>Icons</b> example illustrates how Qt renders an icon in " +
			"different modes (active, normal, disabled, and selected) and " +
			"states (on and off) based on a set of images."
		)
	
	def checkCurrentStyle(self):
		for action in self.styleActionGroup.actions():
			styleName = action.data()
			candidate = QStyleFactory.create(styleName)
			if candidate.metaObject().className() == QApplication.style().metaObject().className():
				action.trigger()
				return
	
	def changeStyle(self, checked):
		if (not checked):
			return
		
		action = self.sender()
		style = QStyleFactory.create(action.data())
		QApplication.setStyle(style)
		
		for button in self.sizeButtonGroup.buttons():
			metric = self.sizeButtonGroup.id(button)
			value = style.pixelMetric(metric)
			{
				QStyle.PM_SmallIconSize: lambda : button.setText("Small ({} x {})".format(value, value)),
				QStyle.PM_LargeIconSize: lambda : button.setText("Large ({} x {})".format(value, value)),
				QStyle.PM_ToolBarIconSize: lambda : button.setText("Toolbars ({} x {})".format(value, value)),
				QStyle.PM_ListViewIconSize: lambda : button.setText("List views ({} x {})".format(value, value)),
				QStyle.PM_IconViewIconSize: lambda : button.setText("Icon views ({} x {})".format(value, value)),
				QStyle.PM_TabBarIconSize: lambda : button.setText("Tab bars ({} x {})".format(value, value)),
			}.get(metric, lambda: "")()
		
		self.triggerChangeSize()
	
	def changeIcon(self):
		icon = QIcon()
		
		for row in range(self.imagesTable.rowCount()):
			fileItem = self.imagesTable.item(row, 0)
			modeItem = self.imagesTable.item(row, 1)
			stateItem = self.imagesTable.item(row, 2)
			
			if fileItem.checkState() == Qt.Checked:
				modeIndex = IconPreviewArea.iconModeNames().index(modeItem.text())
				stateIndex = IconPreviewArea.iconStateNames().index(stateItem.text())
				mode = IconPreviewArea.iconModes()[modeIndex]
				state = IconPreviewArea.iconStates()[stateIndex]
				fileName = fileItem.data(Qt.UserRole)
				image = QImage(fileName)
				if not image.isNull():
					icon.addPixmap(QPixmap.fromImage(image), mode, state)
		
		self.previewArea.setIcon(icon)
	
	def changeSize(self, id, checked):
		if (not checked):
			return
		
		other = (id == self.OtherSize)
		extend = self.otherSpinBox.value() if other else QApplication.style().pixelMetric(id)
		self.previewArea.setSize(QSize(extend, extend))
		self.otherSpinBox.setEnabled(other)
	
	def triggerChangeSize(self):
		self.changeSize(self.sizeButtonGroup.checkedId(), True)