from sqlalchemy import create_engine, Column, Integer, String
from data.ORMSetup import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    #branch_id
    password = Column(String) #needs to be encoded
    #role needs to be calidated from a pool of roles
    

