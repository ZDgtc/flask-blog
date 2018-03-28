from . import db
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # 只读函数，返回错误，不可读取原密码
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # 只写函数，用于设置密码，自动转换为散列值
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 将密码作为参数传入，与数据库中的散列值做对比
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 接收unicode字符串表示的用户标识符，返回用户对象或者None
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __repr__(self):
        return '<User %r>' % self.username
