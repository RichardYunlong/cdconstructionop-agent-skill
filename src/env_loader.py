"""
环境变量加载工具
用于加载项目中的环境变量配置
"""
import os
from pathlib import Path
from typing import Optional


def load_env_file(env_path: Optional[str] = None) -> bool:
    """
    加载环境变量文件
    :param env_path: 环境变量文件路径，默认为项目根目录下的 .env 文件
    :return: 是否成功加载
    """
    if env_path is None:
        # 默认使用项目根目录下的 .env 文件
        # 获取当前文件的父目录的父目录，即项目根目录
        project_root = Path(__file__).parent.parent
        env_path = project_root / ".env"
    else:
        env_path = Path(env_path)
    
    if not env_path.exists():
        print(f"警告: 环境变量文件不存在: {env_path}")
        print("请复制 .env.example 文件为 .env 并配置您的API密钥")
        return False
    
    try:
        # 读取环境变量文件
        with open(env_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                # 忽略注释行和空行
                if line and not line.startswith('#'):
                    # 解析 KEY=VALUE 格式的行
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # 移除可能的引号
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    # 设置环境变量
                    os.environ[key] = value
        
        print(f"成功加载环境变量文件: {env_path}")
        return True
        
    except Exception as e:
        print(f"加载环境变量文件失败: {str(e)}")
        return False


# 尝试加载环境变量文件
load_env_file()