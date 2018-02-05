import sys
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsEllipseItem, \
    QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent, QGraphicsItem, QStyleOptionGraphicsItem
from PyQt5.QtGui import QPainter


class MovableDisk(QGraphicsEllipseItem):
    """ Provide a movable red disk w/o using itemIsMovable flag. If move_all is True will send position changes to
        parent."""
    def __init__(self, top_left_x, top_left_y, radius, move_all: bool=False, parent=None):
        super().__init__(0, 0, radius, radius, parent=parent)  # Init. to (0,0) to avoid bias in coordinate system...
        self.setPos(top_left_x, top_left_y)  # ...but we can use setPos to move the object.
        self.move_all = move_all
        if self.move_all is True:
            self.setBrush(Qt.green)
        else:
            self.setBrush(Qt.red)
        self.setAcceptHoverEvents(True)  # hover events are used to change mouse cursor

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent'):
        """When cursor enters the object, set cursor to open hand"""
        QApplication.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent'):
        """When cursor leaves the object, restore mouse cursor"""
        QApplication.instance().restoreOverrideCursor()

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        """mouseMoveEvent is called whenever a mouse button is pressed and the cursor is moved. """
        new_cursor_position = event.scenePos()  # mouse cursor in scene coordinates
        old_cursor_position = event.lastScenePos()
        offset_x = new_cursor_position.x() - old_cursor_position.x()
        offset_y = new_cursor_position.y() - old_cursor_position.y()
        if self.move_all is False:
            """Update single disk"""
            old_top_left_corner = self.scenePos()
            new_top_left_corner_x = offset_x + old_top_left_corner.x()
            new_top_left_corner_y = offset_y + old_top_left_corner.y()
            self.setPos(QPointF(new_top_left_corner_x, new_top_left_corner_y))  # update disk top left corner
        else:
            """Call parent to update everybody"""
            self.parentItem().move_everybody(offset_x, offset_y)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'): pass

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent'): pass

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent'): pass


class MovableGroup(QGraphicsItem):
    def __init__(self):
        super().__init__()
        """The children objects are painted as the parent is painted"""
        self.disks = [MovableDisk(50, 50, 10, move_all=False, parent=self),
                      MovableDisk(100, 100, 10, move_all=False, parent=self),
                      MovableDisk(100, 50, 10, move_all=True, parent=self)]

    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget=None):
        """This function needs to be reimplemented because the object is abstract"""
        pass

    def boundingRect(self):
        """This function needs to be reimplemented because the object is abstract"""
        return QRectF()

    def move_everybody(self, offset_x, offset_y):
        for disk in self.disks:
            current_position = disk.scenePos()
            new_position_x = current_position.x() + offset_x
            new_position_y = current_position.y() + offset_y
            disk.setPos(QPointF(new_position_x, new_position_y))


class MyView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 250, 250)
        self.group = MovableGroup()
        self.scene.addItem(self.group)


if __name__ == '__main__':
    app = QApplication([])
    f = MyView()
    f.show()
    sys.exit(app.exec_())
