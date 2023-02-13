from flask import Flask, request, jsonify, make_response
from sqlalchemy import desc, and_
import os
from db_manager import db
from models import Post, User, Friends, UserFavorite, Categories, Comment
import uuid
import jwt
import datetime
from flask_cors import CORS, cross_origin
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
if app.config['ENV'] == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')
db.init_app(app)
with app.app_context():
    db.create_all()
UPLOAD_DIR = os.path.curdir = 'static/uploads/'
app.secret_key = '1dae11441a1a2acf1cad3eca'


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'a valid token is missing'}),401
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.Users.query.filter_by(
                public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'}),401

        return f(current_user, *args, **kwargs)
    return decorator


@app.route('/api/register', methods=['POST'])
@cross_origin()
def signup_user():
   try:
    data = request.get_json()
    if not data['password']or not data['username']or not data['email']:
        raise ValueError('Values are null')
    hashed_password = generate_password_hash(data['password'], method='sha256')
    print(data['password'])
    new_user = User.Users(public_id=str(uuid.uuid4(
    )), username=data['username'], email=data['email'],image=data['image'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'registered successfully'})
   except Exception as e: 
    return jsonify({
        'message':'registered unsuccessfully'
    },501)


@app.route('/api/login', methods=['POST'])
@cross_origin()
def login_user():
    auth = request.get_json()
    if not auth or not auth['email'] or not auth['password']:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})

    user = User.Users.query.filter(
        and_(User.Users.email == auth['email'], User.Users.is_block == False)).first()
    if check_password_hash(user.password, auth['password']):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(days=10)}, app.config['SECRET_KEY'], "HS256")

        return jsonify({'token': token})

    print('ss')
    return make_response('could not verify',  401, {'Authentication': '"login required"'})


@app.route('/api/tt', methods=['GET'])
# @token_required
def test():
    db.session.add(Friends.Friends(user_id=1, friend_id=2
                                   ))
    db.session.commit()
    return 's'


@app.route('/api/posts', methods=['GET'])
@cross_origin()
def posts():
    order_by = request.args.get('order_by')
    count = int(request.args.get('count'))
    category = int(request.args.get('category')or 0)
    query = str(request.args.get('query')or '')
    if order_by == 'newest':
        posts = db.session.query(Post.Posts).filter(
            and_(Post.Posts.is_block == False,Post.Posts.title.contains(query))).order_by(desc(Post.Posts.created_at)).limit(count).all()
    elif order_by == 'most_view':
        posts = db.session.query(Post.Posts).filter(
           and_(Post.Posts.is_block == False,Post.Posts.title.contains(query))).order_by(desc(Post.Posts.views)).limit(count).all()
    elif order_by == 'most_like':
        posts = db.session.query(Post.Posts).filter(
           and_(Post.Posts.is_block == False,Post.Posts.title.contains(query))).order_by(desc(Post.Posts.likes)).limit(count).all()
    else:
        posts = db.session.query(Post.Posts).filter(
           and_(Post.Posts.is_block == False,Post.Posts.title.contains(query))).limit(count).all()
    if category and category>0:
        posts=filter(lambda post:post.category_id==category,posts)
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'user': post.get_user(),
        'views': post.views,
        'likes': post.get_favorites(),
        'image': post.image,
        'raw_material': post.raw_material,
        'prepare': post.prepare,
        'is_block': post.is_block,
        'created_at': post.created_at,
        'category': post.get_category()if post.category_id else "",
    }for post in posts])


@app.route('/api/add_friend', methods=['POST'])
@cross_origin()
@token_required
def add_friend(current_user):
    data = request.get_json()
    last = db.session.query(Friends.Friends).filter(and_(Friends.Friends.user_id ==
                                                         current_user.id, Friends.Friends.friend_id == int(data['friend_id']))).first()
    if last:
        return ''
    db.session.add(Friends.Friends(user_id=current_user.id,
                   friend_id=int(data['friend_id'])))
    db.session.commit()
    return jsonify({
        'message': 'friend added successfully'
    })


@app.route('/api/friends', methods=['GET'])
@cross_origin()
@token_required
def friends(current_user):
    friendly = db.session.query(Friends.Friends).filter(
        Friends.Friends.user_id == current_user.id).all()
    return jsonify([{
        'user_name': friend.get_friend().username,
        'email': friend.get_friend().email,
        'image': friend.get_friend().image,
    }for friend in friendly])


@app.route('/api/add_favorite', methods=['POST'])
@cross_origin()
@token_required
def add_favorite(current_user):
    data = request.get_json()
    last = db.session.query(UserFavorite.UserFavorites).filter(and_(UserFavorite.UserFavorites.user_id ==
                                                                    current_user.id, UserFavorite.UserFavorites.post_id == int(data['post_id']))).first()
    if last:
        return ''
    db.session.add(UserFavorite.UserFavorites(
        user_id=current_user.id, post_id=int(data['post_id'])))
    db.session.commit()
    return jsonify({
        'message': 'favorite added successfully'
    })
@app.route('/api/remove_favorite', methods=['POST'])
@cross_origin()
@token_required
def remove_favorite(current_user):
    data = request.get_json()
    last = db.session.query(UserFavorite.UserFavorites).filter(and_(UserFavorite.UserFavorites.user_id ==
                                                                    current_user.id, UserFavorite.UserFavorites.post_id == int(data['post_id']))).delete()
    db.session.commit()
    return jsonify({
        'message': 'favorite removed successfully'
    })


@app.route('/api/favorites', methods=['GET'])
@cross_origin()
@token_required
def favorites(current_user):
    try:
        favorites = db.session.query(UserFavorite.UserFavorites).filter(
            UserFavorite.UserFavorites.user_id == current_user.id).all()
        posts = []
        for i in range(len(favorites)):
            posts.append(db.session.query(Post.Posts).filter(
                Post.Posts.id == favorites[i].post_id).first())
        return jsonify([{
            'id': post.id,
            'title': post.title,
            'user': post.get_user(),
            'views': post.views,
            'likes': post.get_favorites(),
            'image': post.image,
            'raw_material': post.raw_material,
            'prepare': post.prepare,
            'is_block': post.is_block,
            'created_at': post.created_at,
            'category': post.get_category()if post.category_id else "",

        }for post in posts])
    except:
        return ''


@app.route('/api/categories', methods=['GET'])
@cross_origin()
def categories():
    categories_list = db.session.query(Categories.Categories).filter(
        Categories.Categories.is_block == False).all()
    return jsonify([{
        'title': category.title,
        'image': category.image,
        'id': category.id,
    }for category in categories_list])


@app.route('/api/profile', methods=['GET'])
@cross_origin()
@token_required
def profile(current_user):
    posts = db.session.query(Post.Posts).filter(
        and_(Post.Posts.is_block == False, Post.Posts.user_id == current_user.id)).all()
    return jsonify({
        'username': current_user.username,
        'image': current_user.image,
        'posts': [{
            'id': post.id,
            'title': post.title,
            'user': post.get_user(),
            'views': post.views,
            'likes': post.get_favorites(),
            'image': post.image,
            'raw_material': post.raw_material,
            'prepare': post.prepare,
            'is_block': post.is_block,
            'created_at': post.created_at,
            'category': post.get_category()if post.category_id else "",
        }for post in posts]})


@app.route('/api/add_comment', methods=['POST'])
@cross_origin()
@token_required
def add_comment(current_user):
    data = request.get_json()
    db.session.add(Comment.Comments(
        user_id=current_user.id, post_id=int(data['post_id']), text=data['text']))
    db.session.commit()
    return jsonify({
        'message': 'comment added successfully'
    })


@app.route('/api/comments/<int:post_id>', methods=['GET'])
@cross_origin()
def comments(post_id):
    comments = db.session.query(Comment.Comments).filter(
        and_(Comment.Comments.is_block == False, Comment.Comments.post_id == post_id)).all()
    return jsonify([{
        'text': comment.text,
        'username': comment.get_username(),
        'image': comment.get_userimage(),
    }for comment in comments])


@app.route('/api/comments/user', methods=['GET'])
@cross_origin()
@token_required
def commentsByUser(current_user):
    comments = db.session.query(Comment.Comments).filter(
        and_(Comment.Comments.is_block == False, Comment.Comments.user_id == current_user.id)).all()
    return jsonify([{
        'text': comment.text,
        'post_title': comment.get_post_title(),
    }for comment in comments])


@app.route('/api/post/<int:post_id>', methods=['GET'])
@cross_origin()
def post(post_id):
    post = db.session.query(Post.Posts).filter(
        and_(Post.Posts.is_block == False, Post.Posts.id == post_id)).first()
    if(post.views):
        post.views=post.views+1
    else:
        post.views=1
    db.session.add(post)
    db.session.commit()
    return jsonify({
        'prepare': post.prepare,
        'raw_material': post.raw_material,
        'title': post.title,
        'image': post.image,
        'id': post.id,
        'likes': post.get_favorites(),
        'views': post.views,
        'category': post.get_category(),
        'user':{
            'username':post.get_user(),
            'image':post.get_user_image(),
        }
    })


@app.route('/api/add_post', methods=['POST'])
@cross_origin()
@token_required
def add_post(current_user):
    data = request.get_json()
    db.session.add(Post.Posts(
        user_id=current_user.id, title=data['title'],image=data['image'], prepare=data['prepare'], raw_material=data['raw_material'], category_id=data['category_id']))
    db.session.commit()
    return jsonify({
        'message': 'post added successfully'
    })



if __name__ == '__main__':
    app.run(debug=True, port=2024)
