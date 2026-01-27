# 🐲龙建商机 ✨
## 📌 项目概述
本项目是一个基于 AI Agent 的 Skill 工具，专用于分析建筑行业的新商机💡。根据用户指定的建筑方向、客户类型和商机状态，自动生成包含 5 个潜在客户或合作伙伴 的详细分析报告📊，助力企业快速锁定市场机会🚀。
## 🌟 功能特点
- 多维度分析支持🌐：覆盖结构工程、岩土工程、桥梁与隧道工程等多种建筑方向
- 全客户类型适配🤝：支持行政机关、事业单位、央企、国企、上市公司、民营企业等各类客户
- 智能状态识别🔍：提供意向阶段、争夺阶段、竞标阶段、废标重启、成果扩大等商机状态的针对性建议
- 结构化输出📑：每个商机包含项目信息、证明材料、推断依据和营销方案，信息完整且可操作
## ⚙️ 环境配置
### 1️⃣ 创建虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活环境
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```
### 2️⃣ 安装依赖
```bash
pip install -r requirements.txt
```
### 3️⃣ 环境变量配置
为了使用大模型 API 服务，请按以下步骤配置环境变量：
步骤一：创建环境配置文件
```bash
# Windows
copy .env.example .env
# Linux/macOS
cp .env.example .env
```
步骤二：编辑配置文件
```bash
# Windows
notepad .env
# Linux/macOS
nano .env
```
步骤三：填写 API 配置
根据使用的大模型服务商，填写相应的 API 密钥和配置项。项目启动时会自动加载环境变量🔑。
## 🤖 大模型配置
本项目支持国内主流大模型，可通过环境变量灵活配置：
- 通义千问（Qwen）
- 智谱AI（ChatGLM）
- 字节跳动豆包（Doubao）
- 月之暗面（Moonshot）
- MiniMax
配置示例
- 通义千问
```bash
export QWEN_API_KEY="your_qwen_api_key"
export CURRENT_MODEL_TYPE="qwen"
export DEFAULT_MODEL="qwen-max"
```
- 智谱AI
```bash
export ZHIPU_API_KEY="your_zhipu_api_key"
export CURRENT_MODEL_TYPE="zhipu"
export DEFAULT_MODEL="glm-4"
```
- 月之暗面
```bash
export MOONSHOT_API_KEY="your_moonshot_api_key"
export CURRENT_MODEL_TYPE="moonshot"
export DEFAULT_MODEL="moonshot-v1-8k"
```
## 🚀 快速开始
### 方法一：测试脚本快速体验
```bash
# 运行测试套件查看示例结果
python -m pytest tests/ -v

# 或直接运行测试文件
python tests/test_skill.py
```
测试脚本包含多个预设场景，可立即查看分析效果👀。
### 方法二：交互式使用示例
```python
from main import OpportunityAnalysisInput, analyze_opportunities
import asyncio

# 创建输入参数
input_data = OpportunityAnalysisInput(
    construction_direction="市政工程",  # 建筑方向
    customer_type="国企",              # 客户类型
    business_status="意向阶段"          # 商机状态
)

# 异步执行分析
async def run_example():
    result = await analyze_opportunities(input_data)
    
    # 输出分析结果
    print(f"发现 {len(result.opportunities)} 个潜在商机:")
    for i, opportunity in enumerate(result.opportunities, 1):
        print(f"\n{i}. 公司名称: {opportunity.company_name}")
        print(f"   项目信息: {opportunity.project_info}")
        print(f"   证明信息: {opportunity.proof_info}")
        print(f"   推断信息: {opportunity.inferred_info}")
        print(f"   营销方案: {opportunity.marketing_plan}")

# 执行示例
asyncio.run(run_example())
```
### 方法三：自定义参数体验
您可以根据需求灵活调整以下参数组合：
- 建筑方向选项🏗️：结构工程、岩土工程、桥梁与隧道工程、道路与铁道工程、市政工程、水利工程、自定义方向（100字以内）
- 客户类型选项🏢：行政机关、事业单位、央企、国企、上市公司、民营企业、自定义类型（100字以内）
- 商机状态选项📈：意向阶段、争夺阶段、竞标阶段、废标重启、成果扩大、自定义状态（100字以内）
### 输入参数说明
- construction_direction（建筑方向）：可选值见上，支持100字以内自定义内容
- customer_type（客户类型）：可选值见上，支持100字以内自定义内容
- business_status（商机状态）：可选值见上，支持100字以内自定义内容
### 输出结果格式
返回包含 5 个商机信息 的结构化数据，每个商机包含以下字段：
- company_name：公司名称
- project_info：项目信息（50字以内）
- proof_info：证明信息（含网站公告、招标信息等，255字以内）
- inferred_info：推断的商机信息（255字以内）
- marketing_plan：营销方案（255字以内）
## 🛠️ 使用方法
- 直接运行测试
```bash
python tests/test_skill.py
# 或
python tests\ui_main.py
```
- 在项目中集成使用
```python
from main import OpportunityAnalysisInput, analyze_opportunities

input_data = OpportunityAnalysisInput(
    construction_direction="市政工程",
    customer_type="国企", 
    business_status="意向阶段"
)

result = await analyze_opportunities(input_data)

for opportunity in result.opportunities:
    print(f"公司名称: {opportunity.company_name}")
    print(f"项目信息: {opportunity.project_info}")
    # 其他字段处理...
```
## 📂 项目结构
```
cdconstructionop-agent-skill/
├── main.py                    # 项目主入口文件 🏁
├── config.json               # Agent Skill 配置文件 ⚙️
├── requirements.txt          # Python 依赖包列表 📦
├── .env.example             # 环境变量配置模板 📄
├── .env                     # 环境变量配置文件（需手动创建） 🔐
├── README.md                # 项目说明文档 📖
├── src/                     # 源代码目录 💻
│   ├── core.py              # 核心分析逻辑实现 🧠
│   ├── utils.py             # 工具模块（网络搜索、信息验证） 🔧
│   ├── model_config.py      # 大模型配置管理 ⚙️
│   ├── llm_client.py        # 大模型客户端（支持多平台） 🌐
│   └── env_loader.py        # 环境变量加载工具 🛠️
├── tests/                   # 测试代码目录 🧪
│   └── test_skill.py        # 功能测试文件 ✅
└── venv/                    # Python 虚拟环境目录 🐍
```
## 📋 依赖要求
- Python >= 3.7
- pydantic
- aiohttp
- httpx
## ⚠️ 重要注意事项
- 项目定位🎯：本项目为 AI Agent Skill 的标准结构实现，适用于快速原型开发
- API 依赖🔑：实际部署需配置有效的大模型 API 密钥以获得准确分析结果
- 数据真实性📌：文档中的网络链接仅为示例，实际应用需替换为真实信息源
- 结果验证🔍：商机分析结果仅供参考，重要决策建议进一步调研验证
- 版本兼容✅：请确保使用指定版本的 Python 和依赖包以保证功能正常
