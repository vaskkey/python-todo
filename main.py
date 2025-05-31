import sys
from gui.app import init_app
from db.json_db import JsonDb

def main():
    db = JsonDb();
    sys.exit(init_app(db))

if __name__ == '__main__':
    main()

