from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


# 工厂函数，接收配置名作为参数
def create_app(config_name):
    app = Flask(__name__)
    # 配置导入程序
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化扩展
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # 通过注册蓝本附加路由和错误处理页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


