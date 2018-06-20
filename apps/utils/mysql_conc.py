# -*- coding:utf-8 -*-


def get_email_account(user, password):
    """获取邮箱账号, 密码"""
    import pymysql
    connection = pymysql.connect(
        host='127.0.0.1',
        user=user,
        password=password,
        database='sys',
        port=3306,
        charset='utf8'
    )
    cursor = connection.cursor()
    cursor.execute('select user, passwd from myaccount where situation="新浪邮箱"')
    res = cursor.fetchone()
    cursor.close()
    return res[0], res[1]