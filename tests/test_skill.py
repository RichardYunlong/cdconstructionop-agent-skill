"""
测试建筑行业新商机分析 Agent Skill
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 添加src目录到Python路径，以便能够导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# 加载环境变量
from src.env_loader import load_env_file
load_env_file()

from core import OpportunityAnalysisInput, analyze_opportunities


async def test_construction_opportunity_analyzer():
    """测试建筑行业新商机分析功能"""
    
    # 测试用例1：市政工程，国企，意向阶段
    print("=" * 60)
    print("测试用例1：市政工程，国企，意向阶段")
    print("=" * 60)
    
    input_data1 = OpportunityAnalysisInput(
        construction_direction="市政工程",
        customer_type="国企",
        business_status="意向阶段"
    )
    
    result1 = await analyze_opportunities(input_data1)
    
    print(f"找到 {len(result1.opportunities)} 个潜在商机:")
    for i, opp in enumerate(result1.opportunities, 1):
        print(f"\n{i}. 公司名称: {opp.company_name}")
        print(f"   项目信息: {opp.project_info}")
        print(f"   证明信息: {opp.proof_info}")
        print(f"   推断信息: {opp.inferred_info}")
        print(f"   营销方案: {opp.marketing_plan}")
    
    # 测试用例2：桥梁与隧道工程，上市公司，竞标阶段
    print("\n" + "=" * 60)
    print("测试用例2：桥梁与隧道工程，上市公司，竞标阶段")
    print("=" * 60)
    
    input_data2 = OpportunityAnalysisInput(
        construction_direction="桥梁与隧道工程",
        customer_type="上市公司",
        business_status="竞标阶段"
    )
    
    result2 = await analyze_opportunities(input_data2)
    
    print(f"找到 {len(result2.opportunities)} 个潜在商机:")
    for i, opp in enumerate(result2.opportunities, 1):
        print(f"\n{i}. 公司名称: {opp.company_name}")
        print(f"   项目信息: {opp.project_info}")
        print(f"   证明信息: {opp.proof_info}")
        print(f"   推断信息: {opp.inferred_info}")
        print(f"   营销方案: {opp.marketing_plan}")
    
    # 测试用例3：自定义方向，自定义客户类型，自定义商机状态
    print("\n" + "=" * 60)
    print("测试用例3：自定义方向，自定义客户类型，自定义商机状态")
    print("=" * 60)
    
    input_data3 = OpportunityAnalysisInput(
        construction_direction="绿色建筑技术",
        customer_type="环保科技企业",
        business_status="成果扩大"
    )
    
    result3 = await analyze_opportunities(input_data3)
    
    print(f"找到 {len(result3.opportunities)} 个潜在商机:")
    for i, opp in enumerate(result3.opportunities, 1):
        print(f"\n{i}. 公司名称: {opp.company_name}")
        print(f"   项目信息: {opp.project_info}")
        print(f"   证明信息: {opp.proof_info}")
        print(f"   推断信息: {opp.inferred_info}")
        print(f"   营销方案: {opp.marketing_plan}")


def main():
    """运行测试"""
    print("开始测试建筑行业新商机分析 Agent Skill...")
    import asyncio
    asyncio.run(test_construction_opportunity_analyzer())
    print("\n测试完成!")


if __name__ == "__main__":
    main()