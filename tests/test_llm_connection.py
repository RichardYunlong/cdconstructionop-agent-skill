"""
测试大模型连接性的脚本
用于验证大模型API是否配置正确并可以正常使用
"""
import asyncio
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from src.llm_client import LLMClient
from src.model_config import get_current_model_config


async def test_llm_connection():
    """
    测试大模型连接性
    """
    print("=" * 60)
    print("开始测试大模型连接性...")
    print("=" * 60)
    
    # 显示当前模型配置
    config = get_current_model_config()
    print(f"当前模型配置:")
    print(f"- 模型名称: {config['default_model']}")
    print(f"- API端点: {config['base_url']}")
    print(f"- API密钥状态: {'已配置' if config['api_key'] else '未配置'}")
    print("-" * 60)
    
    if not config['api_key']:
        print("❌ 错误: API密钥未配置")
        print("请在 .env 文件中配置相应的API密钥")
        print("例如: QWEN_API_KEY='your_api_key_here'")
        return False
    
    # 创建LLM客户端并测试连接
    llm_client = LLMClient()
    
    # 准备测试消息
    test_messages = [
        {"role": "system", "content": "你是一个有用的助手。"},
        {"role": "user", "content": "你好，请简单介绍一下你自己，限制在50字以内。"}
    ]
    
    try:
        print("正在发送测试请求到大模型...")
        response = await llm_client.call_llm(test_messages, temperature=0.7, max_tokens=100)
        
        print("✅ 大模型连接测试成功!")
        print("-" * 60)
        print("大模型回复:")
        print(response)
        print("-" * 60)
        print("✅ 测试完成: 大模型连接正常")
        return True
        
    except Exception as e:
        print(f"❌ 大模型连接测试失败: {str(e)}")
        print("-" * 60)
        return False


async def test_url_formatting():
    """
    测试URL格式化功能
    """
    print("\n" + "=" * 60)
    print("测试URL格式化功能...")
    print("=" * 60)
    
    # 创建一个临时的LLMClient实例来测试URL格式化功能
    llm_client = LLMClient()
    
    # 测试包含URL的文本
    test_text_with_urls = """
    这里有一些网址：
    - 百度: https://www.baidu.com
    - GitHub: https://github.com
    - 阿里云: https://www.aliyun.com/path/to/service?param=value
    还有一个HTTP链接: http://example.com
    """
    
    formatted_text = llm_client._format_urls(test_text_with_urls)
    
    print("原始文本:")
    print(test_text_with_urls)
    print("\n格式化后的文本:")
    print(formatted_text)
    print("\n✅ URL格式化功能测试完成")
    

async def main():
    """
    主函数，运行所有测试
    """
    print("🔧 大模型连接性测试工具")
    print("此工具将测试大模型API的连接性和基本功能")
    
    # 测试大模型连接
    connection_success = await test_llm_connection()
    
    # 测试URL格式化功能
    await test_url_formatting()
    
    print("\n" + "=" * 60)
    print("测试总结:")
    if connection_success:
        print("✅ 所有测试通过，大模型配置正确，可以正常使用")
    else:
        print("❌ 连接测试失败，请检查API密钥和网络连接")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())