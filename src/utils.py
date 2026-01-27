"""
工具模块，提供网络搜索和信息验证功能
"""
import re
from typing import List, Dict, Optional
import aiohttp
from urllib.parse import urljoin, urlparse


class WebSearcher:
    """网络搜索工具类"""
    
    @staticmethod
    async def validate_url(url: str) -> bool:
        """
        验证URL是否有效
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    return response.status == 200
        except Exception:
            return False
    
    @staticmethod
    async def extract_key_info_from_text(text: str) -> Dict[str, List[str]]:
        """
        从文本中提取关键信息，如URL、项目名称、时间等
        """
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        dates = re.findall(r'\d{4}[年\-]\d{1,2}[月\-]\d{1,2}[日]?', text)
        project_names = re.findall(r'(?:项目|工程)\w*(?:建设|规划|招标|中标)', text)
        
        return {
            "urls": urls,
            "dates": dates,
            "project_names": project_names
        }


class ConstructionOpportunityHelper:
    """建筑商机分析辅助类"""
    
    @staticmethod
    def get_construction_direction_description(direction: str) -> str:
        """
        获取建筑方向描述
        """
        descriptions = {
            "结构工程": "涉及建筑物承重体系的设计与施工，包括高层建筑、工业厂房等结构设计与建造",
            "岩土工程": "研究岩石与土体工程性质的应用学科，涵盖地基基础、边坡稳定、地下空间开发等领域",
            "桥梁与隧道工程": "专注于跨越障碍物的交通构造物设计与施工，包括各类桥梁、隧道及地下通道",
            "道路与铁道工程": "从事公路、城市道路及铁路线路的规划、设计、施工与维护",
            "市政工程": "服务于城市公共设施的建设工程，包括供水排水、燃气热力、公共交通等基础设施",
            "水利工程": "涉及水资源开发利用的工程，包括防洪、灌溉、发电、航运等水利设施"
        }
        return descriptions.get(direction, direction)
    
    @staticmethod
    def get_customer_type_description(customer_type: str) -> str:
        """
        获取客户类型特征描述
        """
        descriptions = {
            "行政机关": "政府组成部门及直属机构，决策流程规范，重视合规性，预算相对固定",
            "事业单位": "公益性质单位，有一定自主权，资金来源多元，注重社会效益",
            "央企": "国家控股的重要企业，管理体系完善，技术要求高，注重长期合作",
            "国企": "地方国资委监管企业，决策链条较短，成本控制严格",
            "上市公司": "公众持股公司，透明度要求高，注重ROI，决策相对灵活",
            "民营企业": "私人控股企业，决策效率高，成本敏感，注重实用性"
        }
        return descriptions.get(customer_type, customer_type)
    
    @staticmethod
    def get_business_status_strategy(status: str) -> str:
        """
        获取不同商机状态下应对策略
        """
        strategies = {
            "意向阶段": "加强关系建立，提供前期咨询，影响需求定义",
            "争夺阶段": "展示差异化优势，提供定制化方案，深化客户关系",
            "竞标阶段": "优化技术方案，确保投标质量，加强风险管控",
            "废标重启": "分析失败原因，改进方案，争取优先考虑",
            "成果扩大": "挖掘新需求，推荐升级服务，促进转介绍"
        }
        return strategies.get(status, status)


# 定义一些常用的政府和行业网站，用于信息验证
GOVERNMENT_SITES = [
    "http://www.gov.cn/",
    "http://www.mohurd.gov.cn/",  # 住建部
    "http://www.mwr.gov.cn/",     # 水利部
    "http://www.nra.gov.cn/"      # 铁路局
]

TENDER_SITES = [
    "https://www.cctc.com/",      # 中国采购与招标网
    "http://www.cebpubservice.com/",  # 中国招标公共服务平台
    "https://www.zhaobiao.cn/"    # 招标网
]

ENTERPRISE_SITES = [
    "http://www.sse.com.cn/",     # 上交所
    "http://www.szse.cn/",        # 深交所
    "https://www.tianyancha.com/" # 天眼查
]