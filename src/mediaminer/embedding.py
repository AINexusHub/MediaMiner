from langchain_community.embeddings.zhipuai import ZhipuAIEmbeddings
from typing import List, Optional
import os

# 设置API密钥（可以从环境变量读取或直接设置）
os.environ["ZHIPUAI_API_KEY"] = "cab1d9eb83594d81869369bcdf0d0519.Z737f2AJEVMsIoJ2"

class ZhipuEmbedding:
    def __init__(self, model_name: str = "embedding-2"):
        """
        初始化智谱Embedding模型
        
        Args:
            model_name: Embedding模型名称，默认为"embedding-2"
        """
        self.embeddings = ZhipuAIEmbeddings(model=model_name)
    
    def embed_query(self, text: str) -> List[float]:
        
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        为多个文档文本生成嵌入向量
        
        Args:
            texts: 要生成嵌入向量的文本列表
            
        Returns:
            List[List[float]]: 嵌入向量列表
        """
        return self.embeddings.embed_documents(texts)

# 使用示例
if __name__ == "__main__":
    # 创建实例
    embedding = ZhipuEmbedding()
    
    # 单个文本嵌入
    text = "我国自主研发量子计算机 “悟空” 算力再突破 实现特定问题百倍提速"
    query_embedding = embedding.embed_query(text)
    print(f"单个文本嵌入向量维度: {len(query_embedding)}")
    print(f"向量前5个值: {query_embedding[:5]}")
    
    # 多个文本嵌入
    texts = ["世界人工智能大会今日开幕 多款国产大模型首发亮相", "全国统一电子病历查询系统上线 跨省市就医告别纸质证明个测试", "我国自主研发量子计算机 “悟空” 算力再突破 实现特定问题百倍提速"]
    document_embeddings = embedding.embed_documents(texts)
    print(f"\n多个文本嵌入数量: {len(document_embeddings)}")
    print(f"第一个向量维度: {len(document_embeddings[0])}")
    print(f"第一个向量前5个值: {document_embeddings[0][:5]}")