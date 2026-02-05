from PySide6.QtCore import QSize, Qt, QThread, QObject, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QComboBox, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QInputDialog, QLineEdit, QSizePolicy, QCheckBox, QGridLayout

import RASgraphs as rg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib import gridspec

app = QApplication([])

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, height_ratios = [10, 1]):
        self.fig, self.axes = plt.subplots(2, 1, height_ratios = [10, 1])
        self.axes[1].get_yaxis().set_visible(False)
        plt.subplots_adjust(hspace = 0.0)
        super().__init__(self.fig)

    def colormap(self):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)


    def normalxrd(self):
        self.fig.clear()
        gs = gridspec.GridSpec(2, 1, height_ratios=[10, 1], hspace = 0.0)
        ax = self.fig.add_subplot(gs[0])
        ax2 = self.fig.add_subplot(gs[1])
        self.axes = [ax, ax2]
        self.axes[1].get_yaxis().set_visible(False)


class mainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.plots = [[]]
        self.files = []
        self.lefts = []
        self.rights = []
        self.spacings = [0.2]
        self.cutoffs = []
        self.titles = []
        self.labels = []
        self.amorphs = []
        self.colors = []
        self.axes = [[0, 1]]
        self.offsets = []
        self.cmapys = [[]]

        self.plot_ind = 0
        self.cur_ind = 0
        self.line_ind = 0
        self.display_ind = 1
        self.left = 0
        self.right = 1
        self.spacing = 0.2
        self.cutoff = 15
        self.title = "XRD Results"
        self.label = "XRD Results"
        self.amorphous = False
        self.color = "Blue"
        self.offset = 0
        self.cmapy = 1
        self.log = False
        self.cmaplabel = "Measurement"

        self.sc = MplCanvas(self)

        self.setMinimumSize(QSize(700, 400))
        self.setWindowTitle("RAS Grapher")

        mlayout = QGridLayout()
        slayout = QVBoxLayout()
        flayout = QVBoxLayout()
        clrlayout = QHBoxLayout()
        amlayout = QHBoxLayout()

        lrlayout = QVBoxLayout()
        splayout = QHBoxLayout()
        axeslayout = QVBoxLayout()

        linelayout = QHBoxLayout()
        hahalayout = QHBoxLayout()
        tlayout = QHBoxLayout()
        llayout = QHBoxLayout()
        nblayout = QVBoxLayout()
        textlayout = QVBoxLayout()
        toolslayout = QVBoxLayout()

        ctlayout = QHBoxLayout()
        ofslayout = QHBoxLayout()
        colorlayout = QHBoxLayout()

        cmapylayout = QHBoxLayout()
        cmaplabellayout = QHBoxLayout()

        self.addplot = QPushButton("Add Plot", self)
        self.addplot.clicked.connect(self.addPlot)
        self.button =  QPushButton("Open Files", self)
        self.button.clicked.connect(self.openFileDialog)
        self.filename = QLabel("  Current File: ")
        self.filename.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.clearlabel = QLabel("Clear Graphs ")
        self.clearlabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.clear = QCheckBox()
        self.clear.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.clear.checkStateChanged.connect(self.clearGraphsClicked)
        self.amorphlabel = QLabel("  Amorphous? ")
        self.amorphlabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.amorph = QCheckBox()
        self.amorph.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.amorph.checkStateChanged.connect(self.updateAmorphous)
        self.chooselabel = QLabel("Which Graph? ")
        self.chooseline = QLineEdit(f"{self.display_ind}", self)
        self.chooseline.returnPressed.connect(self.updateLine)
        self.titlelabel = QLabel("Set Title: ")
        self.settitle = QLineEdit(self.title, self)
        self.settitle.returnPressed.connect(self.updateTitle)
        self.labellabel = QLabel("Set Label: ")
        self.setlabel = QLineEdit(self.label, self)
        self.setlabel.returnPressed.connect(self.updateLabel)
        self.leftlabel = QLabel("Set Axis Left: ")
        self.axisleft = QLineEdit(f"{self.left}", self)
        self.axisleft.returnPressed.connect(self.updateAxes)
        self.rightlabel = QLabel("Set Axis Right: ")
        self.axisright = QLineEdit(f"{self.right}", self)
        self.axisright.returnPressed.connect(self.updateAxes)
        self.spacelabel = QLabel("Set spacing (degrees):")
        self.setspace = QLineEdit(f"{self.spacing}", self)
        self.setspace.returnPressed.connect(self.updateSpacing)
        self.cutofflabel = QLabel("Set peak cutoff:")
        self.cutofflabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setcutoff = QLineEdit(f"{self.cutoff}", self)
        self.setcutoff.returnPressed.connect(self.updateCutoff)
        self.offsetlabel = QLabel("Set Offset: ")
        self.setoffset = QLineEdit(f"{self.offset}", self)
        self.setoffset.returnPressed.connect(self.updateOffset)
        self.colorlabel = QLabel("Set Color:")
        self.setcolor = QLineEdit(f"{self.color}", self)
        self.setcolor.returnPressed.connect(self.updateColor)
        self.next = QPushButton("Next", self)
        self.back = QPushButton("Back", self)
        self.next.clicked.connect(self.nextPlot)
        self.back.clicked.connect(self.prevPlot)
        self.animate = QPushButton("Animate", self)
        self.animate.clicked.connect(self.Animate)
        self.hahalabel = QLabel("Debug Peak Graphs ")
        self.hahalabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.haha = QCheckBox()
        self.haha.checkStateChanged.connect(self.updateGraph)
        self.cmapYlabel = QLabel("Set Color Map Y: ")
        self.setcmapY = QLineEdit(f"{self.display_ind}")
        self.setcmapY.returnPressed.connect(self.updateCMapY)
        self.cmaplabellabel = QLabel("Set Color Map Label: ")
        self.setcmaplabel = QLineEdit(f"{self.cmaplabel}")
        self.setcmaplabel.returnPressed.connect(self.updateCMapLabel)
        self.plotchoice = QComboBox()
        self.plotchoice.addItem("XRD Graph")
        self.plotchoice.addItem("Colormap, Regular Scale")
        self.plotchoice.addItem("Colormap, Log Scale")
        self.plotchoice.setCurrentIndex(0)
        self.plotchoice.currentIndexChanged.connect(self.updateGraph)
        self.save = QPushButton("Save", self)
        self.save.clicked.connect(self.saveFileDialog)
        
        
        #self.setCentralWidget(sc)
        mlayout.setSpacing(0)
        self.sidebar = QWidget()
        self.sidebar.setLayout(slayout)
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        mlayout.addWidget(self.sidebar, 0, 0, 1, 1)
        mlayout.addWidget(self.sc, 0, 1, 1, 9)
        slayout.addWidget(self.addplot)
        slayout.addWidget(self.button)

        clrlayout.setSpacing(0)
        clrlayout.addWidget(self.clearlabel)
        clrlayout.addWidget(self.clear)
        amlayout.addWidget(self.amorphlabel)
        amlayout.addWidget(self.amorph)
        flayout.addLayout(clrlayout)
        flayout.addLayout(amlayout)
        flayout.addWidget(self.filename)
        slayout.addLayout(flayout)

        nblayout.addWidget(self.back)
        nblayout.addWidget(self.next)
        slayout.addLayout(nblayout)

        tlayout.addWidget(self.titlelabel)
        tlayout.addWidget(self.settitle)
        textlayout.addLayout(tlayout)

        llayout.addWidget(self.labellabel)
        llayout.addWidget(self.setlabel)
        textlayout.addLayout(llayout)

        linelayout.addWidget(self.chooselabel)
        linelayout.addWidget(self.chooseline)
        toolslayout.addLayout(linelayout)

        hahalayout.addWidget(self.hahalabel)
        hahalayout.addWidget(self.haha)
        toolslayout.addLayout(hahalayout)
        
        splayout.addWidget(self.spacelabel)
        splayout.addWidget(self.setspace)
        axeslayout.addLayout(splayout)

        lrlayout.addWidget(self.leftlabel)
        lrlayout.addWidget(self.axisleft)
        lrlayout.addWidget(self.rightlabel)
        lrlayout.addWidget(self.axisright)
        axeslayout.addLayout(lrlayout)
        
        ctlayout.addWidget(self.cutofflabel)
        ctlayout.addWidget(self.setcutoff)
        toolslayout.addLayout(ctlayout)

        ofslayout.addWidget(self.offsetlabel)
        ofslayout.addWidget(self.setoffset)
        toolslayout.addLayout(ofslayout)

        colorlayout.addWidget(self.colorlabel)
        colorlayout.addWidget(self.setcolor)
        toolslayout.addLayout(colorlayout)

        cmapylayout.addWidget(self.cmapYlabel)
        cmapylayout.addWidget(self.setcmapY)

        cmaplabellayout.addWidget(self.cmaplabellabel)
        cmaplabellayout.addWidget(self.setcmaplabel)
        
        slayout.addLayout(axeslayout)
        slayout.addLayout(toolslayout)
        slayout.addLayout(textlayout)
        slayout.addWidget(self.animate)
        slayout.addLayout(cmapylayout)
        slayout.addLayout(cmaplabellayout)
        slayout.addWidget(self.plotchoice)
        slayout.addWidget(self.save)
                
        self.widget = QWidget()
        self.widget.setLayout(mlayout)
        self.setCentralWidget(self.widget)

    def addPlot(self):
        self.plots.append([])
        self.axes.append([0, 1])
        self.spacings.append(0.2)
        self.cmapys.append([])
        self.left = 0
        self.right = 1
        self.spacing = 0.2
        self.plot_ind = len(self.plots)-1
        self.clearGraphs()
        self.sc.draw_idle()
        self.updateLabels()

    def openFileDialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            for i in range(len(selected_files)):
                self.files.append(selected_files[i])
                self.cutoffs.append(self.cutoff)
                self.offsets.append(self.offset)
                self.titles.append(self.title)
                self.labels.append(self.label)
                self.amorphs.append(self.amorphous)
                self.colors.append(self.color)
                self.cur_ind = len(self.files)-1
                self.line_ind = len(self.plots[self.plot_ind])
                self.display_ind = self.line_ind + 1
                self.cmapy = self.display_ind
                self.cmapys[self.plot_ind].append(self.cmapy)
                self.plots[self.plot_ind].append(self.cur_ind)
                theta, intensity = rg.file_read_gen(self.files[self.cur_ind])
                self.left = theta[0]
                self.right = theta[len(theta)-1]
                self.axes[self.plot_ind] = [self.left, self.right]
                print(self.cur_ind)
                print("Selected File:", self.files[self.cur_ind])
            self.updateLabels()
            self.updateGraph()
            
    def saveFileDialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            plt.savefig(selected_files[0])
            
    def clearGraphs(self):
        self.sc.fig.clear()
        if(self.plotchoice.currentIndex() == 0):
            self.sc.normalxrd()
        else:
            self.sc.colormap()

    def updateTitle(self):
        self.title = self.settitle.text()
        self.titles[self.plots[self.plot_ind][self.line_ind]] = self.title
        self.updateGraph()

    def updateLabel(self):
        self.label = self.setlabel.text()
        self.labels[self.plots[self.plot_ind][self.line_ind]] = self.label
        self.updateGraph()

    def updateSpacing(self):
        self.spacing = float(self.setspace.text())
        self.spacings[self.plots[self.plot_ind][self.line_ind]] = self.spacing
        self.updateGraph()

    def updateCutoff(self):
        self.cutoff = float(self.setcutoff.text())
        self.cutoffs[self.plots[self.plot_ind][self.line_ind]] = self.cutoff
        self.updateGraph()

    def updateColor(self):
        self.color = self.setcolor.text()
        self.colors[self.plots[self.plot_ind][self.line_ind]] = self.color
        self.updateGraph()

    def updateOffset(self):
        self.offset = int(self.setoffset.text())
        self.offsets[self.plots[self.plot_ind][self.line_ind]] = self.offset
        self.updateGraph()

    def nextPlot(self):
        if(self.plot_ind < len(self.plots)-1):
            self.plot_ind += 1
            self.updateGraph()
            self.updateLine()

    def prevPlot(self):
        if(self.plot_ind > 0):
            self.plot_ind -= 1
            self.updateGraph()
            self.updateLine()

    def Animate(self):
        rg.custom_smro_animation_ras(self.files, self.spacing)

    def updateGraph(self):
        print(self.plotchoice.currentIndex())
        if(self.plotchoice.currentIndex() == 0):
            self.updateXRD()
        elif(self.plotchoice.currentIndex() == 1):
            self.log = False
            self.updateCMap()
        else:
            self.log = True
            self.updateCMap()

    def updateXRD(self):
        self.sc.normalxrd()
        print(len(self.plots[self.plot_ind]))
        for i in range(len(self.plots[self.plot_ind])):
            self.cur_ind = self.plots[self.plot_ind][i]
            self.nohahaGraph()
            if(self.haha.isChecked()):
                #rg.custom_smro_hahaplot_ras(self.files[self.cur_ind], self.title, self.spacing, self.sc.axes)
                rg.plot_haha2_ras_gen(self.sc.axes, 0, self.files[self.cur_ind], self.title, "cyan", "haha2", self.spacing, axis_vis = False, amorphous = self.amorphous)
        rg.change_axes(self.sc.axes, self.axes[self.plot_ind], self.spacing)

    def nohahaGraph(self):
        rg.custom_plot_gen(self.sc.axes, self.files[self.cur_ind], self.titles[self.cur_ind], self.colors[self.cur_ind], self.labels[self.cur_ind], self.spacings[self.plot_ind], self.cutoffs[self.cur_ind], offset = self.offsets[self.cur_ind], amorphous = self.amorphs[self.cur_ind])
        #rg.custom_smro_plot_ras(self.files[self.cur_ind], self.cutoff, self.spacing, self.sc.axes)
        
        self.sc.draw_idle() 
    
    def clearGraphsClicked(self):
        if(self.clear.isChecked):
            self.clearGraphs()
            self.sc.draw_idle()

    def updateAmorphous(self):
        if(self.amorphous):
            self.amorphous = False
        else:
            self.amorphous = True
        print(self.amorphous)
        self.amorphs[self.plots[self.plot_ind][self.line_ind]] = self.amorphous
        self.updateGraph()

    def updateLine(self):
        self.line_ind = int(self.chooseline.text())-1
        self.display_ind = self.line_ind + 1
        self.updateLabels()
    
    def updateLabels(self):
        self.spacing = self.spacings[self.plot_ind]
        self.cutoff = self.cutoffs[self.plots[self.plot_ind][self.line_ind]]
        self.title = self.titles[self.plots[self.plot_ind][self.line_ind]]
        self.label = self.labels[self.plots[self.plot_ind][self.line_ind]]
        self.amorphous = self.amorphs[self.plots[self.plot_ind][self.line_ind]]
        self.color = self.colors[self.plots[self.plot_ind][self.line_ind]]
        self.cmapy = self.cmapys[self.plot_ind][self.line_ind]
        self.axisleft.setText(f"{self.left}")
        self.axisright.setText(f"{self.right}")
        self.chooseline.setText(f"{self.display_ind}")
        self.settitle.setText(self.title)
        self.setlabel.setText(self.label)
        self.setspace.setText(f"{self.spacing}")
        self.setcutoff.setText(f"{self.cutoff}")
        self.setcmapY.setText(f"{self.cmapy}")
        if (len(self.files[self.cur_ind]) > 30):
            self.filename.setText("Current File: ..." + self.files[self.line_ind][-30:])
        else:
            self.filename.setText("Current File: " + self.files[self.line_ind])
        self.update()

    def updateAxes(self):
        self.left = float(self.axisleft.text())
        self.right = float(self.axisright.text())
        new_axes = [self.left, self.right]
        self.axes[self.plot_ind] = new_axes
        rg.change_axes(self.sc.axes, new_axes, self.spacing)
        self.sc.draw_idle()

    def updateCMapY(self):
        self.cmapy = float(self.setcmapY.text())
        self.cmapys[self.plot_ind][self.line_ind] = self.cmapy
        self.updateGraph()

    def updateCMap(self):
        self.sc.colormap()
        rg.color_map(self.sc.fig, self.sc.axes, self.plots, self.plot_ind, self.files, self.cmapys, self.title, self.cmaplabel, self.log)
        self.sc.draw_idle() 

    def updateCMapLabel(self):
        self.cmaplabel = self.setcmaplabel.text()
        self.updateGraph()
    
window = mainWindow()
window.show()

if __name__ == "__main__":
    app.exec()
