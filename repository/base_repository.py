from sqlalchemy import select

class BaseRepository:
    def __init__(self, db, model):
        self.db = db
        self.model = model

    def get_by_id(self, obj_id):
        return self.db.query(self.model).get(obj_id)

    def list_all(self):
        stmt = select(self.model)
        return self.db.execute(stmt).scalars().all()

    def create(self, obj):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj):
        self.db.delete(obj)
        self.db.commit()

    def update(self, obj, updates: dict):
        for key, value in updates.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj