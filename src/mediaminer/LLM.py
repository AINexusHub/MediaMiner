from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_community.chat_models.zhipuai import ChatZhipuAI
from typing import List, Optional
import os

# 设置API密钥
os.environ["ZHIPUAI_API_KEY"] = "cab1d9eb83594d81869369bcdf0d0519.Z737f2AJEVMsIoJ2"

class ZhipuLLM:
    def __init__(self, model_name: str = "glm-4.5-flash", temperature: float = 0.2):
        """
        初始化ZhipuLLM实例
        
        Args:
            model_name: 模型名称，默认为"glm-4.5-flash"
            temperature: 生成文本的随机性参数，范围0-1，默认为0.2
        """
        self.llm = ChatZhipuAI(model=model_name, temperature=temperature)
        self.history_messages: List[BaseMessage] = []  # 存储对话历史
    
    def chat(self, text: str, system_prompt: Optional[str] = None) -> str:
        """
        与模型进行对话（支持多轮）
        
        Args:
            text: 用户输入的文本
            system_prompt: 系统提示词（仅在首次调用或历史为空时生效）
            
        Returns:
            str: 模型的回复内容
        """
        # 如果历史为空且提供了系统提示词，则添加到历史中
        if not self.history_messages and system_prompt:
            self.history_messages.append(SystemMessage(content=system_prompt))
        
        # 添加用户消息到历史
        self.history_messages.append(HumanMessage(content=text))
        
        # 使用完整历史调用模型
        response = self.llm.invoke(self.history_messages)
        
        # 添加模型回复到历史
        self.history_messages.append(AIMessage(content=response.content))
        
        return response.content
    
    def clear_history(self) -> None:
        """清空对话历史"""
        self.history_messages.clear()
    
    def get_history(self) -> List[BaseMessage]:
        """
        获取当前对话历史
        
        Returns:
            List[BaseMessage]: 对话历史消息列表
        """
        return self.history_messages.copy()  # 返回副本，避免外部直接修改
    
    def set_history(self, history: List[BaseMessage]) -> None:
        """
        设置对话历史
        
        Args:
            history: 新的对话历史消息列表
        """
        self.history_messages = history.copy()  # 使用副本，避免外部直接修改

# 使用示例（多轮对话）
if __name__ == "__main__":
    # 创建实例
    llm = ZhipuLLM()
    
    # 开始多轮对话
    print("=== 多轮对话示例 ===")
    print("输入 'exit' 退出对话，输入 'clear' 清空历史")
    
    while True:
        user_input = input("\n你: ")
        
        if user_input.lower() == "exit":
            print("对话结束")
            break
        
        if user_input.lower() == "clear":
            llm.clear_history()
            print("对话历史已清空")
            continue
        
        # 获取模型回复
        try:
            response = llm.chat(user_input)
            print(f"AI: {response}")
        except Exception as e:
            print(f"发生错误: {e}")