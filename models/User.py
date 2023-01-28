from db_manager import db
from sqlalchemy import Integer,String,DateTime,Boolean,Column,Text
from datetime import datetime

class Users(db.Model):
    id = Column(Integer(), primary_key=True)
    public_id = Column(String)
    username = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    password = Column(String(),nullable=False)
    image = Column(Text(),nullable=True)
    is_admin = Column(Boolean(),nullable=True,default=False)
    is_block = Column(Boolean(),nullable=True,default=False)
    is_confirmed = Column(Boolean(),nullable=True,default=False)
    created_at = Column(DateTime(),default=datetime.now())