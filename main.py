"""
建筑行业新商机分析 Agent Skill
项目入口文件
"""
import sys
import os
# 添加src目录到Python路径，以便能够导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core import analyze_opportunities, OpportunityAnalysisInput


def main():
    """主函数，用于演示功能"""
    print("建筑行业新商机分析 Agent Skill")
    print("请使用对应的前端界面或API调用此功能，或运行tests目录下的测试文件查看示例")


if __name__ == "__main__":
    main()