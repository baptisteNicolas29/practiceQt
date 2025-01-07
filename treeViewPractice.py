import re
import sys
from typing import List, Any, Dict, Optional
from PySide2 import QtWidgets as qtw, QtCore as qtc, QtGui as qtg


# view
class TreeViewPractice(qtw.QTreeView):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setModel(SearchModel())

        # self.model().sourceModel()
        self.feedModel(data)
        self.model().setRecursiveFilteringEnabled(True)
        self.model().setFilterCaseSensitivity(qtc.Qt.CaseInsensitive)

        self.setItemDelegateForColumn(2, ItemDelegate())
        self.setEditTriggers(qtw.QAbstractItemView.SelectedClicked)
        # self.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)

    def feedModel(
            self,
            data: List[Dict[str, Any]],
            parent: Optional[qtg.QStandardItem] = None
            ) -> None:

        self.model().sourceModel().setHorizontalHeaderLabels(['name', 'type', 'assigned'])
        parent = parent or self.model().sourceModel().invisibleRootItem()

        for content in data:
            row = parent.rowCount()
            items = []

            for column in range(self.model().sourceModel().columnCount()):

                dt = self.model().headerData(column, qtc.Qt.Horizontal, qtc.Qt.DisplayRole)

                data = content.get(dt)

                if isinstance(data, str):
                    item = Item(data)

                elif isinstance(data, list):
                    item = Item(data[0])
                    item.setData(data, qtc.Qt.UserRole)

                else:
                    item = Item()

                parent.setChild(row, column, item)
                items.append(item)

            if childs := content.get("decendent"):
                self.feedModel(childs, items[0])


# item delegate (to manage widgets)
class ItemDelegate(qtw.QItemDelegate):

    def createEditor(
            self,
            parent: qtw.QWidget,
            option: qtw.QStyleOptionViewItem,
            index: qtc.QModelIndex
            ) -> qtw.QWidget:

        if index.data(qtc.Qt.UserRole):
            return qtw.QComboBox(parent)

        else:
            return super().createEditor(parent, option, index)

    def setEditorData(
            self,
            editor: qtw.QWidget,
            index: qtc.QModelIndex
            ) -> None:

        if not isinstance(editor, qtw.QComboBox):
            return super().setEditorData(editor, index)

        data = index.data(qtc.Qt.UserRole)
        editor.addItems(data)
        value = index.data()

        if value is not None:
            editor.setCurrentText(value)

        else:
            editor.setCurrentIndex(0)

        editor.showPopup()

    def setModelData(
            self,
            editor: qtw.QWidget,
            model: qtc.QAbstractItemModel,
            index: qtc.QModelIndex
            ) -> None:

        if not isinstance(editor, qtw.QComboBox):
            return super().setModelData(editor, model, index)

        model.setData(index, editor.currentText())


# proxy model
class SearchModel(qtc.QSortFilterProxyModel):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setSourceModel(ItemModel())
        # self.setRecursiveFilteringEnabled(True)

    def setFilterByColumn(self, regex: str, column: int):
        self.filters[column] = regex
        self.invalidateFilter()

    def filterAcceptsRow(self, row, parent):
        match = True
        model = self.sourceModel()

        for column in range(model.columnCount()):
            display_data = model.index(row, column, parent).data(qtc.Qt.DisplayRole)
            match = self.filterRegularExpression().match(display_data).hasMatch()

            if match:
                return True

        return False


# item model
class ItemModel(qtg.QStandardItemModel):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


# item
class Item(qtg.QStandardItem):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class MainWidget(qtw.QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._search = qtw.QLineEdit()
        self._tree = TreeViewPractice()

        self.setLayout(qtw.QVBoxLayout())
        self.layout().setContentsMargins(4, 4, 4, 4)
        self.layout().setSpacing(2)
        self.layout().addWidget(self._search)
        self.layout().addWidget(self._tree)

        self._search.textChanged.connect(
                self._tree.model().setFilterRegularExpression
                )


if __name__ == '__main__':

    app = qtw.QApplication(sys.argv)

    data = [
        {
            "name": "character",
            "type": "assetType",
            "decendent": [
                {
                    "name": "darthPlaguies",
                    "type": "char",
                    "assigned": ['bni', 'lpa', 'msh'],
                },
                {
                    "name": "darthSidious",
                    "type": "char",
                    "assigned": ['bni', 'lpa', 'msh'],
                },
                {
                    "name": "excavationRobot",
                    "type": "char",
                    "assigned": ['bni', 'lpa', 'msh'],
                },
            ],
        },
        {
            "name": "props",
            "type": "assetType",
            "decendent": [
                {
                    "name": "darthPlaguiesLightSaber",
                    "type": "props",
                    "assigned": ['bni', 'lpa', 'msh'],
                },
                {
                    "name": "darthSidiousLightSaber",
                    "type": "props",
                    "assigned": ['bni', 'lpa', 'msh'],
                },
                {
                    "name": "spaceShip",
                    "type": "props",
                    "assigned": ['bni', 'lpa', 'msh'],
                },
                {
                    "name": "drill",
                    "type": "props",
                    "assigned": ['bni', 'lpa', 'msh'],
                },
            ],
        },
        {
            "name": "sets",
            "type": "assetType",
            "decendent": [
                {
                    "name": "cave001",
                    "type": "set",
                    "assigned": ['bni', 'lpa', 'msh'],
                },
                {
                    "name": "caveSpaceShip",
                    "type": "set",
                    "assigned": ['bni', 'lpa', 'msh'],
                },
            ],
        },
    ]

    wdg = MainWidget()
    wdg.show()

    app.exec_()
