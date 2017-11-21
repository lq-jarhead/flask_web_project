# -*- coding: cp936 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo

from wtforms import ValidationError
from ..models import User

#登录
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
    
#注册
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Required(),Length(1, 64),
                                             Email()])
    username = StringField("Username",validators=[
        Required(),Length(1,64),Regexp("^[A-Za-z][A-Za-z0-9_.]*$",0,
                                       "username must have only letters, "
                                       "numbers,dots or underscores")])
    password = PasswordField('Password', validators=[Required(),EqualTo("password2", message="Passwords must match")])
    password2=PasswordField("Confirm password",validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Register')


    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")


    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use. ")

#单纯的更改密码
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')


#忘记密码情况下，用 邮箱找回密码分两步
#第一步是发送邮件
class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')

#第二部，根据邮箱链接到修改密码的url，进行密码重置
class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),Email()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field): #新增的一个表单验证函数，确定email是用户的
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')

class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
