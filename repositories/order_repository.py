from models import User


class OrderRepository:
    def __init__(self,db):
        self.db = db

    def get_by_id(self,user_id):
        return self.db.query(User).filter(User.id == user_id).first()
    def list_all(self):
        return self.db.query(User).all()

