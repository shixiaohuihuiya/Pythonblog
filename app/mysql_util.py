# -*- coding: UTF-8 -*-
# author:xiaohuihui
# time : 2024/7/3 14:16
# file: mysql_util.py
# software: PyCharm

# 设置数据库的操作  mysql

import pymysql # python MySQL连接
import sys    # 系统模块
import traceback # 追踪错误

class MysqlUtil():
    def __init__(self):
        '''
        初始化方法，连接数据库
        '''
        host='localhost'
        user='root'
        password='root'
        database = 'blog'
        self.db = pymysql.connect(host=host, user=user, password=password, db=database)  # 建立连接
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)  # 设置游标，并将游标设置为字典类型

    def insert(self,sql):
        """
        插入数据
        :param sql: 插入数据的sql语句
        """
        try:
            #执行sql语句
            self.cursor.execute(sql)
            # 提交数据
            self.db.commit()
        except Exception:
            print("发生异常",Exception)
            # self.db.rollback()
        finally:
            self.db.close()

    """
    查询一条记录
    """
    def fetchone(self,sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result
        except Exception:
            # 输出异常方式
            traceback.print_exc()
            # 事务进行回滚的状态
            self.db.rollback()
        finally:
            # 关闭数据库
            self.db.close()

    """
    查询多条数据
    """
    def fetchall(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except:
            info = sys.exc_info()
            print(info[0], ":", info[1])
        finally:
            self.db.close()


    def delete(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception:
            f = open("\log.txt", 'a')
            traceback.print_exc(file=f)
            f.flush()
            f.close()
            # 如果发生异常，则回滚
            self.db.rollback()
        finally:
            # 最终关闭数据库连接
            self.db.close()

    def update(self, sql):
        '''
            更新结果集
        '''
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            self.db.commit()
        except:
            # 如果发生异常，则回滚
            self.db.rollback()
        finally:
            # 最终关闭数据库连接
            self.db.close()

