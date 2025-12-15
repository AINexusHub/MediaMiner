-- 创建飞书用户表
CREATE TABLE IF NOT EXISTS feishu_users (
    user_id VARCHAR(64) NOT NULL COMMENT '飞书用户ID',
    user_name VARCHAR(64) COMMENT '飞书用户名',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='飞书用户表';

-- 创建用户兴趣表
CREATE TABLE IF NOT EXISTS user_interests (
    id INT AUTO_INCREMENT COMMENT '主键ID',
    user_id VARCHAR(64) NOT NULL COMMENT '飞书用户ID',
    interest_tag VARCHAR(32) NOT NULL COMMENT '兴趣标签（如AI、科技）',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (id),
    UNIQUE KEY idx_user_tag (user_id, interest_tag),
    FOREIGN KEY (user_id) REFERENCES feishu_users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户兴趣表';

-- 初始化测试数据（可选）
INSERT INTO feishu_users (user_id, user_name) VALUES ('test001', '测试用户') ON DUPLICATE KEY UPDATE user_name='测试用户';