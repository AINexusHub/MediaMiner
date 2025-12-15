from minio import Minio
from minio.error import S3Error
import json
import os
from datetime import datetime


# MinIO配置类（统一管理配置，便于后续修改）
class MinioConfig:
    endpoint = "localhost:9000"  # MinIO容器映射的端口
    access_key = "minioadmin"  # MinIO默认账号（若你改了需同步）
    secret_key = "minioadmin123"  # MinIO默认密码（若你改了需同步）
    secure = False  # 本地测试关闭HTTPS
    default_bucket = "news-data"  # 默认存储桶（存放新闻相关文件）


# MinIO客户端封装类（核心功能）
class MinioClient:
    def __init__(self, config: MinioConfig = None):
        # 初始化配置
        self.config = config or MinioConfig()
        # 创建MinIO客户端连接
        self.client = Minio(
            endpoint=self.config.endpoint,
            access_key=self.config.access_key,
            secret_key=self.config.secret_key,
            secure=self.config.secure
        )
        # 确保默认存储桶存在（不存在则创建）
        self._ensure_bucket(self.config.default_bucket)

    def _ensure_bucket(self, bucket_name: str):
        """私有方法：确保存储桶存在，不存在则创建"""
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                print(f"✅ 存储桶 [{bucket_name}] 创建成功")
            else:
                print(f"✅ 存储桶 [{bucket_name}] 已存在")
        except S3Error as e:
            print(f"❌ 创建存储桶失败：{e}")

    def upload_json(self, object_name: str, data: dict, bucket_name: str = None):
        """
        上传JSON数据到MinIO（修复字节数据传参问题）
        :param object_name: 存储的文件名（如raw/2025/12/14/test-001.json）
        :param data: 要上传的字典数据（会自动转为JSON字符串）
        :param bucket_name: 存储桶名（默认用配置的default_bucket）
        :return: 成功返回True，失败返回False
        """
        bucket_name = bucket_name or self.config.default_bucket
        try:
            # 将字典转为JSON字符串并编码为字节
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            json_bytes = json_str.encode("utf-8")

            # 关键修复：用io.BytesIO包装字节数据（满足MinIO SDK的read()方法要求）
            from io import BytesIO
            data_stream = BytesIO(json_bytes)

            # 上传到MinIO（length传字节长度，data传包装后的流对象）
            self.client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=data_stream,  # 替换为BytesIO包装的流
                length=len(json_bytes),
                content_type="application/json"  # 指定文件类型为JSON
            )
            print(f"✅ JSON文件 [{object_name}] 上传到存储桶 [{bucket_name}] 成功")
            return True
        except S3Error as e:
            print(f"❌ 上传JSON失败：{e}")
            return False

    def download_json(self, object_name: str, bucket_name: str = None) -> dict:
        """
        从MinIO下载JSON文件并解析为字典
        :param object_name: 要下载的文件名
        :param bucket_name: 存储桶名
        :return: 成功返回字典，失败返回None
        """
        bucket_name = bucket_name or self.config.default_bucket
        try:
            # 下载文件
            response = self.client.get_object(bucket_name, object_name)
            with response:
                # 读取字节并解析为字典
                json_bytes = response.read()
                data = json.loads(json_bytes.decode("utf-8"))
            print(f"✅ JSON文件 [{object_name}] 下载成功")
            return data
        except S3Error as e:
            print(f"❌ 下载JSON失败：{e}")
            return None

    def file_exists(self, object_name: str, bucket_name: str = None) -> bool:
        """
        检查MinIO中是否存在指定文件
        :param object_name: 文件名
        :param bucket_name: 存储桶名
        :return: 存在返回True，不存在返回False
        """
        bucket_name = bucket_name or self.config.default_bucket
        try:
            # 检查文件状态
            self.client.stat_object(bucket_name, object_name)
            print(f"✅ 文件 [{object_name}] 存在于存储桶 [{bucket_name}]")
            return True
        except S3Error as e:
            # 404错误表示文件不存在，其他错误返回False
            if e.code == "NoSuchKey":
                print(f"❌ 文件 [{object_name}] 不存在于存储桶 [{bucket_name}]")
                return False
            else:
                print(f"❌ 检查文件失败：{e}")
                return False


# 测试代码（验证客户端功能）
if __name__ == "__main__":
    # 1. 初始化客户端
    minio_cli = MinioClient()

    # 2. 准备测试JSON数据
    test_news = {
        "news_id": "test-001",
        "title": "2025科技趋势：AI与大数据融合",
        "content": "人工智能与大数据的深度融合将成为2025年科技行业的核心趋势...",
        "publish_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tags": ["AI", "大数据", "科技趋势"]
    }

    # 3. 按日期路径上传（符合业务规范：raw/年/月/日/文件名）
    date_path = datetime.now().strftime("%Y/%m/%d")
    object_name = f"raw/{date_path}/test-001.json"

    # 4. 测试上传
    minio_cli.upload_json(object_name, test_news)

    # 5. 测试文件存在性检查
    minio_cli.file_exists(object_name)

    # 6. 测试下载
    downloaded_data = minio_cli.download_json(object_name)
    if downloaded_data:
        print("📥 下载的JSON数据：")
        print(json.dumps(downloaded_data, ensure_ascii=False, indent=2))