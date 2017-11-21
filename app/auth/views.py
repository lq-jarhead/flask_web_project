# -*- coding: cp936 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm



@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login(): 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))



#注册新用户发送验证邮件
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,"Confirm Your Account",
                  "auth/email/confirm",user=user,token=token)
        flash("A comfirmation email has been sen t to your email,\
Chect it for comfirme your account!")
        return redirect(url_for("main.index"))
        #flash('You can now login.')
        #return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

#点击验证邮件链接
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed: #confirmed是模型的列，confirm是模型中的方法
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

#对于未验证，或者验证失败的用户，进行验证
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

#更改用户密码
@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)

#忘记密码后用邮箱来重置密码
@auth.route('/reset', methods=['GET', 'POST'])
#@login_required#此处有错误，揣测意图，使我们在不登录、忘记密码的添加下才需要重置密码！
#若是当前用户不是匿名的话，访问此url的话直接重定向main.index
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))#此行代码为作者原创
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                token = user.generate_reset_token()#生成令牌，但是看model中此函数中的self.id在模型中并没有给他啊，怎么去区分这个呢
                send_email(user.email, 'Reset Your Password',
                           'auth/email/reset_password',
                           user=user, token=token,
                           next=request.args.get('next'))
            flash('An email with instructions to reset your password has been sent to you.')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

        
@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
#@login_required
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))#此行代码为作者原创
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:#这个时候要理解多个if语句的意思，只要if语句条件不成立才执行后面语句，若成立则结束
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been reseted.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)




@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)#
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token): #此处的change_email方法是model中
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))

