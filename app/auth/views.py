from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import auth
from ..models import User
from .forms import LoginForm


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
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    # get方法不满足if条件，渲染登录模板
    return render_template('auth/login.html', form=form)


# 登出路由
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))
