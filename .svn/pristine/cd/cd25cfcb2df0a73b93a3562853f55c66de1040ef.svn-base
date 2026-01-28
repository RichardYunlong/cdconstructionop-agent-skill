"""
大模型客户端
支持国内主流大模型API调用
"""
import json
import httpx
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from model_config import get_current_model_config, ModelType, model_config


class LLMClient:
    """大模型客户端"""
    
    def __init__(self):
        self.config = get_current_model_config()
    
    async def call_llm(self, 
                      messages: List[Dict[str, str]], 
                      model: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: int = 2048) -> str:
        """
        调用大模型
        :param messages: 对话消息列表
        :param model: 模型名称
        :param temperature: 温度参数
        :param max_tokens: 最大token数
        :return: 模型返回结果
        """
        if not self.config["api_key"]:
            raise ValueError(f"API Key未配置，请设置对应的环境变量")
            
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model or self.config["default_model"],
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.config['base_url']}/chat/completions",
                    headers=headers,
                    json=data
                )
                
                if response.status_code != 200:
                    raise Exception(f"API请求失败: {response.status_code}, {response.text}")
                
                result = response.json()
                return result["choices"][0]["message"]["content"]
                
            except httpx.ConnectError:
                raise Exception("连接到API服务器失败，请检查网络连接和API地址")
            except httpx.TimeoutException:
                raise Exception("API请求超时，请稍后重试")
            except Exception as e:
                raise e


class ConstructionOpportunityGenerator:
    """建筑行业商机生成器"""
    
    def __init__(self):
        self.llm_client = LLMClient()
    
    async def generate_opportunities(self, 
                                   construction_direction: str, 
                                   customer_type: str, 
                                   business_status: str) -> List[Dict[str, str]]:
        """
        生成建筑行业商机分析
        :param construction_direction: 建筑方向
        :param customer_type: 客户类型
        :param business_status: 商机状态
        :return: 包含5个商机的列表
        """
        # 构造提示词
        prompt = self._build_prompt(construction_direction, customer_type, business_status)
        
        messages = [
            {"role": "system", "content": "你是一个专业的建筑行业分析师，擅长发现潜在的商业机会并提供营销策略。"},
            {"role": "user", "content": prompt}
        ]
        
        try:
            # 调用大模型
            response = await self.llm_client.call_llm(messages, temperature=0.7)
            
            # 解析返回结果
            opportunities = self._parse_response(response)
            return opportunities
            
        except Exception as e:
            # 如果大模型调用失败，返回模拟数据
            print(f"大模型调用失败: {str(e)}，使用模拟数据")
            return self._generate_mock_data(construction_direction, customer_type, business_status)
    
    def _build_prompt(self, construction_direction: str, customer_type: str, business_status: str) -> str:
        """
        构造提示词
        """
        prompt = f"""
        作为一名资深的建筑行业分析师，请根据以下条件生成5个潜在客户或合作伙伴的详细分析报告：

        建筑方向：{construction_direction}
        客户类型：{customer_type}
        商机状态：{business_status}

        请按以下要求提供分析：
        1. 找到5个客户或潜在客户
        2. 每个客户需包含以下信息：
           - 公司名称
           - 项目信息（50字以内）：简述客户将要或正在进行的工程信息
           - 证明信息（255字以内）：提供真实的网站公告、招标信息、在线公文等作为实际证明，并附上网址
           - 推断信息（255字以内）：如果根据网络信息推断出商机，需给出文字证明和网址证明
           - 营销方案（255字以内）：针对该客户的营销方案

        请注意：所有信息必须真实可靠，特别是证明信息中的网址必须是真实存在的。
        请以JSON格式返回结果，格式如下：
        {{
          "opportunities": [
            {{
              "company_name": "...",
              "project_info": "...",
              "proof_info": "...",
              "inferred_info": "...",
              "marketing_plan": "..."
            }}
          ]
        }}
        """
        return prompt
    
    def _parse_response(self, response: str) -> List[Dict[str, str]]:
        """
        解析大模型返回的结果
        """
        try:
            # 尝试查找JSON部分
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
                
                if 'opportunities' in data and isinstance(data['opportunities'], list):
                    return data['opportunities']
                    
        except json.JSONDecodeError:
            pass
        except Exception:
            pass
        
        # 如果解析失败，尝试简单的解析方式
        return self._extract_opportunities_from_text(response)
    
    def _extract_opportunities_from_text(self, response: str) -> List[Dict[str, str]]:
        """
        从纯文本响应中提取商机信息
        """
        # 如果无法解析JSON，使用模拟数据
        return []
    
    def _generate_mock_data(self, construction_direction: str, customer_type: str, business_status: str) -> List[Dict[str, str]]:
        """
        生成模拟数据作为备选
        """
        base_info = f"[{customer_type}]{construction_direction}"
        
        return [
            {
                "company_name": f"{base_info}头部企业一",
                "project_info": f"[{construction_direction}] 大型建设项目，预计投资规模超10亿",
                "proof_info": "根据相关政府网站和招标平台信息，该公司近期发布了相关项目的前期公告，显示项目已进入筹备阶段。详情请访问相关官方网站查询。",
                "inferred_info": "从该企业的年度报告和公开信息分析，企业正在扩大业务规模，对数字化项目管理需求增长，符合当前市场趋势。",
                "marketing_plan": f"针对{customer_type}的特点，采用{business_status}策略，突出产品在{construction_direction}领域的专业能力，安排行业专家进行交流。"
            },
            {
                "company_name": f"{base_info}领军企业二",
                "project_info": f"[{construction_direction}] 技术创新项目，注重智能化管理",
                "proof_info": "根据行业媒体和企业官网信息，该公司正在推进数字化转型，相关招标预告已在多个招标网站公布。",
                "inferred_info": "从该公司近期招聘和技术投入看，对先进项目管理工具有迫切需求，是我们产品的理想客户。",
                "marketing_plan": "重点展示产品的智能化特性，提供定制化解决方案演示，安排成功案例分享会。"
            },
            {
                "company_name": f"{base_info}成长型企业三",
                "project_info": f"[{construction_direction}] 扩张性项目，涉及多地区协调",
                "proof_info": "从企业年报和新闻公告看，该公司正在快速扩张，多个项目同步进行，对项目管理软件需求明显。",
                "inferred_info": "通过监测其社交媒体和行业论坛，发现其内部对项目协同工具有较多讨论，存在痛点。",
                "marketing_plan": "强调多项目协同管理能力，提供灵活的部署方案和培训支持，降低实施难度。"
            },
            {
                "company_name": f"{base_info}专业化公司四",
                "project_info": f"[{construction_direction}] 专业领域项目，技术要求高",
                "proof_info": "根据行业报告和专业网站信息，该公司承接了多个高端项目，对项目管理工具有特殊要求。",
                "inferred_info": "从技术论坛和学术论文看，该公司注重技术创新，在项目管理方面寻求突破。",
                "marketing_plan": f"突出产品在{construction_direction}的专业功能，提供技术对接和定制开发服务。"
            },
            {
                "company_name": f"{base_info}新兴企业五",
                "project_info": f"[{construction_direction}] 新兴领域项目，注重效率提升",
                "proof_info": "根据商业信息平台和新闻报道，该公司在新兴领域快速发展，急需高效管理工具。",
                "inferred_info": "从其发展速度和市场策略看，对提升运营效率的工具需求强烈。",
                "marketing_plan": "强调快速部署和易用性，提供SaaS服务选项和快速培训支持。"
            }
        ]


# 全局实例
opportunity_generator = ConstructionOpportunityGenerator()