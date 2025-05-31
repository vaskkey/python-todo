from db.db import AbstractDb
from db.json_db import JsonDb

def main():
    db: AbstractDb = JsonDb()
    db.write({'done': False, 'value': "Finish python project"})
    print(db.read(0))
    print(db.read_all())


if __name__ == '__main__':
    main()

