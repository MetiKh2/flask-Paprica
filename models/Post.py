from db_manager import db
from sqlalchemy import Integer,String,DateTime,Boolean,Column,Text,ForeignKey
from datetime import datetime
from models.User import Users
from models.Categories import Categories
class Posts(db.Model):
    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    category_id = Column(ForeignKey('categories.id'), nullable=True,default=0)
    views = Column(Integer(),nullable=True)
    likes = Column(Integer(),nullable=True)
    image = Column(Text(),nullable=True)
    raw_material = Column(Text(),nullable=True)
    prepare = Column(Text(),nullable=True)
    is_block = Column(Boolean(),nullable=True,default=False)
    created_at = Column(DateTime(),default=datetime.now())
    def get_user(self):
        user = db.session.query(Users).filter(Users.id == self.user_id).first()
        return user.username
    def get_category(self):
        category = db.session.query(Categories).filter(Categories.id == self.category_id).first()
        return category.title