import sys
import os
# 添加项目根目录到Python路径，以便能够导入main模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import OpportunityAnalysisInput, analyze_opportunities
import asyncio


def get_user_input():
    """获取用户输入"""
    print("欢迎使用建筑行业新商机分析系统")
    print("=" * 40)
    
    # 建筑方向选择
    print("请选择建筑方向：")
    directions = [
        "1. 结构工程", "2. 岩土工程", "3. 桥梁与隧道工程", 
        "4. 道路与铁道工程", "5. 市政工程", "6. 水利工程", "7. 自定义"
    ]
    for d in directions:
        print(d)
    
    while True:
        try:
            direction_choice = int(input("请输入选项数字 (1-7): "))
            if 1 <= direction_choice <= 7:
                break
            else:
                print("请输入有效的选项数字 (1-7)")
        except ValueError:
            print("请输入有效的数字")
    
    if direction_choice == 7:
        construction_direction = input("请输入自定义建筑方向 (100字内): ")[:100]
    else:
        direction_map = {
            1: "结构工程", 2: "岩土工程", 3: "桥梁与隧道工程",
            4: "道路与铁道工程", 5: "市政工程", 6: "水利工程"
        }
        construction_direction = direction_map[direction_choice]
    
    # 客户类型选择
    print("\n请选择客户类型：")
    customer_types = [
        "1. 行政机关", "2. 事业单位", "3. 央企", 
        "4. 国企", "5. 上市公司", "6. 民营企业", "7. 自定义"
    ]
    for ct in customer_types:
        print(ct)
    
    while True:
        try:
            customer_choice = int(input("请输入选项数字 (1-7): "))
            if 1 <= customer_choice <= 7:
                break
            else:
                print("请输入有效的选项数字 (1-7)")
        except ValueError:
            print("请输入有效的数字")
    
    if customer_choice == 7:
        customer_type = input("请输入自定义客户类型 (100字内): ")[:100]
    else:
        customer_map = {
            1: "行政机关", 2: "事业单位", 3: "央企",
            4: "国企", 5: "上市公司", 6: "民营企业"
        }
        customer_type = customer_map[customer_choice]
    
    # 商机状态选择
    print("\n请选择商机状态：")
    business_statuses = [
        "1. 意向阶段", "2. 争夺阶段", "3. 竞标阶段", 
        "4. 废标重启", "5. 成果扩大", "6. 自定义"
    ]
    for bs in business_statuses:
        print(bs)
    
    while True:
        try:
            status_choice = int(input("请输入选项数字 (1-6): "))
            if 1 <= status_choice <= 6:
                break
            else:
                print("请输入有效的选项数字 (1-6)")
        except ValueError:
            print("请输入有效的数字")
    
    if status_choice == 6:
        business_status = input("请输入自定义商机状态 (100字内): ")[:100]
    else:
        status_map = {
            1: "意向阶段", 2: "争夺阶段", 3: "竞标阶段",
            4: "废标重启", 5: "成果扩大"
        }
        business_status = status_map[status_choice]
    
    return construction_direction, customer_type, business_status


async def run_analysis(construction_direction, customer_type, business_status):
    """运行分析"""
    print(f"\n正在分析 {construction_direction} 领域中 {customer_type} 类型客户的 {business_status} 商机...")
    
    # 创建输入对象
    input_data = OpportunityAnalysisInput(
        construction_direction=construction_direction,
        customer_type=customer_type,
        business_status=business_status
    )

    try:
        # 异步调用分析函数，不允许使用模拟数据
        result = await analyze_opportunities(input_data, use_mock_data=False)
        
        # 输出结果
        print(f"\n找到 {len(result.opportunities)} 个潜在商机:")
        print("=" * 60)
        for i, opportunity in enumerate(result.opportunities, 1):
            print(f"\n{i}. 公司名称: {opportunity.company_name}")
            print(f"   项目信息: {opportunity.project_info}")
            print(f"   证明信息: {opportunity.proof_info}")
            print(f"   推断信息: {opportunity.inferred_info}")
            print(f"   营销方案: {opportunity.marketing_plan}")
            print("-" * 60)
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        print("提示: 请检查您的API密钥配置和网络连接，确保大模型服务正常可用。")


async def main():
    """主函数"""
    while True:
        # 获取用户输入
        construction_direction, customer_type, business_status = get_user_input()
        
        # 运行分析
        await run_analysis(construction_direction, customer_type, business_status)
        
        # 询问是否继续
        continue_choice = input("\n是否继续分析其他商机? (y/n): ").lower().strip()
        if continue_choice not in ['y', 'yes', '是']:
            print("感谢使用建筑行业新商机分析系统！")
            break


if __name__ == "__main__":
    asyncio.run(main())