import re
import sys
from typing import List, Any, Dict, Optional
from PySide2 import QtWidgets as qtw, QtCore as qtc, QtGui as qtg


class TreeViewPractice(qtw.QTreeView):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setModel(SearchModel())

        data = [
            {
                "name": "character",
                "type": "assetType",
                "decendent": [
                        {
                            "name": "darthPlaguies",
                            "type": "char",
                        },
                        {
                            "name": "darthSidious",
                            "type": "char",
                        }
                    ],
            },
            {
                "name": "props",
                "type": "assetType",
                "decendent": [
                    {
                        "name": "darthPlaguiesLightSaber",
                        "type": "props"
                    },
                    {
                        "name": "darthSidiousLightSaber",
                        "type": "props"
                    },
                ],
            },
            {
                "name": "sets",
                "type": "assetType",
                "decendent": [
                    {
                        "name": "cave001",
                        "type": "set"
                    },
                    {
                        "name": "caveSpaceShip",
                        "type": "set"
                    },
                ],
            },
        ]

        # self.model().sourceModel()
        self.feedModel(data)
        self.model().setRecursiveFilteringEnabled(True)
        self.model().setFilterCaseSensitivity(qtc.Qt.CaseInsensitive)

    def feedModel(
            self,
            data: List[Dict[str, Any]],
            parent: Optional[qtg.QStandardItem] = None
            ) -> None:

        self.model().sourceModel().setHorizontalHeaderLabels(['name', 'type'])
        parent = parent or self.model().sourceModel().invisibleRootItem()

        for content in data:
            row = parent.rowCount()
            items = []

            for column, dt in enumerate(['name', 'type']):
                item = qtg.QStandardItem(content.get(dt, 'N/A'))
                parent.setChild(row, column, item)
                items.append(item)

            if childs := content.get("decendent"):
                self.feedModel(childs, items[0])


class SearchModel(qtc.QSortFilterProxyModel):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setSourceModel(StandardModel())
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


class StandardModel(qtg.QStandardItemModel):
    ...


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
    wdg = MainWidget()
    wdg.show()

    app.exec_()
