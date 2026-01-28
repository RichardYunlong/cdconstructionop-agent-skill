"""
建筑行业新商机分析 Agent Skill
用于分析和生成建筑行业新商机清单
"""
import json
import asyncio
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
import aiohttp
import re

from utils import WebSearcher, ConstructionOpportunityHelper, GOVERNMENT_SITES, TENDER_SITES
from llm_client import opportunity_generator


class OpportunityAnalysisInput(BaseModel):
    """商机分析输入参数"""
    construction_direction: str = Field(
        ..., 
        description="建筑方向，可选值：结构工程、岩土工程、桥梁与隧道工程、道路与铁道工程、市政工程、水利工程，或自定义内容"
    )
    customer_type: str = Field(
        ..., 
        description="客户类型，可选值：行政机关、事业单位、央企、国企、上市公司、民营企业，或自定义内容"
    )
    business_status: str = Field(
        ..., 
        description="商机状态，可选值：意向阶段、争夺阶段、竞标阶段、废标重启、成果扩大，或自定义内容"
    )


class OpportunityInfo(BaseModel):
    """单个商机信息"""
    company_name: str = Field(..., description="公司名称")
    project_info: str = Field(..., description="项目信息，50字以内")
    proof_info: str = Field(..., description="证明信息，包括网站公告、招标信息等，255字以内")
    inferred_info: str = Field(..., description="基于网络信息推断的商机信息，255字以内")
    marketing_plan: str = Field(..., description="营销方案，255字以内")


class OpportunityAnalysisOutput(BaseModel):
    """商机分析输出结果"""
    opportunities: List[OpportunityInfo] = Field(..., description="商机列表，包含5个客户或潜在客户的信息")


async def search_for_construction_opportunities(construction_direction: str, customer_type: str) -> List[Dict]:
    """
    搜索相关的建筑行业机会信息
    """
    # 创建搜索关键词
    direction_keywords = {
        "结构工程": ["建筑工程", "高层建筑", "工业厂房"],
        "岩土工程": ["地基基础", "地下空间", "边坡治理"],
        "桥梁与隧道工程": ["桥梁建设", "隧道工程", "跨海工程"],
        "道路与铁道工程": ["高速公路", "城市道路", "铁路建设"],
        "市政工程": ["市政建设", "基础设施", "管网改造"],
        "水利工程": ["水库建设", "引水工程", "防洪治理"]
    }
    
    keywords = direction_keywords.get(construction_direction, [construction_direction])
    
    # 构造搜索查询
    search_results = []
    
    # 模拟搜索结果，实际应用中这里会连接大模型API或搜索引擎
    for i, keyword in enumerate(keywords[:2]):  # 只取前两个关键词
        # 生成模拟搜索结果
        for j in range(3):  # 每个关键词生成3个结果
            idx = len(search_results) + 1
            search_results.append({
                "company_name": f"{customer_type}模拟公司{idx}",
                "project_info": f"关于{keyword}的{construction_direction}项目，投资规模可观",
                "proof_info": f"根据{keyword.replace(' ', '')}.gov.cn网站公示信息，该项目已进入规划阶段，预计年内启动招标。链接：http://www.{keyword.replace(' ', '')}.gov.cn/notice/{idx}",
                "inferred_info": f"从该公司官网和行业媒体报道看，该项目有明确的资金支持和技术需求。参见：http://www.industrynews.com/article/{idx}",
                "marketing_plan": f"结合{ConstructionOpportunityHelper.get_business_status_strategy(customer_type)}策略，突出我们在此类{construction_direction}项目中的优势，安排技术专家进行深度交流。"
            })
    
    return search_results[:5]  # 返回前5个结果


async def analyze_opportunities(input_data: OpportunityAnalysisInput, use_mock_data: bool = True) -> OpportunityAnalysisOutput:
    """
    分析建筑行业新商机
    根据建筑方向、客户类型和商机状态生成5个潜在客户分析
    """
    # 使用辅助类获取相关信息
    direction_desc = ConstructionOpportunityHelper.get_construction_direction_description(input_data.construction_direction)
    customer_desc = ConstructionOpportunityHelper.get_customer_type_description(input_data.customer_type)
    status_strategy = ConstructionOpportunityHelper.get_business_status_strategy(input_data.business_status)
    
    # 调用大模型生成商机分析
    llm_results = await opportunity_generator.generate_opportunities(
        input_data.construction_direction,
        input_data.customer_type,
        input_data.business_status
    )
    
    # 如果大模型返回了有效结果，使用它；否则使用原有逻辑
    if llm_results and len(llm_results) >= 5:
        opportunities = []
        for item in llm_results[:5]:  # 取前5个结果
            opportunities.append(OpportunityInfo(
                company_name=item.get("company_name", "未知公司"),
                project_info=item.get("project_info", "暂无项目信息"),
                proof_info=item.get("proof_info", "暂无证明信息"),
                inferred_info=item.get("inferred_info", "暂无推断信息"),
                marketing_plan=item.get("marketing_plan", "暂无营销方案")
            ))
        return OpportunityAnalysisOutput(opportunities=opportunities)
    
    # 如果不允许使用模拟数据，直接抛出异常
    if not use_mock_data:
        raise Exception("大模型调用失败，且不允许使用模拟数据")
    
    # 如果大模型调用失败或返回结果不足，使用原有逻辑
    # 搜索相关机会
    search_results = await search_for_construction_opportunities(
        input_data.construction_direction, 
        input_data.customer_type
    )
    
    # 如果没有足够的搜索结果，生成默认结果
    if len(search_results) < 5:
        sample_data = [
            {
                "company_name": f"{input_data.customer_type}头部企业一",
                "project_info": f"[{input_data.construction_direction}] 大型建设项目，预计投资规模超10亿",
                "proof_info": f"根据相关政府网站({GOVERNMENT_SITES[0]})和招标平台({TENDER_SITES[0]})信息，该公司近期发布了相关项目的前期公告，显示项目已进入筹备阶段。",
                "inferred_info": f"从该企业的年度报告和公开信息分析，企业正在扩大业务规模，对数字化项目管理需求增长，符合当前市场趋势。",
                "marketing_plan": f"针对{input_data.customer_type}的特点({customer_desc})，采用{status_strategy}策略，突出产品在{input_data.construction_direction}领域的专业能力，安排行业专家进行交流。"
            },
            {
                "company_name": f"{input_data.customer_type}领军企业二",
                "project_info": f"[{input_data.construction_direction}] 技术创新项目，注重智能化管理",
                "proof_info": f"根据行业媒体和企业官网信息，该公司正在推进数字化转型，相关招标预告已在多个招标网站公布。详情见：{TENDER_SITES[1]}",
                "inferred_info": f"从该公司近期招聘和技术投入看，对先进项目管理工具有迫切需求，是我们产品的理想客户。",
                "marketing_plan": f"重点展示产品的智能化特性，提供定制化解决方案演示，安排成功案例分享会。"
            },
            {
                "company_name": f"{input_data.customer_type}成长型企业三",
                "project_info": f"[{input_data.construction_direction}] 扩张性项目，涉及多地区协调",
                "proof_info": f"从企业年报和新闻公告看，该公司正在快速扩张，多个项目同步进行，对项目管理软件需求明显。",
                "inferred_info": f"通过监测其社交媒体和行业论坛，发现其内部对项目协同工具有较多讨论，存在痛点。",
                "marketing_plan": f"强调多项目协同管理能力，提供灵活的部署方案和培训支持，降低实施难度。"
            },
            {
                "company_name": f"{input_data.customer_type}专业化公司四",
                "project_info": f"[{input_data.construction_direction}] 专业领域项目，技术要求高",
                "proof_info": f"根据行业报告和专业网站信息，该公司承接了多个高端项目，对项目管理工具有特殊要求。",
                "inferred_info": f"从技术论坛和学术论文看，该公司注重技术创新，在项目管理方面寻求突破。",
                "marketing_plan": f"突出产品在{input_data.construction_direction}的专业功能，提供技术对接和定制开发服务。"
            },
            {
                "company_name": f"{input_data.customer_type}新兴企业五",
                "project_info": f"[{input_data.construction_direction}] 新兴领域项目，注重效率提升",
                "proof_info": f"根据商业信息平台和新闻报道，该公司在新兴领域快速发展，急需高效管理工具。",
                "inferred_info": f"从其发展速度和市场策略看，对提升运营效率的工具需求强烈。",
                "marketing_plan": f"强调快速部署和易用性，提供SaaS服务选项和快速培训支持。"
            }
        ]
        
        # 将搜索结果与默认数据合并
        for i in range(len(search_results)):
            sample_data[i] = search_results[i]
        
        search_results = sample_data
    
    opportunities = []
    for item in search_results:
        opportunities.append(OpportunityInfo(
            company_name=item["company_name"],
            project_info=item["project_info"],
            proof_info=item["proof_info"],
            inferred_info=item["inferred_info"],
            marketing_plan=item["marketing_plan"]
        ))
    
    return OpportunityAnalysisOutput(opportunities=opportunities)


def main():
    """主函数，用于测试"""
    print("建筑行业新商机分析 Agent Skill")
    print("请使用对应的前端界面或API调用此功能")


if __name__ == "__main__":
    main()