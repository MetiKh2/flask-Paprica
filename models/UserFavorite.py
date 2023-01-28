from db_manager import db
from sqlalchemy import Integer,String,DateTime,Boolean,Column,Text,ForeignKey
from datetime import datetime
from models.Post import Posts
class UserFavorites(db.Model):
    id = Column(Integer(), primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    post_id = Column(ForeignKey('posts.id'), nullable=False)
    created_at = Column(DateTime(),default=datetime.now())
    def get_post(self):
        post = db.session.query(Posts).filter(Posts.id == self.post_id).first()
        return post