class BaseRepository:
    def init(self, db_session):
        self.db = db_session

    def add(self, entity):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity