# -*- coding: UTF-8 -*-
# author:xiaohuihui
# time : 2024/7/3 19:18
# file: forms.py
# software: PyCharm
from wtforms import Form, StringField, TextAreaField, PasswordField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf import FlaskForm
from mysql_util import MysqlUtil


# 登录的表单
class LoginForm(FlaskForm):
    username = StringField(
        ' ',
        validators=[
            DataRequired(message='请输入用户名'),
            Length(min=2,max=30,message='长度在2-30个字符之间')
        ]
    )

    password = PasswordField(
        ' ',
        validators=[
            DataRequired(message='请输入密码'),
            Length(min=6, max=25, message='长度是在 6-25个字符之间')
        ]

    )
    def validate_username(self,field):
        sql = "SELECT * FROM sys_user  WHERE user_name = '%s'" % (field.data) # 根据用户名查找user表中记录
        db = MysqlUtil() # 实例化数据库操作类
        result = db.fetchone(sql) # 获取一条记录
        print(result)
        if not result:
            raise ValidationError("用户名不存在")

# 表单的模版

class ArticleForm(Form):
    title = StringField(
        '标题',
        vlaidators=[
            DataRequired(message='长度在2-30个字符之间'),
            Length(min=2, max=30)
        ]
    )


    content = TextAreaField(
        '内容',
        validators=[
            DataRequired(message='长度不少于5个字符'),
            Length(min=5)
        ]
    )



# 注册的表单模版
class AddUserForm(FlaskForm):
    # 用户名
    username = StringField(
        ' ',
        validators=[
            DataRequired(message='请输入用户名'),
            Length(min=2, max=30, message='长度在2-30个字符之间')
        ]
    )
    # 返回的名称
    realname = StringField(
        ' ',
        validators=[
            DataRequired(message='请输入名昵'),
            Length(min=2, max=30, message='长度在2-30个字符之间')
        ]
    )
    # 邮箱
    email = StringField(
        ' ',
        validators=[
            DataRequired(message='请输入邮箱'),
            Length(min=2, max=30, message='长度在2-30个字符之间')
        ]
    )
    # 密码
    password = PasswordField(
        ' ',
        validators=[
            DataRequired(message='请输入密码'),
            Length(min=6, max=25, message='长度是在 6-25个字符之间')
        ]

    )
    # 确认密码
    is_password = PasswordField(
        ' ',
        validators=[
            DataRequired(message='请输入密码'),
            Length(min=6, max=25, message='长度是在 6-25个字符之间')
        ]

    )
    # 手机号
    phonenumber = StringField(
        ' ',
        validators=[
            DataRequired(message='请输入你的手机号'),
            Length(min=11, max=30, message='长度在11-30个字符之间')
        ]
    )
    # 头像地址输入
    avatar = StringField(
        ' ',
        validators=[
            DataRequired(message='请输入邮箱'),
            Length(min=1, max=255, message='长度在1-255个字符之间')
        ]
    )
    # 单选 一组单选按钮
    radio = RadioField('Label', choices=[('1', '管理员'), ('0', '普通人')],
                             validators=[DataRequired()])

    remark = StringField(
        ' ',
        validators=[
            DataRequired(message='请输入备注'),
            Length(min=2, max=30, message='长度在2-30个字符之间')
        ]
    )

