import psycopg2

# 建立数据库连接
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="postgrespw",
    database="postgres"
)

# 创建游标对象
cur = conn.cursor()

# 创建自定义数据库
create_database_query = 'CREATE DATABASE artia;'
cur.execute(create_database_query)

# 切换到新创建的数据库
conn.close()
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="postgrespw",
    database="artia"
)
cur = conn.cursor()

# 创建表格
create_table_query = '''
CREATE TABLE IF NOT EXISTS aigc (
    id SERIAL PRIMARY KEY,
    content TEXT,
    imageUrl TEXT,
    imageUrls TEXT[],
    buttons TEXT[],
    createdAt TIMESTAMP,
    responseAt TIMESTAMP,
    ref TEXT,
    description TEXT,
    type TEXT,
    originatingMessageId TEXT,
    buttonMessageId TEXT
);
'''
cur.execute(create_table_query)

# 提交事务并关闭连接
conn.commit()
cur.close()
conn.close()
