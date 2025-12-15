import pymysql

# 仅保留核心连接参数，适配新容器配置
conn = pymysql.connect(
    host="localhost",
    port=3307,
    user="root",
    password="Root@123456",  
    database="news_bot_db",
    charset="utf8mb4"
)

try:
    cursor = conn.cursor()
    # 验证表存在
    cursor.execute("SHOW TABLES;")
    print("✅ 数据库表列表：", cursor.fetchall())
    # 插入测试数据
    cursor.execute("INSERT INTO feishu_users (user_id, user_name) VALUES ('test001', '测试用户') ON DUPLICATE KEY UPDATE user_name='测试用户';")
    conn.commit()
    # 查询数据
    cursor.execute("SELECT * FROM feishu_users;")
    print("✅ 查询结果：", cursor.fetchall())
except Exception as e:
    print("❌ 错误：", str(e))
    conn.rollback()
finally:
    conn.close()