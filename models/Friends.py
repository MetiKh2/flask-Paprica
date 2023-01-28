from db_manager import db
from sqlalchemy import Integer,String,DateTime,Boolean,Column,Text,ForeignKey
from datetime import datetime
from models.User import Users
class Friends(db.Model):
    id = Column(Integer(), primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    friend_id = Column(ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(),default=datetime.now())
    def get_friend(self):
        user = db.session.query(Users).filter(Users.id == self.friend_id).first()
        return user