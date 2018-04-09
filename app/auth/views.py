from flask import render_template, redirect, request, url_for, flash, ab
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm
from app import db


# 每次请求前运行，更新已登录用户的访问时间
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


# 登录路由
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # 提交表格，为post方法，验证用户登录信息
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # 把用户标记为已登录，并根据用户选择是否设置cookie
            login_user(user, form.remember_me.data)
            # 跳转到之前访问页面或者首页
            next = request.args.get('next')
            if next is None or not next.startwith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('用户名或密码错误')
    # get方法不满足if条件，渲染登录模板
    return render_template('auth/login.html', form=form)


# 登出路由
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))


# 注册路由
@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        flash('注册成功')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)