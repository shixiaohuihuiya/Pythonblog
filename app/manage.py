# -*- coding: UTF-8 -*-
# author:xiaohuihui
# time : 2024/7/2 15:12
# file: manage.py
# software: PyCharm
import os
from datetime import datetime
from functools import wraps
import base64
# 作为启动的端口

from flask import Flask, render_template, session, flash, redirect, url_for, request

from forms import LoginForm, ArticleForm
from  mysql_util import MysqlUtil
app = Flask(__name__)
app.config['SECRET_KEY'] = "han"
# 如果用户已经登录
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:     # 判断用户是否登录
            return f(*args, **kwargs)  # 如果登录，继续执行被装饰的函数
        else:                          # 如果没有登录，提示无权访问
            flash('无权访问，请先登录', 'danger')
            return redirect(url_for('login'))
    return wrap

# 判断用户的权限 普通人 还是管理员
def is_permission():
    """
       1.首先 判断用户是不是管理员
       2.根据管理员决定显示多少的内容
       3.管理员就显示 所有的信息 如果是普通用户的话那么就只显示 当前自己的
       :return:
       """
    # 判断用户的身份
    username = session['username']
    res = MysqlUtil().fetchone("select * from sys_user  where real_name = '%s'" % (username))
    permissionId = res['permission_id']
    # 查询该用户是否为管理
    permission = MysqlUtil().fetchone("select * from sys_permission   where id = %s" % (permissionId))
    if permission['permission_name'] == "管理员":
        return True
    else:
        return False



def pl():
    if is_permission():
        db = MysqlUtil()
        sql = "select bar.*, from blog_article_remack bar join sys_user su on su.id = bar.user_id join blog_article ba on ba.id = bar.blog_article_id"
        pls = db.fetchall(sql)
        return pls
    else:
        db = MysqlUtil()
        id = session['id']
        sql = f"select bar.*, from blog_article_remack bar join sys_user su on su.id = bar.user_id join blog_article ba on ba.id = bar.blog_article_id where user_id = {id}"
        pls = db.fetchall(sql)
        return pls

def ryxq():
    if is_permission():
        db = MysqlUtil()
        sql = "SELECT * FROM sys_user"
        rysqs = db.fetchall(sql)
        return rysqs
    else:
        db = MysqlUtil()
        id = session['id']
        sql = f"select * from sys_user where id = {id}"
        rysqs = db.fetchall(sql)
        return rysqs


def dzxq():
    """
    1.首先 判断用户是不是管理员
    2.根据管理员决定显示多少的内容
    3.管理员就显示 所有的信息 如果是普通用户的话那么就只显示 当前自己的
    """
    # 判断用户的身份
    if is_permission():
        db = MysqlUtil()
        sql = f"""SELECT bad.id,su.real_name as realname , ba.article_name as title , bad.createtime ,bad.sate
                FROM blog_article_dz bad JOIN sys_user su ON su.id = bad.user_id JOIN blog_article ba ON ba.id = bad.article_id"""
        dzxq = db.fetchall(sql)
        print(dzxq)
        return dzxq
    else:
        db = MysqlUtil()
        id = session['id']
        sql = f"""SELECT su.real_name as realname , ba.article_name as title , bad.createtime ,bad.sate
FROM blog_article_dz bad JOIN sys_user su ON su.id = bad.user_id JOIN blog_article ba ON ba.id = bad.article_id WHERE bad.user_id = {id}"""
        dzxq = db.fetchall(sql)
        return dzxq

# 博客首页 查询所有的博客信息
@app.route('/')
def index():
    db = MysqlUtil()
    count = 5
    page = request.args.get('page')  # 获取当前页码
    if page is None:
        page = 1
    sql = f'SELECT  ba.* ,su.real_name AS author FROM blog_article ba  left JOIN sys_user su ON su.id = ba.user_id where article_state = 2 group by update_time DESC LIMIT {(int(page)-1)*count},{count}'
    articles = db.fetchall(sql)

    # 遍历数据  遍历所有的文章数据
    return render_template('index.html',articles=articles,page=int(page))

# 分类
@app.route('/fl')
def fl():
    db = MysqlUtil()
    sql = "select * from blog_article_type"
    fl = db.fetchall(sql)
    return render_template('fl.html',fls = fl) # 渲染模板

# 具体分类的文章
@app.route('/flArticle/<string:id>')
# 通过分类的id 进行查询的所哟的代码
def flArticle(id):
    db = MysqlUtil()
    count = 5
    page = request.args.get('page')  # 获取当前页码
    if page is None:
        page = 1
    sql = f'''SELECT ba.*,su.real_name AS author , bat.type_name AS typename FROM blog_article ba JOIN sys_user su ON su.id = ba.user_id JOIN blog_article_type bat ON bat.id = ba.article_type
                WHERE ba.article_type = {id}
                    GROUP BY ba.update_time
                    DESC LIMIT {(int(page)-1)*count},{count} '''
    articles = db.fetchall(sql)
    print("分类之后查询到的数据是：",articles)
    return render_template('index2.html',articles = articles,page=int(page))

# 控制台
@app.route('/kzt')
@is_logged_in
def kzt():
    if is_permission():
        db = MysqlUtil()
        sql = "select ba.*,su.real_name as author  from blog_article ba left join sys_user su on su.id = ba.user_id"
        realUserArticle = db.fetchall(sql)
        return render_template('kzt.html', realUserArticle=realUserArticle, dzxq=dzxq())
    else:
        id = session['id']
        sql = "select ba.*,su.real_name as author  from blog_article ba left join sys_user su on su.id = ba.user_id where ba.user_id = '%s'"%(id)
        db = MysqlUtil()
        real_user_article = db.fetchall(sql)
        return render_template('kzt.html', realUserArticle=real_user_article, dzxq=dzxq(),pls=pl(),ryxqs = ryxq())  # 渲染模板

# 登录
@app.route('/login',methods=['GET','POST'])
def login():
    if "login_in" in session:
        return redirect(url_for("kzt"))
    form = LoginForm(request.form)
    # 验证提交的事件  如果表单提交之后 判断为 True
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        # message = f"用户名：{username}<br>密码：{password}"
        print(f"用户名：{username}\n密码：{password}")
        db = MysqlUtil()
        sql = "SELECT * FROM sys_user  WHERE user_name = '%s'" % (username)
        print(sql)
        result1 = db.fetchone(sql)
        print(result1)
        res_password = result1['password']
        real_name = result1['real_name']

        print(res_password)
        # 这里采用的是base64加密的方式来实现 密码加密的操作
        bs64Password = base64.b64encode(password.encode("utf-8")).decode("utf-8")
        print(bs64Password)
        print(bs64Password==res_password)
        if bs64Password == res_password:
            session['logged_in'] = True
            # 返回的是 返回的名称
            session['username'] = real_name
            session['id'] = result1['id']

            flash('登录成功！', 'success')  # 闪存信息
            return redirect(url_for("kzt"))
    return render_template('login.html',form=form)

# 退出的端口
@app.route('/loginout',methods=['GET','POST'])
def loginout():
    session.clear()
    flash('您已成功退出', 'success')  # 闪存信息
    return redirect(url_for('index'))  # 跳转到登录页面


# 文章的详情
@app.route("/article/<string:id>/",methods=['GET',"POST"])
def article(id):
    db = MysqlUtil()
    sql = f"SELECT  ba.* ,su.real_name AS author FROM blog_article ba  JOIN sys_user su ON su.id = ba.user_id where ba.id = {id}"
    article = db.fetchone(sql)
    readNum = article['article_read_count']
    id = article['id']
    update_readNum = readNum + 1
    # 跟新阅读的数量
    db1 = MysqlUtil()
    sql1 = f"update blog_article set article_read_count = {update_readNum} where id = {id}"
    db1.update(sql1)
    addArticlePl(id)
    return render_template('article.html',article=article,remacks=selectPl(id))



# 删除评论
@app.route("/del_reamck/<string:id>")
# 这里是模拟删除，不是真的删除，以方便恢复数据
def delRemack(id):
    db = MysqlUtil()
    sql = f"update blog_article_remack set remack_sate = 1 where id = {id}"
    db.update(sql)
    return "删除成功"






# 删除文章
@app.route("/del_article/<string:id>",methods = ['POST','GET'])
def delArticle(id):
    db = MysqlUtil()
    # 这里应该使用的是传递的数据是 修改的数据 而不是删除的数据 所以 只需要对文章详情的状态进行修改就ok了 修改成需要的状态代码 0就是不展示   1 就是禁用这种
    # 如果将文章的数据删除的话那么就是永久性的删除了 这样的话 后面想进行恢复的时候 也没有相关的数据 也没有相关的
    sql = f"UPDATE blog_article set article_state = 2 WHERE id = {id}"
    db.delete(sql)
    print("修改状态成功")
    return redirect(url_for("kzt"))

# 添加文章
@app.route("/add_article",methods=['POST',"GET"])
@is_logged_in
def addArticle():
    # 这里选择的是获取到表单上面的数据
    form = ArticleForm()
    return render_template("addArticle.html",form = form)

# 这里是将点赞的状态 改成删除的状态
@app.route("/del_dzxq/<string:id>",methods=['POST','GET'])
@is_logged_in
def delDzxq(id):
    db = MysqlUtil()
    sql = f"update blog_artilce_dz set del_state = 1 where id = {id}"
    db.update(sql)
    return redirect(url_for("kzt"))

# 人员详细
@app.route("/selectUserByUser")
@is_logged_in # 做的登录拦截
def selectUserByUser():
    if is_permission(): # 判断登录 是否为管理员
        db = MysqlUtil()
        sql = f"select * from  sys_user"
        userall = db.fetchall(sql)
        return render_template('kzt.html',userall = userall)
    else:
        db = MysqlUtil()
        id = session['id']
        sql = f"select * from  sys_user where id = {id}"
        userall = db.fetchone(sql)
        return render_template('kzt.html', userall=userall)

# 修改的用户信息
@app.route("/updateUser/<string:id>",methods=['POST','GET'])
@is_logged_in
def updateUser(id):
    '''
    首先是查询出现信息,进行显示修改数据
    再次提交进行修改数据
    :return:
    '''
    db = MysqlUtil()
    sql = f"""
        select * from sys_user where id = {id}
    """
    # 首先是返回数据之后，再去找
    result = db.fetchone(sql)

    # 获取所有的值
    if request.method == "POST":
        if is_permission():
            # username = request.form['username']
            realname = request.form['realname']
            email = request.form['email']
            avatar = request.form['avatar']
            phonenumber = request.form['phonenumber']
            permission_id = request.form['permission_id']
            password = request.form['password']
            newtimenow = datetime.now()
            db1 = MysqlUtil()
            sql1 = """update sys_user set 
                    real_name = '%s',
                    email = '%s',
                    phonenumber = '%s',
                    avatar = '%s',
                    permission_id = '%s',
                    password = '%s',
                    remark = '%s'"""%(realname,email,phonenumber,avatar,permission_id,password,newtimenow)
            db1.update(sql1)
            return url_for("kzt")
    return render_template("kzt.html",result=result)



# 新增用户信息
@app.route("/addUser",methods=['POST','GET'])
@is_logged_in # 判断是否登录
def addUser():
    '''
    1. 首先是判断是不是管理员
    2. 就可以进行进行数据的增加 如果不是的情况下，那么就不显示 用户新增的按钮
    3. 获取到新增的数据 添加到数据库中
    '''
    # 首先对username 进行检验 检验 是否有重复的 如果有重复的 不进行 新增的操作
    if request.method == "POST":
        # 账号
        username = request.form['username']
        #返回名称 （昵称）
        realname = request.form['real_name']
        #密码
        password =  base64.b64encode(request.form['password'].encode("utf-8")).decode("utf-8")
        #确认密码
        is_password = request.form['is_password']
        # 权限
        option = request.form['option']
        #手机号
        phonenumber = request.form['phonenumber']
        #邮箱
        email = request.form['email']

        db1 = MysqlUtil()
        sql = "select * from sys_user where user_name = '%s'"%(username)
        newdatetime = datetime.now().__str__()
    # 判断用户名是否重复
        res_username = db1.fetchone(sql)
        if res_username == None:
            # 如果查询的是空的时候才可以进行插入
            db2 = MysqlUtil()
            sql2 = """
                insert into sys_user(
                    user_name,
                    real_name,
                    email ,
                    phonenumber,
                    avatar,
                    permission_id,
                    password,
                    remark,
                    del_state 
                ) values (
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    'https://img0.baidu.com/it/u=491725098,2182699032&fm=253&fmt=auto&app=138&f=JPEG?w=499&h=332',
                    %s,
                    '%s',
                    '%s',
                    0
                );
            
            """%(username,realname,email,phonenumber,option,password,newdatetime)
            print(sql2)
            db2.insert(sql2)
            return "注册成功！"

    return render_template('addUser.html')


# 修改 用户信息的状态 也不是真的删除 也是只有管理员才可以进行修改人员信息的状态
@app.route("/del_user/<string:id>")
def delUser():
    # 通过用户的id进行删除的操作
    db = MysqlUtil()
    sql = f"update sys_user set del_state = 1"
    # 做一个删除的记录 但是数据不是真的删除这些代码
    db.update(sql)

@is_logged_in
def addArticlePl(id):
    if request.method == 'POST':
        pl = request.form['pl']
        print(pl)
        user_id = session['id']
        print("这是user_id:",user_id)
        print(f"pl的内容是：{pl}")
        if pl == " ":
            return "评论数据为空！"
        else:
            article_id = id
            newdatetime = datetime.now()
            db = MysqlUtil()
            sql = """
                            insert into blog_article_remack(
                                blog_article_id,
                                user_id,
                                create_date,
                                article_remack_content,
                                remack_sate
                            ) values (
                                %s,
                                %s,
                                '%s',
                                '%s',
                                0

                            )
                        """ % (article_id, user_id, newdatetime, pl)
            db.insert(sql)
            return redirect(f"/article/{id}/")

# 查询评论
def selectPl(id):
    db = MysqlUtil()
    sql = f"SELECT bar.*,su.real_name AS author , ba.article_name AS title FROM blog_article_remack bar JOIN sys_user su ON su.id = bar.user_id JOIN blog_article ba ON ba.id = bar.blog_article_id WHERE blog_article_id = {id} AND bar.article_remack_content IS NOT NULL"
    remacks = db.fetchall(sql)
    return remacks
# 404 页面找不到
@app.errorhandler(404)
def page_not_found(error):
    """
    404
    """
    return render_template("404.html"), 404






if __name__ == '__main__':
    # 获取当前的工作目录
    print(os.getcwd())
    # 运行当前flask 程序
    app.run(debug=True,port=6789,host='0.0.0.0')