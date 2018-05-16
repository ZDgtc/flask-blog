from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm
from app import db
from ..email import send_email


# 每次请求前运行，更新已登录用户的访问时间
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        # 过滤未确认的账户
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
        # 确认token需要用到id，不能延后提交
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认您的账户', 'auth/email/confirm', user=user, token=token)
        flash('一封确认邮件已发到您的邮箱。')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


# 确认账户
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您已成功确认账户！')
    else:
        flash('确认链接非法或已过期。')
    return redirect(url_for('main.index'))


# 要求确认账户
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


# 再次发送确认邮件
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认您的账户', 'auth/email/confirm', user=current_user, token=token)
    flash('一封新的确认邮件已发到您的邮箱。')
    return redirect(url_for('main.index'))
