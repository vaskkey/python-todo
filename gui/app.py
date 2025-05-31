from PySide6 import QtWidgets
from db.db import AbstractDb
from gui.window import Window

def init_app(db: AbstractDb) -> int:
    app = QtWidgets.QApplication([])
    window = Window(db)
    window.resize(800, 600)
    window.show()

    return app.exec()
