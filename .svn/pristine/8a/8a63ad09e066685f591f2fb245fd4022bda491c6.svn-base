"""
大模型配置文件
支持国内主流大模型API配置
"""
import os
from enum import Enum
from typing import Optional

# 导入环境变量加载工具
from env_loader import load_env_file


# 初始化时加载环境变量
load_env_file()


class ModelType(Enum):
    """支持的大模型类型"""
    QWEN = "qwen"           # 通义千问
    BAICHUAN = "baichuan"   # 百川
    YI = "yi"               # 火山引擎- Yi
    DOUBAO = "doubao"       # 字节跳动-豆包
    ZHIPU = "zhipu"         # 智谱AI
    MOONSHOT = "moonshot"   # 月之暗面
    MINIMAX = "minimax"     # MiniMax
    GEMINI = "gemini"       # Google Gemini（国际）
    OPENAI = "openai"       # OpenAI（国际）


class ModelConfig:
    """大模型配置类"""
    
    def __init__(self):
        # 通义千问配置
        self.qwen_api_key = os.getenv("QWEN_API_KEY", "")
        self.qwen_base_url = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        
        # 百川配置
        self.baichuan_api_key = os.getenv("BAICHUAN_API_KEY", "")
        self.baichuan_base_url = os.getenv("BAICHUAN_API_KEY", "https://api.baichuan-ai.com/v1")
        
        # 智谱AI配置
        self.zhipu_api_key = os.getenv("ZHIPU_API_KEY", "")
        self.zhipu_base_url = os.getenv("ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
        
        # 字节跳动豆包配置
        self.doubao_api_key = os.getenv("DOUBAO_API_KEY", "")
        self.doubao_base_url = os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
        
        # 月之暗面配置
        self.moonshot_api_key = os.getenv("MOONSHOT_API_KEY", "")
        self.moonshot_base_url = os.getenv("MOONSHOT_BASE_URL", "https://api.moonshot.cn/v1")
        
        # MiniMax配置
        self.minimax_api_key = os.getenv("MINIMAX_API_KEY", "")
        self.minimax_base_url = os.getenv("MINIMAX_BASE_URL", "https://api.minimaxi.chat/v1")
        
        # 默认使用模型
        self.default_model = os.getenv("DEFAULT_MODEL", "qwen-max")
        
        # 默认配置
        self.current_model_type = ModelType(os.getenv("CURRENT_MODEL_TYPE", "qwen"))
    
    def get_api_config(self, model_type: Optional[ModelType] = None) -> dict:
        """获取指定模型类型的API配置"""
        if model_type is None:
            model_type = self.current_model_type
            
        if model_type == ModelType.QWEN:
            return {
                "api_key": self.qwen_api_key,
                "base_url": self.qwen_base_url,
                "default_model": self.default_model
            }
        elif model_type == ModelType.ZHIPU:
            return {
                "api_key": self.zhipu_api_key,
                "base_url": self.zhipu_base_url,
                "default_model": self.default_model
            }
        elif model_type == ModelType.DOUBAO:
            return {
                "api_key": self.doubao_api_key,
                "base_url": self.doubao_base_url,
                "default_model": self.default_model
            }
        elif model_type == ModelType.MOONSHOT:
            return {
                "api_key": self.moonshot_api_key,
                "base_url": self.moonshot_base_url,
                "default_model": self.default_model
            }
        elif model_type == ModelType.MINIMAX:
            return {
                "api_key": self.minimax_api_key,
                "base_url": self.minimax_base_url,
                "default_model": self.default_model
            }
        else:
            # 默认使用通义千问配置
            return {
                "api_key": self.qwen_api_key,
                "base_url": self.qwen_base_url,
                "default_model": self.default_model
            }


# 全局配置实例
model_config = ModelConfig()


def set_current_model(model_type: ModelType):
    """设置当前使用的模型类型"""
    model_config.current_model_type = model_type


def get_current_model_config() -> dict:
    """获取当前模型配置"""
    return model_config.get_api_config()