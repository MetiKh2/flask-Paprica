from db_manager import db
from sqlalchemy import Integer,String,DateTime,Boolean,Column,Text,ForeignKey
from datetime import datetime
from models.Post import Posts
from models.User import Users
class Comments(db.Model):
    id = Column(Integer(), primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    post_id = Column(ForeignKey('posts.id'), nullable=False)
    text = Column(Text, nullable=False)
    is_block = Column(Boolean, nullable=True,default=False)
    created_at = Column(DateTime(),default=datetime.now())
    def get_post(self):
        post = db.session.query(Posts).filter(Posts.id == self.post_id).first()
        return post
    def get_post_title(self):
        post = db.session.query(Posts).filter(Posts.id == self.post_id).first()
        return post.title
    def get_username(self):
        user = db.session.query(Users).filter(Users.id == self.user_id).first()
        return user.username
    def get_userimage(self):
        user = db.session.query(Users).filter(Users.id == self.user_id).first()
        return user.image