import sys
from PySide2 import QtWidgets as qtw, QtGui as qtg, QtCore as qtc


class QSmartSliderWidget(qtw.QWidget):

    QStart = 0
    QMiddle = 1
    QEnd = 2

    QSlid = 0
    QStep = 1

    def __init__(
            self,
            *args,
            step: int = 5,
            **kwargs
            ) -> None:
        super().__init__(*args, **kwargs)

        self.__step = step
        self.__silder_type = self.QStep

    def paintEvent(self, event: qtg.QPaintEvent) -> None:

        qp = qtg.QPainter()
        qp.begin(self)

        font = qtg.QFont('Serif', 7, qtg.QFont.Light)
        qp.setFont(font)
        size = self.size()
        w = size.width()
        h = size.height()
        v = int(min(w/self.__step * .8, h * .8))

        for i in range(self.__step):
            x = int(((w/self.__step) * i) + ((w/self.__step) - v) * .5)
            y = int((h - v) / 2)
            qp.drawRect(qtc.QRect(x, y, v, v))

        qp.end()

    def mouseMoveEvent(self, event: qtg.QMouseEvent) -> None:

        super().mouseMoveEvent(event)
        self.update()
        x = event.pos().x()
        y = event.pos().y()
        p = self.mapToGlobal(event.pos())
        qtw.QToolTip.showText(p, f'{x}:{y}')


if __name__ == '__main__':

    app = qtw.QApplication(sys.argv)
    wdg = QSmartSliderWidget(step=9)
    wdg.show()
    app.exec_()
