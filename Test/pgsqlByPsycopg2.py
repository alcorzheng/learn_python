# /usr/bin/env python
# -*- coding:utf-8 -*-

import psycopg2

# 连接数据库
conn = psycopg2.connect("dbname=study_python user=study password=study host=127.0.0.1 port=5432")

# 创建cursor以访问数据库
cur = conn.cursor()

# 创建表
cur.execute(
        'CREATE TABLE Employee ('
        'name    varchar(80),'
        'address varchar(80),'
        'age     int,'
        'date    date'
        ')'
    )

# 插入数据
cur.execute("INSERT INTO Employee VALUES('Gopher', 'China Beijing', 100, '2017-05-27')")

# 查询数据
cur.execute("SELECT * FROM Employee")
rows = cur.fetchall()
for row in rows:
    print('name=' + str(row[0]) + ' address=' + str(row[1]) +  ' age=' + str(row[2]) + ' date=' + str(row[3]))

# 更新数据
cur.execute("UPDATE Employee SET age=12 WHERE name='Gopher'")

# 删除数据
cur.execute("DELETE FROM Employee WHERE name='Gopher'")

# 提交事务
conn.commit()

# 关闭连接
conn.close()