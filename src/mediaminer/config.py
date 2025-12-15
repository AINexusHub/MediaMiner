from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field

# 1. 加载环境变量
# 加载本地.env文件，开发环境用；生产环境部署时，注释这行，从系统环境变量读
load_dotenv()
# 读取当前环境（开发/生产）
APP_ENV = os.getenv("APP_ENV", "development")

# 2. 定义各模块的配置类
class DatabaseConfig(BaseModel):
    """数据库配置"""
    host: str = Field(..., description="数据库主机地址")
    port: int = Field(..., description="数据库端口")
    user: str = Field(..., description="数据库用户名")
    password: str = Field(..., description="数据库密码")
    db_name: str = Field(..., description="数据库名称")

class MinioConfig(BaseModel):
    """MinIO对象存储配置"""
    endpoint: str = Field(..., description="MinIO服务地址")
    access_key: str = Field(..., description="MinIO访问密钥")
    secret_key: str = Field(..., description="MinIO密钥")
    bucket_name: str = Field(..., description="存储桶名称")

class MilvusConfig(BaseModel):
    """Milvus向量数据库配置"""
    host: str = Field(..., description="Milvus主机地址")
    port: int = Field(..., description="Milvus端口")
    collection_name: str = Field(..., description="向量集合名称")

class AIServiceConfig(BaseModel):
    """AI服务配置"""
    api_url: str = Field(..., description="AI接口地址")
    api_key: str = Field(..., description="AI接口密钥")
    timeout: int = Field(default=30, description="请求超时时间（秒）")

#  3. 主配置类（整合所有模块）
class AppConfig(BaseModel):
    """项目主配置"""
    debug: bool = Field(description="调试模式")
    log_level: str = Field(description="日志级别")
    database: DatabaseConfig  # 数据库配置
    minio: MinioConfig        # MinIO配置
    milvus: MilvusConfig      # Milvus配置
    ai_service: AIServiceConfig  # AI服务配置

#  4. 按环境加载配置
def load_app_config() -> AppConfig:
    """加载当前环境的配置"""
    if APP_ENV == "production":
        # 生产环境：从系统环境变量读取（更安全）
        return AppConfig(
            debug=False,
            log_level="WARNING",
            database=DatabaseConfig(
                host=os.getenv("PROD_DB_HOST"),
                port=int(os.getenv("PROD_DB_PORT")),
                user=os.getenv("PROD_DB_USER"),
                password=os.getenv("PROD_DB_PASSWORD"),
                db_name=os.getenv("PROD_DB_NAME")
            ),
            minio=MinioConfig(
                endpoint=os.getenv("PROD_MINIO_ENDPOINT"),
                access_key=os.getenv("PROD_MINIO_ACCESS_KEY"),
                secret_key=os.getenv("PROD_MINIO_SECRET_KEY"),
                bucket_name=os.getenv("PROD_MINIO_BUCKET")
            ),
            milvus=MilvusConfig(
                host=os.getenv("PROD_MILVUS_HOST"),
                port=int(os.getenv("PROD_MILVUS_PORT")),
                collection_name=os.getenv("PROD_MILVUS_COLLECTION")
            ),
            ai_service=AIServiceConfig(
                api_url=os.getenv("PROD_AI_API_URL"),
                api_key=os.getenv("PROD_AI_API_KEY"),
                timeout=int(os.getenv("PROD_AI_TIMEOUT", 30))
            )
        )
    else:
        # 开发环境：从.env文件读取
        return AppConfig(
            debug=True,
            log_level="INFO",
            database=DatabaseConfig(
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", 3306)),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "root"),
                db_name=os.getenv("DB_NAME", "news_assistant")
            ),
            minio=MinioConfig(
                endpoint=os.getenv("MINIO_ENDPOINT", "localhost:9000"),
                access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
                secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
                bucket_name=os.getenv("MINIO_BUCKET", "news-bucket")
            ),
            milvus=MilvusConfig(
                host=os.getenv("MILVUS_HOST", "localhost"),
                port=int(os.getenv("MILVUS_PORT", 19530)),
                collection_name=os.getenv("MILVUS_COLLECTION", "news_vector")
            ),
            ai_service=AIServiceConfig(
                api_url=os.getenv("AI_API_URL", "http://localhost:8000/v1/chat"),
                api_key=os.getenv("AI_API_KEY", "test_key"),
                timeout=int(os.getenv("AI_TIMEOUT", 30))
            )
        )

# 5. 对外提供配置实例
# 项目其他模块直接导入这个config即可使用
config = load_app_config()