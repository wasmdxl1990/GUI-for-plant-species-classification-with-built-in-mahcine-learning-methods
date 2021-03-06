"""
@author: Zhangjian Ouyang
@date: 10/25/2018
This file is GUI of project of CS501
"""
from Neat_projectcode import Class_prediction
import morphologicalfeatures
import binary_image
import cv2
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication, Qt
from Segmentation_Correction import seg_cor
global species_name
global species_pro
species_name = [0, 0, 0]
species_pro = [0, 0, 0]


DIR_INPUT = 'C:/Users/ma125/OneDrive - purdue.edu/2018 Fall/CS501/Project/' 
DIR_INPUT1 = 'C:/Users/ma125/OneDrive - purdue.edu/2018 Fall/CS501/Project' 

# class DraggableLabel(QLabel):
#     def __init__(self,parent,image):
#         super(QLabel,self).__init__(parent)
#         self.setPixmap(QPixmap(image))
#         self.show()
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.drag_start_position = event.pos()
#
#     def mouseMoveEvent(self, event):
#         if not (event.buttons() & Qt.LeftButton):
#             return
#         if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
#             return
#         drag = QDrag(self)
#         mimedata = event.mimeData()
#         mimedata.setText(self.text())
#         mimedata.setImageData(self.pixmap().toImage())
#
#         drag.setMimeData(mimedata)
#         pixmap = QPixmap(self.size())
#         painter = QPainter(pixmap)
#         painter.drawPixmap(self.rect(), self.grab())
#         painter.end()
#         drag.setPixmap(pixmap)
#         drag.setHotSpot(event.pos())
#         drag.exec_(Qt.CopyAction | Qt.MoveAction)


class Label(QLabel):
    """
    Enable the label can be dropped
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.path = ""
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
            print("Yes")
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text())
        temp_path = e.mimeData().text()
        print(temp_path)
        self.path = temp_path[8:]
        print(self.path)

    def get_path(self):
        print("get_path", self.path)
        return self.path


class GUI(QWidget):
    """
    Main class
    """
    def __init__(self):
        super().__init__()
        self.timer_camera = QtCore.QTimer()
        # self.cap = cv2.VideoCapture(0)
        # self.filename = "filename"
        self.initUI()
        # self.slot_init()

    def slot_init(self):
        """
        Initialize the slot
        :return:
        """
        self.timer_camera.start(30)
        self.timer_camera.timeout.connect(self.pic_capture)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawBrushes(qp)
        qp.end()

    def drawBrushes(self, qp):
        brush = QBrush(Qt.NoBrush)
        qp.setBrush(brush)
        qp.drawRect(1200, 40, 450, 600)
        qp.drawRect(40, 40, 1120, 600)

    def initUI(self):
        """
        Setup the GUI
        :return:
        """

        # chart
        self.graphicview = QtWidgets.QGraphicsView()
        # chart = Figure_Canvas()
        # chart.test()
        # graphicscene = QtWidgets.QGraphicsScene()
        # graphicscene.addWidget(chart)
        # self.graphicview.setWindowTitle("Data")
        # self.graphicview.setScene(graphicscene)

        label0 = QLabel(self)
        label0.setText("Species")
        label0.setFont(QFont("Roman times", 8, QFont.Bold))
        label0.move(60, 660)
        self.qle0 = QLineEdit(self)
        self.qle0.move(60, 710)
        self.qle0.textChanged[str].connect(self.name)

        # label 1 shows the species
        label1 = QLabel(self)
        label1.setText("Predict Species")
        label1.setFont(QFont("Roman times", 8, QFont.Bold))
        label1.move(420, 660)
        self.qle1 = QLineEdit(self)
        self.qle1.move(420, 710)
        self.qle1.textChanged[str].connect(self.name)


        # label 2 shows the origin image
        self.label2 = Label(self)
        self.label2.resize(480, 480)
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.black)
        self.label2.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.gray)
        self.label2.setPalette(pe)
        self.label2.move(60, 100)

        # label 3 shows the processed image
        self.label3 = QLabel(self)
        self.label3.resize(480, 480)
        self.label3.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.gray)
        self.label3.setPalette(pe)
        self.label3.move(650, 100)

        # Orginal image label
        self.label4 = QLabel(self)
        self.label4.setAcceptDrops(True)
        self.label4.setText("Original Image")
        self.label4.setFont(QFont("Roman times", 8, QFont.Bold))
        self.label4.move(60, 60)

        # Process image label
        self.label5 = QLabel(self)
        self.label5.setText("Processed Image")
        self.label5.setFont(QFont("Roman times", 8, QFont.Bold))
        self.label5.move(650, 60)

        # Feature label
        self.label6 = QLabel(self)
        self.label6.setText("Feature")
        self.label6.setFont(QFont("Roman times", 8, QFont.Bold))
        self.label6.move(1250, 60)

        # Area label
        label7 = QLabel(self)
        label7.setText("Area")
        label7.move(1250, 100)
        self.qle7 = QLineEdit(self)
        self.qle7.move(1250, 150)

        # Perimeter label
        label8 = QLabel(self)
        label8.setText("Perimeter")
        label8.move(1250, 200)
        self.qle8 = QLineEdit(self)
        self.qle8.move(1250, 250)

        # MinL label
        label9 = QLabel(self)
        label9.setText("MinL")
        label9.move(1250, 300)
        self.qle9 = QLineEdit(self)
        self.qle9.move(1250, 350)

        # MaxL label
        label10 = QLabel(self)
        label10.setText("MaxL")
        label10.move(1250, 400)
        self.qle10 = QLineEdit(self)
        self.qle10.move(1250, 450)

        # Eccentricity label
        label11 = QLabel(self)
        label11.setText("Eccentricity")
        label11.move(1250, 500)
        self.qle11 = QLineEdit(self)
        self.qle11.move(1250, 550)


        # Quit button
        btn1 = QPushButton('Quit', self)
        btn1.clicked.connect(QCoreApplication.instance().quit)
        btn1.resize(btn1.sizeHint())
        btn1.move(1700, 500)

        # Species button
        btn2 = QPushButton('Species', self)
        btn2.clicked.connect(self.name)
        btn2.clicked.connect(self.graphicview.show)
        btn2.resize(btn2.sizeHint())
        btn2.move(1700, 300)

        # Load button
        btn3 = QPushButton('load', self)
        btn3.clicked.connect(self.loadFile)
        btn3.resize(btn3.sizeHint())
        btn3.move(1700, 100)

        # Process button
        btn4 = QPushButton('Process', self)
        btn4.clicked.connect(self.image_process)
        btn4.resize(btn4.sizeHint())
        btn4.move(1700, 200)

        self.setGeometry(600, 600, 2000, 800)
        pe.setBrush(self.backgroundRole(), QBrush(QPixmap(DIR_INPUT+'GUI/bg.jpg')))
        self.setPalette(pe)
        self.setWindowTitle('CS501: Green Leaf')
        self.show()
        # if cv2.waitKey(1) & 0xFF == ord('c'):
        #     self.cap.release()
        #     cv2.destroyAllWindows()


    def loadFile(self):
        """
        load image
        :return: image path
        """
        global fname
        print("load--file")
        fname, _ = QFileDialog.getOpenFileName(self, 'choose pic', DIR_INPUT1, 'Image files(*.jpg *.gif *.png)')
        pic1 = cv2.imread(fname)
        pic1 = cv2.resize(pic1, (480, 480), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(DIR_INPUT+'GUI/test.jpg', pic1)
        self.label2.setPixmap(QPixmap(DIR_INPUT+'GUI/test.jpg'))
        testID = int(fname[-8: -4])
        a, b, species_name, species_pro= Class_prediction(testID)
        print(species_name, species_pro)

        chart = Figure_Canvas(species_name, species_pro)
        chart.test()
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(chart)
        self.graphicview.setWindowTitle("Data")
        self.graphicview.setScene(graphicscene)

        return fname


    def name(self):
        """
        Show the species of the image
        :return:
        """
        testID = int(fname[-8: -4])
        a, b, species_name, species_pro= Class_prediction(testID)
        self.qle0.setText(a)
        self.qle1.setText(b)

    def data(self):
        testID = int(fname[-8: -4])
        return species_name, species_pro

    def image_process(self):
        """
        process image & extract features
        :return:
        """
        print(fname)
        
        seg_cor(fname,thresh = 150)
        pic = cv2.imread(DIR_INPUT+'GUI/first.jpg')
        pic = cv2.resize(pic, (480, 320), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(DIR_INPUT+'GUI/test2.jpg', pic)
        pic = QtGui.QPixmap(DIR_INPUT+'GUI/test2.jpg')
        self.label3.setPixmap(pic)
        fea = morphologicalfeatures.feature_extraction(DIR_INPUT+'GUI/second.jpg')
        self.qle7.setText(str("%0.3f"%fea["Area"]))
        self.qle8.setText(str("%0.3f"%fea["Perimeter"]))
        self.qle9.setText(str("%0.3f"%fea["MinL"]))
        self.qle10.setText(str("%0.3f"%fea["MaxL"]))
        self.qle11.setText(str("%0.3f"%fea["Eccentricity"]))


class Figure_Canvas(FigureCanvas):
    """
    Drawing chart with matplt
    """
    def __init__(self, species_name, species_pro, parent=None, width=10, height=6, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111)
        self.species_name = species_name
        self.species_pro = species_pro

    def test(self):
        print(self.species_pro)
        print(self.species_name)
        x = [self.species_name[0], self.species_name[1], self.species_name[2]]
        y = [self.species_pro[0], self.species_pro[1], self.species_pro[2]]
        width = 0.5
        self.axes.bar([0, 1, 2], y, width, align="center")
        self.axes.set_xticks([0, 1, 2])
        self.axes.set_xticklabels(x)
        self.axes.set_ylabel('possibility %')
        # x1 = ['SVM', 'RR', 'RT', 'Kmeans']
        # y1 = [50, 80, 20, 90]
        # width = 0.5
        # self.axes1.bar([0, 1, 2, 3], y1, width, align="center", color='green')
        # self.axes1.set_xticks([0, 1, 2, 3])
        # self.axes1.set_xticklabels(x1)
        # self.axes1.set_ylabel('possibility %')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
