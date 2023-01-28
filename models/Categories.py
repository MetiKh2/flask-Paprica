from db_manager import db
from sqlalchemy import Integer,String,DateTime,Boolean,Column,Text,ForeignKey
from datetime import datetime
from models.User import Users
class Categories(db.Model):
    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    image = Column(Text(),nullable=True)
    is_block = Column(Boolean(),nullable=True,default=False)
    created_at = Column(DateTime(),default=datetime.now())