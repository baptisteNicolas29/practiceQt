from Qt import QtWidgets, QtCore, QtGui


class QRadialMenu(QtWidgets.QWidget):

    ShapeArc = 0
    ShapeLine = 1
    ShapeDots = 2
    aboutToHide = QtCore.Signal()
    aboutToShow = QtCore.Signal()

    hovered = QtCore.Signal(QtWidgets.QAction)
    triggered = QtCore.Signal(QtWidgets.QAction)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.__rotation = - 90
        self.__actions = []
        self.__shapes = []

        self.__previous_hovered = None

    def rotation(self) -> float:
        return self.__rotation

    def setRotation(self, value: float) -> None:
        self.__rotation = value

    def addAction(self, action: QtWidgets.QAction) -> QtWidgets.QAction:
        self.__actions.append(action)
        action.setParent(self)
        self.__shapes.append(QtGui.QPainterPath())

        self.repaint()
        return action

    def actionGeometry(self, act: QtWidgets.QAction) -> QtGui.QPainterPath:
        return self.__shapes[self.__actions.index(act)]

    def actionAt(self, point: QtCore.QPoint) -> None:

        for idx, shp in enumerate(self.__shapes):
            if shp.contains(point):
                return self.__actions[idx]

        else:
            return None

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        action_len = len(self.__actions)
        cursor_pos = self.mapFromGlobal(QtGui.QCursor.pos())
        center = QtCore.QPointF(self.width() / 2, self.height() / 2)
        outerRadius = min([self.height(), self.width()]) / 3
        innerRadius = outerRadius / 4

        innerRect = QtCore.QRectF(
                center - QtCore.QPointF(innerRadius, innerRadius),
                center + QtCore.QPointF(innerRadius, innerRadius),
                )

        outerRect = QtCore.QRectF(
                center - QtCore.QPointF(outerRadius, outerRadius),
                center + QtCore.QPointF(outerRadius, outerRadius),
                )

        # draw backgroud
        painter: QtGui.QPainter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 3, QtCore.Qt.DashLine))

        if action_len == 0:
            painter.drawEllipse(
                    center,
                    outerRadius / 2,
                    outerRadius / 2
                    )

            painter.drawEllipse(
                    QtCore.QPointF(self.width() / 2, self.height() / 2,),
                    outerRadius / 4,
                    outerRadius / 4
                    )

        for idx, shp in enumerate(self.__shapes):
            angleSize = 360 / action_len
            startAngle = idx * angleSize + self.__rotation

            shp.clear()
            shp.moveTo(
                    center + QtCore.QLineF.fromPolar(innerRadius, startAngle).p2()
                    )
            shp.arcTo(innerRect, startAngle, angleSize)
            shp.lineTo(
                    center + QtCore.QLineF.fromPolar(
                        outerRadius, startAngle + angleSize
                        ).p2()
                    )
            shp.arcTo(outerRect, startAngle + angleSize, -angleSize)
            # shp.closeSubpath()

            if shp.contains(cursor_pos):
                shp.closeSubpath()
                painter.setPen(QtGui.QPen(QtCore.Qt.black, 3))
                painter.drawPath(shp)
                painter.setPen(QtGui.QPen(QtCore.Qt.black, 3, QtCore.Qt.DashLine))

            else:
                painter.drawPath(shp)

        painter.end()

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        print(self.actionAt(event.pos()))
        super().mouseDoubleClickEvent(event)

    def enterEvent(self, event):
        pass
        # print('hoverEnterEvent')

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        self.repaint()

        if action := self.actionAt(event.pos()):
            if action != self.__previous_hovered:
                self.hovered.emit(action)
                self.__previous_hovered = action

        else:
            self.__previous_hovered = None

        return super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        pass
        # print('hoveLeaveEvent')

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if action := self.actionAt(event.pos()):
            self.triggered.emit(action)

        return super().mousePressEvent(event)


if __name__ == "__main__":

    app = QtWidgets.QApplication()
    wdg = QRadialMenu()

    actions = []
    for x in ['new', 'open', 'save', 'save increment', 'exit']:
        act = wdg.addAction(QtWidgets.QAction(x))
        actions.append(act)

    wdg.triggered.connect(print)

    wdg.show()
    app.exec_()
