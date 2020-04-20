from .db.connect import Session


def get_mysql():
    try:
        db = Session()
        yield db
    finally:
        db.close()