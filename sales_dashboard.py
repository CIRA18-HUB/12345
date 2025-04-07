import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import re
import os

# 设置页面配置
st.set_page_config(
    page_title="销售数据分析仪表盘",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 定义深色主题的自定义CSS样式
st.markdown("""
<style>
    /* 深色主题 */
    :root {
        --dark-bg-primary: #1E1E28;
        --dark-bg-secondary: #2D2D3A;
        --dark-text-primary: #E5E6EB;
        --dark-text-secondary: #CCCCCC;
        --dark-border: #444444;
        --dark-accent-blue: #4A6FE3;
        --dark-accent-green: #2D8659;
        --dark-accent-red: #C9394A;
        --dark-accent-yellow: #D9A23B;
        --dark-accent-purple: #7E57C2;
    }

    body {
        background-color: var(--dark-bg-primary);
        color: var(--dark-text-primary);
    }

    /* 主标题 */
    .main-header {
        font-size: 1.8rem;
        color: var(--dark-text-primary);
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1.2rem;
        background-color: var(--dark-bg-secondary);
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
        letter-spacing: 0.02em;
        font-weight: 600;
    }

    /* 子标题 */
    .sub-header {
        font-size: 1.3rem;
        color: var(--dark-text-primary);
        padding-top: 1.2rem;
        padding-bottom: 0.8rem;
        margin-top: 1.2rem;
        border-bottom: 1px solid var(--dark-border);
        letter-spacing: 0.02em;
        font-weight: 500;
    }

    /* 卡片样式 */
    .card {
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
        padding: 1.2rem;
        margin-bottom: 1.2rem;
        background-color: var(--dark-bg-secondary);
        transition: transform 0.2s, box-shadow 0.2s;
        border: 1px solid var(--dark-border);
    }

    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    }

    /* 指标值样式 */
    .metric-value {
        font-size: 1.6rem;
        font-weight: 600;
        color: var(--dark-accent-blue);
        margin: 0.4rem 0;
        letter-spacing: 0.02em;
        line-height: 1.2;
    }

    .metric-label {
        font-size: 0.95rem;
        color: var(--dark-text-secondary);
        font-weight: 400;
        letter-spacing: 0.01em;
        margin-bottom: 0.2rem;
    }

    /* 高亮区域 */
    .highlight {
        background-color: rgba(74, 111, 227, 0.15);
        padding: 1.2rem;
        border-radius: 8px;
        margin: 1.2rem 0;
        border-left: 4px solid var(--dark-accent-blue);
    }

    /* 图表解释区域 */
    .chart-explanation {
        background-color: rgba(74, 111, 227, 0.15);
        padding: 0.9rem;
        border-radius: 6px;
        margin: 0.8rem 0 1.4rem 0;
        border-left: 3px solid var(--dark-accent-blue);
        font-size: 0.92rem;
        color: var(--dark-text-primary);
    }

    /* 商业洞察区域 */
    .business-insight {
        background-color: rgba(45, 134, 89, 0.15);
        padding: 0.9rem;
        border-radius: 6px;
        margin: 0.8rem 0;
        border-left: 3px solid var(--dark-accent-green);
        font-size: 0.92rem;
        color: var(--dark-text-primary);
    }

    /* 行动建议区域 */
    .action-tip {
        background-color: rgba(217, 162, 59, 0.15);
        padding: 0.9rem;
        border-radius: 6px;
        margin: 0.8rem 0 1.4rem 0;
        border-left: 3px solid var(--dark-accent-yellow);
        font-size: 0.92rem;
        color: var(--dark-text-primary);
    }

    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: var(--dark-bg-secondary);
        border-radius: 6px 6px 0 0;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 4px 4px 0 0;
        letter-spacing: 0.01em;
        font-size: 0.92rem;
        color: var(--dark-text-secondary);
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(74, 111, 227, 0.2);
        border-bottom: 2px solid var(--dark-accent-blue);
        color: var(--dark-accent-blue);
    }

    /* 展开器样式 */
    .stExpander {
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
        border: 1px solid var(--dark-border);
        background-color: var(--dark-bg-secondary);
    }

    /* 下载按钮区域 */
    .download-button {
        text-align: center;
        margin-top: 2rem;
    }

    /* 区域间距 */
    .section-gap {
        margin-top: 2.5rem;  /* 增加部分间距 */
        margin-bottom: 2rem;
    }

    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: var(--dark-bg-secondary);
        border-right: 1px solid var(--dark-border);
        padding: 1.5rem 1rem;
    }

    .sidebar-header {
        font-size: 1.1rem;
        color: var(--dark-text-primary);
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--dark-border);
        letter-spacing: 0.01em;
        font-weight: 500;
    }

    /* 图表容器样式 */
    .chart-container {
        background-color: var(--dark-bg-secondary);
        border-radius: 8px;
        padding: 1.2rem;
        margin: 1.2rem 0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
        border: 1px solid var(--dark-border);
    }

    /* 自定义按钮样式 */
    .feishu-button {
        background-color: var(--dark-accent-blue);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 4px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        transition: background-color 0.3s;
        border: none;
        cursor: pointer;
    }

    .feishu-button:hover {
        background-color: #3A58B7;
    }

    /* 修复表格样式 */
    div[data-testid="stTable"] {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid var(--dark-border);
        background-color: var(--dark-bg-secondary);
    }

    div[data-testid="stTable"] table {
        border-collapse: collapse;
        color: var(--dark-text-primary);
    }

    div[data-testid="stTable"] th {
        background-color: rgba(40, 40, 50, 0.95);
        color: var(--dark-text-primary);
        font-weight: 500;
        padding: 0.6rem 0.8rem;
        text-align: left;
        border-bottom: 1px solid var(--dark-border);
    }

    div[data-testid="stTable"] td {
        padding: 0.6rem 0.8rem;
        border-bottom: 1px solid var(--dark-border);
        color: var(--dark-text-secondary);
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown('<div class="main-header">2025Q1 销售数据分析仪表盘 | 新品上市追踪</div>', unsafe_allow_html=True)


# 格式化数值的函数
def format_yuan(value):
    if value >= 100000000:  # 亿元级别
        return f"{value / 100000000:.2f}亿元"
    elif value >= 10000:  # 万元级别
        return f"{value / 10000:.2f}万元"
    else:
        return f"{value:.2f}元"


# ==== 工具函数区 ====
def extract_packaging(product_name):
    """
    从产品名称中提取包装类型，使用正则表达式增强匹配能力

    参数:
    product_name (str): 产品名称

    返回:
    str: 包装类型分类
    """
    try:
        # 确保输入是字符串
        if not isinstance(product_name, str):
            return "其他"

        # 检查组合类型（优先级最高）
        if re.search(r'分享装袋装', product_name):
            return '分享装袋装'
        elif re.search(r'分享装盒装', product_name):
            return '分享装盒装'

        # 按包装大小分类（从大到小）
        elif re.search(r'随手包', product_name):
            return '随手包'
        elif re.search(r'迷你包', product_name):
            return '迷你包'
        elif re.search(r'分享装', product_name):
            return '分享装'

        # 按包装形式分类
        elif re.search(r'袋装', product_name):
            return '袋装'
        elif re.search(r'盒装', product_name):
            return '盒装'
        elif re.search(r'瓶装', product_name):
            return '瓶装'

        # 处理特殊规格
        kg_match = re.search(r'(\d+(?:\.\d+)?)\s*KG', product_name, re.IGNORECASE)
        if kg_match:
            weight = float(kg_match.group(1))
            if weight >= 1.5:
                return '大包装'
            return '散装'

        g_match = re.search(r'(\d+(?:\.\d+)?)\s*G', product_name)
        if g_match:
            weight = float(g_match.group(1))
            if weight <= 50:
                return '小包装'
            elif weight <= 100:
                return '中包装'
            else:
                return '大包装'

        # 默认分类
        return '其他'
    except Exception as e:
        print(f"提取包装类型时出错: {str(e)}, 产品名称: {product_name}")
        return '其他'  # 捕获任何异常并返回默认值


# ==== 数据加载函数 ====
@st.cache_data
def load_data(file_path=None):
    """
    从文件加载数据或使用示例数据，增强错误处理
    """
    # 如果提供了文件路径，从文件加载
    if file_path and os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)

            # 数据预处理
            # 确保所有必要的列都存在
            required_columns = ['客户简称', '所属区域', '发运月份', '申请人', '产品代码', '产品名称',
                                '订单类型', '单价（箱）', '数量（箱）']

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(f"文件缺少必要的列: {', '.join(missing_columns)}。使用示例数据进行演示。")
                return load_sample_data()

            # 计算销售额
            df['销售额'] = df['单价（箱）'] * df['数量（箱）']

            # 确保发运月份是日期类型
            try:
                df['发运月份'] = pd.to_datetime(df['发运月份'])
            except Exception as e:
                st.warning(f"转换日期格式时出错: {str(e)}。月份分析功能可能受影响。")

            # 确保所有的字符串列都是字符串类型
            for col in ['客户简称', '所属区域', '申请人', '产品代码', '产品名称', '订单类型']:
                df[col] = df[col].astype(str)

            # 添加简化产品名称列
            df['简化产品名称'] = df.apply(
                lambda row: get_simplified_product_name(row['产品代码'], row['产品名称']),
                axis=1
            )

            # 在这里一次性提取包装类型，避免后续重复处理
            df['包装类型'] = df['产品名称'].apply(extract_packaging)

            return df
        except Exception as e:
            st.error(f"文件加载失败: {str(e)}。使用示例数据进行演示。")
            return load_sample_data()
    else:
        # 没有文件路径或文件不存在，使用示例数据
        if file_path:
            st.warning(f"文件路径不存在: {file_path}。使用示例数据进行演示。")
        return load_sample_data()


# 增强的图表解释函数
def add_chart_explanation(explanation_text, insights_text=None, action_tips=None):
    """添加图表解释、商业洞察和行动建议"""
    st.markdown(f'<div class="chart-explanation">📊 <b>图表解读：</b> {explanation_text}</div>',
                unsafe_allow_html=True)

    if insights_text:
        st.markdown(f'<div class="business-insight">💡 <b>商业洞察：</b> {insights_text}</div>',
                    unsafe_allow_html=True)

    if action_tips:
        st.markdown(f'<div class="action-tip">🎯 <b>行动建议：</b> {action_tips}</div>',
                    unsafe_allow_html=True)


def configure_chart(fig, title, xaxis_title, yaxis_title, height=550, legend_title=None):
    """统一配置图表样式的函数，应用于所有图表以保持一致性"""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, family="Arial, sans-serif", color="#E5E6EB")
        ),
        xaxis=dict(
            title=dict(text=xaxis_title, font=dict(size=14, color="#E5E6EB")),
            tickfont=dict(size=12, color="#E5E6EB"),
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(70,70,70,0.3)'
        ),
        yaxis=dict(
            title=dict(text=yaxis_title, font=dict(size=14, color="#E5E6EB")),
            tickfont=dict(size=12, color="#E5E6EB"),
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(70,70,70,0.3)'
        ),
        legend=dict(
            font=dict(size=12, family="Arial, sans-serif", color="#E5E6EB"),
            title=dict(text=legend_title, font=dict(size=14, color="#E5E6EB")) if legend_title else None,
            orientation="h",
            yanchor="bottom",
            y=-0.30,  # 增大图例与图表的距离
            xanchor="center",
            x=0.5,
            bgcolor="rgba(40,40,40,0.8)"
        ),
        height=height,  # 增加默认高度
        margin=dict(t=80, b=120, l=80, r=60),  # 增加边距
        plot_bgcolor='rgba(30,30,40,0.95)',  # 深色背景
        paper_bgcolor='rgba(25,25,35,0.95)',  # 深色纸张背景
        font=dict(family="Arial, sans-serif", color="#E5E6EB"),  # 浅色文字
        hovermode="closest"
    )
    return fig


# 创建产品代码到简化产品名称的映射函数
def get_simplified_product_name(product_code, product_name):
    """
    从产品名称中提取简化产品名称，增强错误处理
    """
    try:
        # 确保输入是字符串类型
        if not isinstance(product_name, str):
            return str(product_code)  # 返回产品代码作为备选

        if '口力' in product_name:
            # 提取"口力"之后的产品类型
            name_parts = product_name.split('口力')
            if len(name_parts) > 1:
                name_part = name_parts[1]
                if '-' in name_part:
                    name_part = name_part.split('-')[0].strip()

                # 进一步简化，只保留主要部分（去掉规格和包装形式）
                for suffix in ['G分享装袋装', 'G盒装', 'G袋装', 'KG迷你包', 'KG随手包']:
                    if suffix in name_part:
                        name_part = name_part.split(suffix)[0]
                        break

                # 去掉可能的数字和单位
                simple_name = re.sub(r'\d+\w*\s*', '', name_part).strip()

                if simple_name:  # 确保简化名称不为空
                    return f"{simple_name} ({product_code})"

        # 如果无法提取或处理中出现错误，则返回产品代码
        return str(product_code)
    except Exception as e:
        # 捕获任何异常，确保函数始终返回一个字符串
        print(f"简化产品名称时出错: {e}，产品代码: {product_code}")
        return str(product_code)


# 创建示例数据（以防用户没有上传文件）
@st.cache_data
def load_sample_data():
    """
    创建示例数据，确保所有列表长度一致
    """
    # 产品代码
    product_codes = [
        'F3415D', 'F3421D', 'F0104J', 'F0104L', 'F3411A', 'F01E4B',
        'F01L4C', 'F01C2P', 'F01E6D', 'F3450B', 'F3415B', 'F0110C',
        'F0183F', 'F01K8A', 'F0183K', 'F0101P'
    ]

    # 产品名称，确保与产品代码数量一致
    product_names = [
        '口力酸小虫250G分享装袋装-中国', '口力可乐瓶250G分享装袋装-中国',
        '口力比萨XXL45G盒装-中国', '口力比萨68G袋装-中国', '口力午餐袋77G袋装-中国',
        '口力汉堡108G袋装-中国', '口力扭扭虫2KG迷你包-中国', '口力字节软糖2KG迷你包-中国',
        '口力西瓜1.5KG随手包-中国', '口力七彩熊1.5KG随手包-中国',
        '口力软糖新品A-中国', '口力软糖新品B-中国', '口力软糖新品C-中国', '口力软糖新品D-中国',
        '口力软糖新品E-中国', '口力软糖新品F-中国'
    ]

    # 客户简称，确保长度一致
    customers = ['广州佳成行', '广州佳成行', '广州佳成行', '广州佳成行', '广州佳成行',
                 '广州佳成行', '河南甜丰號', '河南甜丰號', '河南甜丰號', '河南甜丰號',
                 '河南甜丰號', '广州佳成行', '河南甜丰號', '广州佳成行', '河南甜丰號',
                 '广州佳成行']

    try:
        # 创建简化版示例数据，添加更多变化性
        data = {
            '客户简称': customers,
            '所属区域': ['东', '东', '东', '东', '东', '东', '中', '中', '中', '中', '中',
                         '南', '中', '北', '北', '西'],
            '发运月份': ['2025-03', '2025-03', '2025-03', '2025-03', '2025-03', '2025-03',
                         '2025-03', '2025-03', '2025-03', '2025-03', '2025-03', '2025-03',
                         '2025-03', '2025-03', '2025-03', '2025-03'],
            '申请人': ['梁洪泽', '梁洪泽', '梁洪泽', '梁洪泽', '梁洪泽', '梁洪泽',
                       '胡斌', '胡斌', '胡斌', '胡斌', '胡斌', '梁洪泽', '胡斌', '梁洪泽',
                       '胡斌', '梁洪泽'],
            '产品代码': product_codes,
            '产品名称': product_names,
            '订单类型': ['订单-正常产品'] * 16,
            '单价（箱）': [121.44, 121.44, 216.96, 126.72, 137.04, 137.04, 127.2, 127.2,
                         180, 180, 180, 150, 160, 170, 180, 190],
            '数量（箱）': [10, 10, 20, 50, 252, 204, 7, 2, 6, 6, 6, 30, 20, 15, 10, 5]
        }

        # 创建DataFrame
        df = pd.DataFrame(data)

        # 计算销售额
        df['销售额'] = df['单价（箱）'] * df['数量（箱）']

        # 增加销售额的变化性，避免所有区域都有相同的销售额
        # 通过groupby后乘以不同的随机因子来实现
        region_factors = {'东': 5.2, '南': 3.8, '中': 0.9, '北': 1.6, '西': 1.3}

        # 应用区域因子
        for region, factor in region_factors.items():
            mask = df['所属区域'] == region
            df.loc[mask, '销售额'] = df.loc[mask, '销售额'] * factor

        # 添加简化产品名称
        df['简化产品名称'] = df.apply(
            lambda row: get_simplified_product_name(row['产品代码'], row['产品名称']),
            axis=1
        )

        # 添加包装类型
        df['包装类型'] = df['产品名称'].apply(extract_packaging)

        return df
    except Exception as e:
        # 如果示例数据创建失败，创建一个最小化的DataFrame
        st.error(f"创建示例数据时出错: {str(e)}。使用简化版示例数据。")

        # 创建最简单的数据集
        simple_df = pd.DataFrame({
            '客户简称': ['示例客户A', '示例客户B', '示例客户C'],
            '所属区域': ['东', '南', '中'],
            '发运月份': ['2025-03', '2025-03', '2025-03'],
            '申请人': ['示例申请人A', '示例申请人B', '示例申请人C'],
            '产品代码': ['X001', 'X002', 'X003'],
            '产品名称': ['示例产品A', '示例产品B', '示例产品C'],
            '订单类型': ['订单-正常产品'] * 3,
            '单价（箱）': [100, 150, 200],
            '数量（箱）': [10, 15, 20],
            '销售额': [1000, 2250, 4000],
            '简化产品名称': ['产品A (X001)', '产品B (X002)', '产品C (X003)'],
            '包装类型': ['盒装', '袋装', '盒装']
        })

        return simple_df


# 定义默认文件路径
DEFAULT_FILE_PATH = "Q1xlsx.xlsx"

# 侧边栏 - 上传文件区域
st.sidebar.markdown('<div class="sidebar-header">📂 数据导入</div>', unsafe_allow_html=True)
use_default_file = st.sidebar.checkbox("使用默认文件", value=True, help="使用指定的本地文件路径")
uploaded_file = st.sidebar.file_uploader("或上传Excel销售数据文件", type=["xlsx", "xls"], disabled=use_default_file)

# 加载数据
if use_default_file:
    # 使用默认文件路径
    if os.path.exists(DEFAULT_FILE_PATH):
        df = load_data(DEFAULT_FILE_PATH)
        st.sidebar.success(f"已成功加载默认文件: {DEFAULT_FILE_PATH}")
    else:
        st.sidebar.error(f"默认文件路径不存在: {DEFAULT_FILE_PATH}")
        df = load_sample_data()
        st.sidebar.info("正在使用示例数据。请上传您的数据文件获取真实分析。")
elif uploaded_file is not None:
    # 使用上传的文件
    df = load_data(uploaded_file)
else:
    # 没有文件，使用示例数据
    df = load_sample_data()
    st.sidebar.info("正在使用示例数据。请上传您的数据文件获取真实分析。")

# 定义新品产品代码
new_products = ['F0110C', 'F0183F', 'F01K8A', 'F0183K', 'F0101P']
new_products_df = df[df['产品代码'].isin(new_products)]

# 创建产品代码到简化名称的映射字典（用于图表显示）
product_name_mapping = {
    code: df[df['产品代码'] == code]['简化产品名称'].iloc[0] if len(df[df['产品代码'] == code]) > 0 else code
    for code in df['产品代码'].unique()
}

# 侧边栏 - 筛选器
st.sidebar.markdown('<div class="sidebar-header">🔍 筛选数据</div>', unsafe_allow_html=True)

# 区域筛选器
all_regions = sorted(df['所属区域'].astype(str).unique())
selected_regions = st.sidebar.multiselect("选择区域", all_regions, default=all_regions)

# 客户筛选器
all_customers = sorted(df['客户简称'].astype(str).unique())
selected_customers = st.sidebar.multiselect("选择客户", all_customers, default=[])

# 产品代码筛选器
all_products = sorted(df['产品代码'].astype(str).unique())
product_options = [(code, product_name_mapping[code]) for code in all_products]
selected_products = st.sidebar.multiselect(
    "选择产品",
    options=all_products,
    format_func=lambda x: f"{x} ({product_name_mapping[x]})",
    default=[]
)

# 申请人筛选器
all_applicants = sorted(df['申请人'].astype(str).unique())
selected_applicants = st.sidebar.multiselect("选择申请人", all_applicants, default=[])

# 应用筛选条件
filtered_df = df.copy()

if selected_regions:
    filtered_df = filtered_df[filtered_df['所属区域'].isin(selected_regions)]

if selected_customers:
    filtered_df = filtered_df[filtered_df['客户简称'].isin(selected_customers)]

if selected_products:
    filtered_df = filtered_df[filtered_df['产品代码'].isin(selected_products)]

if selected_applicants:
    filtered_df = filtered_df[filtered_df['申请人'].isin(selected_applicants)]

# 根据筛选后的数据筛选新品数据
filtered_new_products_df = filtered_df[filtered_df['产品代码'].isin(new_products)]

# 导航栏
st.markdown('<div class="sub-header">📱 导航</div>', unsafe_allow_html=True)
tabs = st.tabs(["📊 销售概览", "🆕 新品分析", "👥 客户细分", "🔄 产品组合", "🌐 市场渗透率"])

with tabs[0]:  # 销售概览
    # KPI指标行
    st.markdown('<div class="sub-header"> 🔑 关键绩效指标</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_sales = filtered_df['销售额'].sum()
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">总销售额</div>
            <div class="metric-value">{format_yuan(total_sales)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        total_customers = filtered_df['客户简称'].nunique()
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">客户数量</div>
            <div class="metric-value">{total_customers}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        total_products = filtered_df['产品代码'].nunique()
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">产品数量</div>
            <div class="metric-value">{total_products}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        avg_price = filtered_df['单价（箱）'].mean()
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">平均单价</div>
            <div class="metric-value">{avg_price:.2f}元</div>
        </div>
        """, unsafe_allow_html=True)

    # 区域销售分析
    st.markdown('<div class="sub-header section-gap"> 📊 区域销售分析</div>', unsafe_allow_html=True)

    # 计算区域销售数据
    region_sales = filtered_df.groupby('所属区域')['销售额'].sum().reset_index()
    region_sales = region_sales.sort_values(by='销售额', ascending=False)

    # 创建子图布局
    fig_region_combined = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "bar"}, {"type": "pie"}]],
        subplot_titles=("各区域销售额", "各区域销售占比"),
        column_widths=[0.6, 0.4],
        horizontal_spacing=0.15  # 增加水平间距
    )

    # 添加柱状图数据
    colors = px.colors.sequential.Plasma  # 使用深色系配色
    for i, row in region_sales.iterrows():
        region = row['所属区域']
        sales = row['销售额']
        color_idx = i % len(colors)

        fig_region_combined.add_trace(
            go.Bar(
                x=[region],
                y=[sales],
                name=region,
                marker_color=colors[color_idx],
                text=[f"{format_yuan(sales)}"],
                textposition='outside',
                textfont=dict(size=12, color="#FFFFFF"),  # 文字改为白色
                hovertemplate='<b>%{x}区域</b><br>销售额: %{text}<extra></extra>',
                showlegend=False
            ),
            row=1, col=1
        )

    # 添加饼图数据
    fig_region_combined.add_trace(
        go.Pie(
            labels=region_sales['所属区域'],
            values=region_sales['销售额'],
            hole=0.4,
            textinfo='percent+label',
            textfont=dict(size=12, color="#FFFFFF"),  # 文字改为白色
            marker=dict(colors=colors[:len(region_sales)]),
            hovertemplate='<b>%{label}区域</b><br>销售额占比: %{percent}<extra></extra>',
            showlegend=False
        ),
        row=1, col=2
    )

    # 更新布局
    fig_region_combined.update_layout(
        title_text="区域销售分析",
        title_font=dict(size=16, color="#E5E6EB"),
        height=550,  # 增加高度
        margin=dict(t=90, b=100, l=70, r=70),  # 增加边距
        plot_bgcolor='rgba(30,30,40,0.95)',  # 深色背景
        paper_bgcolor='rgba(25,25,35,0.95)'  # 深色纸张背景
    )

    # 更新柱状图Y轴
    fig_region_combined.update_yaxes(
        title_text="销售额 (元)",
        title_font=dict(size=14, color="#E5E6EB"),
        tickfont=dict(size=12, color="#E5E6EB"),
        range=[0, region_sales['销售额'].max() * 1.4],  # 增加空间
        tickformat=',',
        row=1, col=1,
        gridcolor='rgba(70,70,70,0.3)'  # 深色网格线
    )

    # 更新子图标题颜色
    fig_region_combined.update_annotations(font=dict(size=14, color="#E5E6EB"))

    # 显示图表
    st.plotly_chart(fig_region_combined, use_container_width=True, config={'displayModeBar': False})

    # 添加图表解释
    add_chart_explanation(
        "此图表左侧展示各区域销售额数值对比，右侧展示各区域在总销售中的占比。柱子/扇形越大表示销售额/占比越高。",
        "从图表可以看出，销售分布在区域间存在显著差异，这可能与区域市场规模、消费习惯或销售资源配置有关。",
        "重点关注销售占比最大的区域，分析其成功因素；针对销售额较低的区域，考虑增加资源投入或开展针对性营销活动。对比区域销售额与区域客户数量，评估单客户价值情况。"
    )

    # 产品销售分析 - 深色系优化版
    st.markdown('<div class="sub-header section-gap"> 📦 产品销售与包装分析</div>', unsafe_allow_html=True)

    # 创建产品分析组合图表
    fig_product_analysis = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "bar"}, {"type": "scatter"}]],
        subplot_titles=("不同包装类型销售额", "产品价格-销量关系"),
        column_widths=[0.5, 0.5],
        horizontal_spacing=0.15  # 增加间距
    )

    # 提取包装类型数据
    packaging_sales = filtered_df.groupby('包装类型')['销售额'].sum().reset_index()
    packaging_sales = packaging_sales.sort_values(by='销售额', ascending=False)

    # 添加包装类型柱状图
    colors = px.colors.sequential.Viridis  # 改用深色系配色
    for i, row in packaging_sales.iterrows():
        package_type = row['包装类型']
        sales = row['销售额']
        color_idx = i % len(colors)

        fig_product_analysis.add_trace(
            go.Bar(
                x=[package_type],
                y=[sales],
                name=package_type,
                marker_color=colors[color_idx],
                text=[f"{format_yuan(sales)}"],
                textposition='outside',
                textfont=dict(size=12, color="#FFFFFF"),  # 文字改为白色
                hovertemplate='<b>%{x}产品</b><br>销售额: %{text}<extra></extra>',
                showlegend=False
            ),
            row=1, col=1
        )

    # 区域颜色映射
    region_colors = {
        '东': '#8A2BE2',  # 深紫色
        '南': '#00688B',  # 深青色
        '西': '#8B4513',  # 深棕色
        '北': '#8B0000',  # 深红色
        '中': '#006400'  # 深绿色
    }

    # 添加价格-销量散点图（气泡图）
    for region in filtered_df['所属区域'].unique():
        region_data = filtered_df[filtered_df['所属区域'] == region]

        fig_product_analysis.add_trace(
            go.Scatter(
                x=region_data['单价（箱）'],
                y=region_data['数量（箱）'],
                mode='markers',
                name=region,
                marker=dict(
                    size=region_data['销售额'] / filtered_df['销售额'].max() * 25,
                    color=region_colors.get(region, '#4B0082'),  # 使用深色系映射
                    opacity=0.8,
                    line=dict(width=1, color="#CCCCCC")
                ),
                hovertemplate='<b>%{text}</b><br>单价：¥%{x:.2f}元<br>数量：%{y}箱<br>区域：' + region + '<extra></extra>',
                text=region_data['简化产品名称']
            ),
            row=1, col=2
        )

    # 更新布局
    fig_product_analysis.update_layout(
        height=580,  # 增加高度
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,  # 增大图例与图表的距离
            xanchor="center",
            x=0.75,
            font=dict(color="#E5E6EB"),
            bgcolor="rgba(40,40,40,0.8)"
        ),
        margin=dict(t=80, b=120, l=70, r=70),  # 增加边距
        plot_bgcolor='rgba(30,30,40,0.95)',  # 深色背景
        paper_bgcolor='rgba(25,25,35,0.95)'  # 深色纸张背景
    )

    # 更新Y轴
    fig_product_analysis.update_yaxes(
        title_text="销售额 (元)",
        title_font=dict(color="#E5E6EB"),
        tickfont=dict(color="#E5E6EB"),
        range=[0, packaging_sales['销售额'].max() * 1.3],
        tickformat=',',
        row=1, col=1,
        gridcolor='rgba(70,70,70,0.3)'  # 深色网格线
    )

    fig_product_analysis.update_yaxes(
        title_text="销售数量 (箱)",
        title_font=dict(color="#E5E6EB"),
        tickfont=dict(color="#E5E6EB"),
        row=1, col=2,
        gridcolor='rgba(70,70,70,0.3)'  # 深色网格线
    )

    # 更新X轴
    fig_product_analysis.update_xaxes(
        title_text="单价 (元/箱)",
        title_font=dict(color="#E5E6EB"),
        tickfont=dict(color="#E5E6EB"),
        tickprefix='¥',
        ticksuffix='元',
        separatethousands=True,
        row=1, col=2,
        gridcolor='rgba(70,70,70,0.3)'  # 深色网格线
    )

    # 更新子图标题颜色
    fig_product_analysis.update_annotations(font=dict(size=14, color="#E5E6EB"))

    st.plotly_chart(fig_product_analysis, use_container_width=True, config={'displayModeBar': False})

    # 添加图表解释
    add_chart_explanation(
        "左图展示不同包装类型产品的销售额对比，右图展示产品价格与销量的关系，气泡大小代表销售额，颜色代表销售区域。",
        "可以观察到：1）特定包装类型更受欢迎，影响销售表现；2）价格与销量之间存在一定的负相关关系，但因区域差异而有所不同；3）部分区域对高价产品的接受度更高。",
        "根据分析建议：1）重点投资生产和推广热销包装类型产品；2）对价格敏感型市场适当调整价格策略；3）针对高价产品销量好的区域，加大高利润产品的营销力度。"
    )

    # 申请人销售业绩分析 - 深色系优化版
    st.markdown('<div class="sub-header section-gap"> 👨‍💼 申请人销售业绩分析</div>', unsafe_allow_html=True)

    # 计算申请人业绩数据
    applicant_performance = filtered_df.groupby('申请人').agg({
        '销售额': 'sum',
        '客户简称': pd.Series.nunique,
        '产品代码': pd.Series.nunique
    }).reset_index()

    applicant_performance.columns = ['申请人', '销售额', '服务客户数', '销售产品种类数']
    applicant_performance = applicant_performance.sort_values('销售额', ascending=False)

    # 创建申请人业绩综合图表
    fig_applicant_performance = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "bar"}, {"type": "bar"}]],
        subplot_titles=("申请人销售额排名", "客户与产品覆盖情况"),
        column_widths=[0.5, 0.5],
        horizontal_spacing=0.18  # 增加水平间距
    )

    # 添加销售额柱状图
    colors_sales = px.colors.sequential.Inferno  # 使用深色系渐变色
    for i, row in applicant_performance.iterrows():
        color_idx = min(len(colors_sales) - 1, i + 3)  # 使用更深的颜色

        fig_applicant_performance.add_trace(
            go.Bar(
                x=[row['申请人']],
                y=[row['销售额']],
                name=row['申请人'],
                marker_color=colors_sales[color_idx],
                text=[f"{format_yuan(row['销售额'])}"],
                textposition='outside',
                textfont=dict(size=12, color="#FFFFFF"),  # 文字改为白色
                hovertemplate='<b>%{x}</b><br>销售额: %{text}<extra></extra>',
                showlegend=False
            ),
            row=1, col=1
        )

    # 添加客户和产品覆盖图
    applicant_coverage = applicant_performance.copy()

    # 为第二个子图准备数据
    customers_trace = go.Bar(
        x=applicant_coverage['申请人'],
        y=applicant_coverage['服务客户数'],
        name='服务客户数',
        marker_color='rgba(102, 51, 153, 0.85)',  # 深紫色
        text=applicant_coverage['服务客户数'],
        textposition='outside',
        textfont=dict(color="#FFFFFF"),  # 文字改为白色
        hovertemplate='<b>%{x}</b><br>服务客户数: %{y}<extra></extra>'
    )

    products_trace = go.Bar(
        x=applicant_coverage['申请人'],
        y=applicant_coverage['销售产品种类数'],
        name='销售产品种类数',
        marker_color='rgba(204, 0, 102, 0.85)',  # 深粉红色
        text=applicant_coverage['销售产品种类数'],
        textposition='outside',
        textfont=dict(color="#FFFFFF"),  # 文字改为白色
        hovertemplate='<b>%{x}</b><br>销售产品种类数: %{y}<extra></extra>'
    )

    # 添加客户和产品覆盖柱状图
    fig_applicant_performance.add_trace(customers_trace, row=1, col=2)
    fig_applicant_performance.add_trace(products_trace, row=1, col=2)

    # 更新布局
    fig_applicant_performance.update_layout(
        height=580,  # 增加高度
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.28,  # 增大图例与图表的距离
            xanchor="center",
            x=0.75,
            font=dict(size=12, color="#E5E6EB"),
            bgcolor="rgba(40,40,40,0.8)"
        ),
        margin=dict(t=80, b=130, l=70, r=70),  # 增加边距
        plot_bgcolor='rgba(30,30,40,0.95)',  # 深色背景
        paper_bgcolor='rgba(25,25,35,0.95)',  # 深色纸张背景
        barmode='group'
    )

    # 更新Y轴
    fig_applicant_performance.update_yaxes(
        title_text="销售额 (元)",
        title_font=dict(color="#E5E6EB"),
        tickfont=dict(color="#E5E6EB"),
        tickformat=',',
        range=[0, applicant_performance['销售额'].max() * 1.3],
        row=1, col=1,
        gridcolor='rgba(70,70,70,0.3)'  # 深色网格线
    )

    fig_applicant_performance.update_yaxes(
        title_text="数量",
        title_font=dict(color="#E5E6EB"),
        tickfont=dict(color="#E5E6EB"),
        range=[0, max(
            applicant_performance['服务客户数'].max(),
            applicant_performance['销售产品种类数'].max()
        ) * 1.4],  # 增加空间
        row=1, col=2,
        gridcolor='rgba(70,70,70,0.3)'  # 深色网格线
    )

    # 更新X轴
    fig_applicant_performance.update_xaxes(
        tickfont=dict(color="#E5E6EB"),
        row=1, col=1
    )

    fig_applicant_performance.update_xaxes(
        tickfont=dict(color="#E5E6EB"),
        row=1, col=2
    )

    # 更新子图标题颜色
    fig_applicant_performance.update_annotations(font=dict(size=14, color="#E5E6EB"))

    st.plotly_chart(fig_applicant_performance, use_container_width=True, config={'displayModeBar': False})

    # 添加图表解释
    add_chart_explanation(
        "左图展示各申请人的销售额排名，右图对比每位申请人覆盖的客户数量（蓝色）和销售的产品种类数（粉色）。",
        "通过分析可发现：1）销售业绩优秀的申请人通常拥有更广泛的客户覆盖或更多样化的产品组合；2）部分申请人专注于高价值客户，尽管客户数量少但销售额高；3）产品多样性与销售业绩有一定相关性。",
        "行动建议：1）向顶尖业绩申请人学习成功经验并在团队内分享；2）针对客户数多但销售额低的申请人，提供客户价值提升培训；3）鼓励产品多样化销售，设计交叉销售激励机制；4）针对不同申请人风格，制定个性化的业绩提升计划。"
    )

    # 原始数据表
    with st.expander("查看筛选后的原始数据"):
        st.dataframe(filtered_df)

with tabs[1]:  # 新品分析
    st.markdown('<div class="sub-header"> 🆕 新品销售分析</div>', unsafe_allow_html=True)

    # 新品KPI指标
    col1, col2, col3 = st.columns(3)

    with col1:
        new_products_sales = filtered_new_products_df['销售额'].sum()
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">新品销售额</div>
            <div class="metric-value">{format_yuan(new_products_sales)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        new_products_percentage = (new_products_sales / total_sales * 100) if total_sales > 0 else 0
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">新品销售占比</div>
            <div class="metric-value">{new_products_percentage:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        new_products_customers = filtered_new_products_df['客户简称'].nunique()
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">购买新品的客户数</div>
            <div class="metric-value">{new_products_customers}</div>
        </div>
        """, unsafe_allow_html=True)

    # 新品销售详情 - 深色系优化版
    st.markdown('<div class="sub-header section-gap">新品销售表现分析</div>', unsafe_allow_html=True)

    if not filtered_new_products_df.empty:
        # 创建新品销售综合分析图表
        # 计算新品销售数据
        product_sales = filtered_new_products_df.groupby(['产品代码', '简化产品名称'])['销售额'].sum().reset_index()
        product_sales = product_sales.sort_values('销售额', ascending=False)

        # 计算新品区域销售数据
        region_product_sales = filtered_new_products_df.groupby(['所属区域', '简化产品名称'])[
            '销售额'].sum().reset_index()

        # 创建子图
        fig_newproduct_analysis = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "bar"}, {"type": "bar"}]],
            subplot_titles=("各新品销售额对比", "各区域新品销售额"),
            column_widths=[0.5, 0.5],
            horizontal_spacing=0.15  # 增加间距
        )

        # 添加各新品销售额柱状图
        colors = px.colors.sequential.Magma  # 使用深色系配色
        for i, row in product_sales.iterrows():
            product = row['简化产品名称']
            sales = row['销售额']
            color_idx = i % len(colors)

            fig_newproduct_analysis.add_trace(
                go.Bar(
                    x=[product],
                    y=[sales],
                    name=product,
                    marker_color=colors[color_idx],
                    text=[f"{format_yuan(sales)}"],
                    textposition='outside',
                    textfont=dict(size=12, color="#FFFFFF"),  # 文字改为白色
                    showlegend=True
                ),
                row=1, col=1
            )

        # 添加各区域新品销售额堆叠柱状图
        for i, product in enumerate(product_sales['简化产品名称']):
            product_data = region_product_sales[region_product_sales['简化产品名称'] == product]
            color_idx = i % len(colors)

            if not product_data.empty:
                fig_newproduct_analysis.add_trace(
                    go.Bar(
                        x=product_data['所属区域'],
                        y=product_data['销售额'],
                        name=product,
                        marker_color=colors[color_idx],
                        showlegend=False
                    ),
                    row=1, col=2
                )

        # 更新布局
        fig_newproduct_analysis.update_layout(
            height=580,  # 增加高度
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.28,  # 增大图例与图表的距离
                xanchor="center",
                x=0.25,
                font=dict(size=12, color="#E5E6EB"),
                bgcolor="rgba(40,40,40,0.8)"
            ),
            margin=dict(t=80, b=140, l=70, r=70),  # 增加边距
            plot_bgcolor='rgba(30,30,40,0.95)',  # 深色背景
            paper_bgcolor='rgba(25,25,35,0.95)',  # 深色纸张背景
            barmode='stack'  # 第二个子图使用堆叠模式
        )

        # 更新Y轴
        fig_newproduct_analysis.update_yaxes(
            title_text="销售额 (元)",
            title_font=dict(color="#E5E6EB"),
            tickfont=dict(color="#E5E6EB"),
            tickformat=',',
            row=1, col=1,
            gridcolor='rgba(70,70,70,0.3)'  # 深色网格线
        )

        fig_newproduct_analysis.update_yaxes(
            title_text="销售额 (元)",
            title_font=dict(color="#E5E6EB"),
            tickfont=dict(color="#E5E6EB"),
            tickformat=',',
            row=1, col=2,
            gridcolor='rgba(70,70,70,0.3)'  # 深色网格线
        )

        # 更新X轴
        fig_newproduct_analysis.update_xaxes(
            tickfont=dict(color="#E5E6EB"),
            row=1, col=1
        )

        fig_newproduct_analysis.update_xaxes(
            tickfont=dict(color="#E5E6EB"),
            row=1, col=2
        )

        # 更新子图标题颜色
        fig_newproduct_analysis.update_annotations(font=dict(size=14, color="#E5E6EB"))

        st.plotly_chart(fig_newproduct_analysis, use_container_width=True, config={'displayModeBar': False})

        # 添加图表解释
        add_chart_explanation(
            "左图展示各新品销售额对比，右图展示不同区域对各新品的接受情况，堆叠柱状图显示了各区域对不同新品的销售额贡献。",
            "分析发现：1）新品间存在明显的销售差异，表明市场对不同新品的接受度不同；2）不同区域对新品有不同的偏好，这可能与区域消费习惯或营销力度有关；3）部分新品在特定区域表现突出。",
            "建议行动：1）针对表现最佳的新品加大生产和营销投入；2）针对表现不佳的新品，分析原因并调整产品特性或营销策略；3）根据区域偏好，制定差异化的新品推广策略；4）从表现最好的区域中提取经验，应用到其他区域。"
        )

        # 新品销售占比分析
        st.markdown('<div class="sub-header section-gap">新品销售占比分析</div>', unsafe_allow_html=True)

        # 创建新品占比分析图表
        fig_newproduct_ratio = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "pie"}, {"type": "bar"}]],
            subplot_titles=("新品与非新品销售占比", "各区域新品销售占比"),
            column_widths=[0.4, 0.6],
            horizontal_spacing=0.1
        )

        # 添加新品与非新品销售占比饼图
        fig_newproduct_ratio.add_trace(
            go.Pie(
                labels=['新品', '非新品'],
                values=[new_products_sales, total_sales - new_products_sales],
                hole=0.4,
                textinfo='percent+label',
                textfont=dict(size=12),
                marker=dict(colors=['#FF6B6B', '#4ECDC4']),
                hovertemplate='<b>%{label}</b><br>销售额占比: %{percent}<br>销售额: ¥%{value:,.2f}元<extra></extra>'
            ),
            row=1, col=1
        )

        # 计算各区域新品占比
        region_total_sales = filtered_df.groupby('所属区域')['销售额'].sum().reset_index()
        region_new_sales = filtered_new_products_df.groupby('所属区域')['销售额'].sum().reset_index()

        region_sales_ratio = pd.merge(region_total_sales, region_new_sales, on='所属区域', how='left',
                                      suffixes=('_total', '_new'))
        region_sales_ratio['new_ratio'] = region_sales_ratio['销售额_new'].fillna(0) / region_sales_ratio[
            '销售额_total'] * 100
        region_sales_ratio = region_sales_ratio.sort_values('new_ratio', ascending=False)

        # 添加各区域新品销售占比柱状图
        fig_newproduct_ratio.add_trace(
            go.Bar(
                x=region_sales_ratio['所属区域'],
                y=region_sales_ratio['new_ratio'],
                text=[f"{ratio:.2f}%" for ratio in region_sales_ratio['new_ratio']],
                textposition='outside',
                marker_color='#FF6B6B',
                hovertemplate='<b>%{x}区域</b><br>新品占比: %{text}<br>新品销售额: ¥%{customdata[0]:,.2f}元<br>总销售额: ¥%{customdata[1]:,.2f}元<extra></extra>',
                customdata=region_sales_ratio[['销售额_new', '销售额_total']].fillna(0).values
            ),
            row=1, col=2
        )

        # 更新布局
        fig_newproduct_ratio.update_layout(
            height=450,
            showlegend=False,
            margin=dict(t=80, b=80, l=60, r=60),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        # 更新Y轴
        fig_newproduct_ratio.update_yaxes(
            title_text="新品销售占比 (%)",
            range=[0, max(region_sales_ratio['new_ratio'].max() * 1.2, 5)],
            row=1, col=2
        )

        st.plotly_chart(fig_newproduct_ratio, use_container_width=True, config={'displayModeBar': False})

        # 添加图表解释
        add_chart_explanation(
            "左图展示新品销售在总销售中的占比，右图展示各区域的新品销售占比情况。",
            "从数据可见：1）新品总体占比为" + f"{new_products_percentage:.2f}%" + "，说明新品对业绩的贡献程度；2）各区域对新品的接受度不同，部分区域对新品接受程度明显更高；3）这种差异可能来自区域市场特性、推广力度或消费习惯。",
            "行动建议：1）评估新品占比是否达到预期目标，并据此调整新品推广策略；2）分析新品接受度高的区域成功经验，总结推广方法；3）针对新品占比低的区域，制定强化培训和营销方案；4）考虑根据区域市场特性调整新品组合。"
        )

    else:
        st.warning("当前筛选条件下没有新品数据。请调整筛选条件或确认数据中包含新品。")

    # 新品数据表
    with st.expander("查看新品销售数据"):
        if not filtered_new_products_df.empty:
            display_columns = [col for col in filtered_new_products_df.columns if
                               col != '产品代码' or col != '产品名称']
            st.dataframe(filtered_new_products_df[display_columns])
        else:
            st.info("当前筛选条件下没有新品数据。")

with tabs[2]:  # 客户细分
    st.markdown('<div class="sub-header"> 👥 客户细分分析</div>', unsafe_allow_html=True)

    if not filtered_df.empty:
        # 计算客户特征
        customer_features = filtered_df.groupby('客户简称').agg({
            '销售额': 'sum',  # 总销售额
            '产品代码': lambda x: len(set(x)),  # 购买的不同产品数量
            '数量（箱）': 'sum',  # 总购买数量
            '单价（箱）': 'mean'  # 平均单价
        }).reset_index()

        # 添加新品购买指标
        new_products_by_customer = filtered_new_products_df.groupby('客户简称')['销售额'].sum().reset_index()
        customer_features = customer_features.merge(new_products_by_customer, on='客户简称', how='left',
                                                    suffixes=('', '_新品'))
        customer_features['销售额_新品'] = customer_features['销售额_新品'].fillna(0)
        customer_features['新品占比'] = customer_features['销售额_新品'] / customer_features['销售额'] * 100

        # 简单客户分类
        customer_features['客户类型'] = pd.cut(
            customer_features['新品占比'],
            bins=[0, 10, 30, 100],
            labels=['保守型客户', '平衡型客户', '创新型客户']
        )

        # 添加客户类型解释
        st.markdown('<div class="highlight" style="margin-bottom: 20px;">', unsafe_allow_html=True)
        st.markdown("""
        <h3 style="font-size: 1.3rem; color: #3370FF; margin-bottom: 10px;">客户类型分类标准</h3>
        <p><strong>保守型客户</strong>：新品销售占比在0-10%之间，对新品接受度较低，倾向于购买成熟稳定的产品。</p>
        <p><strong>平衡型客户</strong>：新品销售占比在10-30%之间，对新品有一定接受度，同时保持对现有产品的购买。</p>
        <p><strong>创新型客户</strong>：新品销售占比在30-100%之间，积极尝试新品，是推广新产品的重要客户群体。</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 客户分类概览 - 优化版
        st.markdown('<div class="sub-header section-gap">客户类型分布与特征分析</div>', unsafe_allow_html=True)

        # 计算客户类型统计数据
        customer_segments = customer_features.groupby('客户类型').agg({
            '客户简称': 'count',
            '销售额': 'mean',
            '新品占比': 'mean'
        }).reset_index()

        customer_segments.columns = ['客户类型', '客户数量', '平均销售额', '平均新品占比']

        # 创建客户类型分析综合图表
        fig_customer_types = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "bar"}, {"type": "bar", "secondary_y": True}]],  # 正确设置第二Y轴
            subplot_titles=("客户类型分布", "客户类型特征对比"),
            column_widths=[0.4, 0.6],
            horizontal_spacing=0.1
        )

        # 添加客户类型分布柱状图
        colors = {
            '保守型客户': '#4ECDC4',
            '平衡型客户': '#FFD166',
            '创新型客户': '#FF6B6B'
        }

        for i, row in customer_segments.iterrows():
            customer_type = row['客户类型']
            count = row['客户数量']

            fig_customer_types.add_trace(
                go.Bar(
                    x=[customer_type],
                    y=[count],
                    name=customer_type,
                    marker_color=colors.get(customer_type, '#777'),
                    text=[count],
                    textposition='outside',
                    textfont=dict(size=12),
                    hovertemplate='<b>%{x}</b><br>客户数量: %{y}<extra></extra>',
                    showlegend=False
                ),
                row=1, col=1
            )

        # 添加客户类型特征对比柱状图
        # 1. 平均销售额柱状图
        fig_customer_types.add_trace(
            go.Bar(
                x=customer_segments['客户类型'],
                y=customer_segments['平均销售额'],
                name='平均销售额',
                marker_color='rgba(58, 71, 180, 0.7)',
                text=[f"{format_yuan(val)}" for val in customer_segments['平均销售额']],
                textposition='outside',
                textfont=dict(size=12),
                hovertemplate='<b>%{x}</b><br>平均销售额: %{text}<extra></extra>'
            ),
            row=1, col=2,
            secondary_y=False  # 使用主Y轴
        )

        # 计算平均新品占比对应的销售额值（为了在同一个图表上展示）
        max_sales = customer_segments['平均销售额'].max()
        ratio_scaled = customer_segments['平均新品占比'] * max_sales / 100

        # 2. 添加平均新品占比线图
        fig_customer_types.add_trace(
            go.Scatter(
                x=customer_segments['客户类型'],
                y=customer_segments['平均新品占比'],  # 直接使用原始的新品占比值
                name='平均新品占比',
                mode='lines+markers+text',
                line=dict(color='#FF6B6B', width=2),
                marker=dict(size=10, color='#FF6B6B'),
                text=[f"{val:.2f}%" for val in customer_segments['平均新品占比']],
                textposition='top center',
                textfont=dict(size=12),
                hovertemplate='<b>%{x}</b><br>平均新品占比: %{text}<extra></extra>'
            ),
            row=1, col=2,
            secondary_y=True  # 使用第二Y轴
        )

        # 更新布局
        fig_customer_types.update_layout(
            height=480,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.22,
                xanchor="center",
                x=0.75,
                font=dict(size=12)
            ),
            margin=dict(t=80, b=120, l=60, r=60),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        # 更新Y轴
        fig_customer_types.update_yaxes(
            title_text="客户数量",
            range=[0, customer_segments['客户数量'].max() * 1.2],
            row=1, col=1
        )

        # 主Y轴（销售额）
        fig_customer_types.update_yaxes(
            title_text="平均销售额 (元)",
            tickformat=',',
            range=[0, customer_segments['平均销售额'].max() * 1.3],
            secondary_y=False,
            row=1, col=2
        )

        # 第二Y轴（新品占比）
        fig_customer_types.update_yaxes(
            title_text="平均新品占比 (%)",
            titlefont=dict(color="#FF6B6B"),
            tickfont=dict(color="#FF6B6B"),
            range=[0, 100],
            secondary_y=True,
            row=1, col=2
        )

        st.plotly_chart(fig_customer_types, use_container_width=True, config={'displayModeBar': False})

        # 添加图表解释
        add_chart_explanation(
            "左图展示三种客户类型的分布情况，右图对比各类客户的平均销售额（柱状图）和平均新品占比（折线图）。",
            "从分析中发现：1）客户类型分布情况反映了市场对新品的总体接受度；2）不同类型客户的平均销售额差异显示了创新性与购买力的关系；3）平均新品占比的差异体现了客户创新接受程度的分层。",
            "建议行动：1）针对保守型客户群，开发渐进式的新品尝试激励方案；2）对平衡型客户，强化新品与经典产品的组合推荐；3）重视并奖励创新型客户的尝鲜行为，将其作为新品推广的种子用户；4）分析各类客户的区域分布特点，调整区域新品推广策略。"
        )

        # 客户销售额和新品占比散点图 - 优化版
        st.markdown('<div class="sub-header section-gap">客户销售额与新品占比关系</div>', unsafe_allow_html=True)

        # 创建改进的散点图
        fig_customer_scatter = px.scatter(
            customer_features,
            x='销售额',
            y='新品占比',
            color='客户类型',
            size='产品代码',  # 购买的产品种类数量
            hover_name='客户简称',
            title='客户销售额与新品占比关系',
            labels={
                '销售额': '销售额 (元)',
                '新品占比': '新品销售占比 (%)',
                '产品代码': '购买产品种类数',
                '客户类型': '客户类型'
            },
            color_discrete_map={
                '保守型客户': '#4ECDC4',
                '平衡型客户': '#FFD166',
                '创新型客户': '#FF6B6B'
            },
            height=500
        )

        # 改进散点图样式
        fig_customer_scatter.update_traces(
            marker=dict(
                opacity=0.7,
                line=dict(width=1, color='DarkSlateGrey')
            ),
            selector=dict(mode='markers')
        )

        # 添加垂直分割线（客户类型区域）
        fig_customer_scatter.add_shape(
            type="line",
            x0=customer_features['销售额'].min(),
            x1=customer_features['销售额'].max(),
            y0=10, y1=10,
            line=dict(color="#FFD166", width=1, dash="dash")
        )

        fig_customer_scatter.add_shape(
            type="line",
            x0=customer_features['销售额'].min(),
            x1=customer_features['销售额'].max(),
            y0=30, y1=30,
            line=dict(color="#FF6B6B", width=1, dash="dash")
        )

        # 添加区域标签
        fig_customer_scatter.add_annotation(
            x=customer_features['销售额'].max() * 0.95,
            y=5,
            text="保守型区域",
            showarrow=False,
            font=dict(color="#4ECDC4", size=12)
        )

        fig_customer_scatter.add_annotation(
            x=customer_features['销售额'].max() * 0.95,
            y=20,
            text="平衡型区域",
            showarrow=False,
            font=dict(color="#FFD166", size=12)
        )

        fig_customer_scatter.add_annotation(
            x=customer_features['销售额'].max() * 0.95,
            y=65,
            text="创新型区域",
            showarrow=False,
            font=dict(color="#FF6B6B", size=12)
        )

        # 更新坐标轴
        fig_customer_scatter.update_xaxes(
            title_text="销售额 (元)",
            showgrid=True,
            gridcolor='rgba(211,211,211,0.3)',
            tickprefix='¥',
            tickformat=',',
            separatethousands=True
        )

        fig_customer_scatter.update_yaxes(
            title_text="新品销售占比 (%)",
            showgrid=True,
            gridcolor='rgba(211,211,211,0.3)',
            range=[0, 100]
        )

        # 更新布局
        fig_customer_scatter.update_layout(
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=60, b=80, l=80, r=60),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(size=12)
            ),
            title=dict(font=dict(size=16))
        )

        st.plotly_chart(fig_customer_scatter, use_container_width=True, config={'displayModeBar': False})

        # 添加图表解释
        add_chart_explanation(
            "此散点图展示了客户销售额与新品占比之间的关系，气泡大小表示购买的产品种类数量，颜色表示客户类型（蓝色为保守型，黄色为平衡型，红色为创新型）。虚线区分了不同客户类型的区域。",
            "分析发现：1）高销售额客户分布在不同的新品接受度区间，说明销售表现与新品接受度没有必然关系；2）部分高销售额客户展现出较高的新品接受度，可作为重点推广目标；3）购买产品种类数（气泡大小）与新品占比有一定关联性。",
            "策略建议：1）识别图中右上方的高价值创新型客户，优先向其推广新品；2）关注右下方的高价值保守型客户，设计专门的渐进式新品导入方案；3）对中间区域的平衡型客户，通过组合销售提升新品比例；4）针对左上方的中小创新型客户，提供更多产品种类选择，扩大总体销售额。"
        )

        # 新品接受度最高的客户 - 优化版
        st.markdown('<div class="sub-header section-gap">新品接受度最高的客户</div>', unsafe_allow_html=True)

        # 选取新品占比最高的前10名客户
        top_acceptance = customer_features.sort_values('新品占比', ascending=False).head(10)

        # 创建高级条形图
        fig_top_acceptance = go.Figure()

        # 使用渐变色
        color_scale = px.colors.sequential.Reds

        # 为每个客户添加条形图，包含销售额信息
        for i, row in top_acceptance.iterrows():
            customer = row['客户简称']
            ratio = row['新品占比']
            sales = row['销售额']
            sales_new = row['销售额_新品']

            # 计算颜色索引 - 更深的红色表示更高的占比
            color_idx = min(len(color_scale) - 1, int(ratio / 100 * (len(color_scale) - 1) + 2))

            fig_top_acceptance.add_trace(go.Bar(
                x=[customer],
                y=[ratio],
                name=customer,
                marker_color=color_scale[color_idx],
                text=[f"{ratio:.2f}%"],
                textposition='outside',
                textfont=dict(size=12),
                hovertemplate='<b>%{x}</b><br>新品占比: %{text}<br>新品销售额: ¥%{customdata[0]:,.2f}元<br>总销售额: ¥%{customdata[1]:,.2f}元<extra></extra>',
                customdata=[[sales_new, sales]]
            ))

        # 更新布局
        fig_top_acceptance.update_layout(
            title='新品接受度最高的前10名客户',
            title_font=dict(size=16),
            xaxis_title=dict(text="客户", font=dict(size=14)),
            yaxis_title=dict(text="新品销售占比 (%)", font=dict(size=14)),
            xaxis_tickfont=dict(size=12),
            yaxis_tickfont=dict(size=12),
            margin=dict(t=60, b=80, l=80, r=60),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            barmode='group',
            showlegend=False,
            height=450
        )

        # 确保Y轴有足够空间显示数据标签并设置范围
        fig_top_acceptance.update_yaxes(
            range=[0, min(top_acceptance['新品占比'].max() * 1.2, 105)]
        )

        # 添加参考线
        fig_top_acceptance.add_shape(
            type="line",
            x0=-0.5,
            x1=len(top_acceptance) - 0.5,
            y0=30,
            y1=30,
            line=dict(color="#FF6B6B", width=1, dash="dash")
        )

        fig_top_acceptance.add_annotation(
            x=len(top_acceptance) - 1,
            y=32,
            text="创新型客户标准线 (30%)",
            showarrow=False,
            font=dict(color="#FF6B6B", size=11)
        )

        st.plotly_chart(fig_top_acceptance, use_container_width=True, config={'displayModeBar': False})

        # 添加图表解释
        add_chart_explanation(
            "此图表展示新品接受度最高的10名客户，按新品销售占比降序排列。条形颜色深浅表示新品占比高低，虚线表示创新型客户的标准线(30%)。",
            "从数据可见：1）这些客户新品占比明显高于平均水平，是新品推广的关键客户群体；2）部分客户新品占比接近或超过50%，表明对新品有极强的接受意愿；3）这些客户可能是趋势引领者或具有特殊的产品需求。",
            "策略建议：1）将这些高接受度客户作为新品首发测试的目标群体；2）深入调研这些客户的购买动机和满意度反馈；3）开发专属VIP新品尝鲜计划，增强其忠诚度；4）挖掘这些客户的共同特征，寻找类似的潜在客户群体扩大新品销售。"
        )

        # 客户表格
        with st.expander("查看客户细分数据表格"):
            # 美化数据表格
            display_columns = ['客户简称', '客户类型', '销售额', '销售额_新品', '新品占比', '产品代码', '数量（箱）',
                               '单价（箱）']
            display_df = customer_features[display_columns].copy()
            # 格式化数值列
            display_df['销售额'] = display_df['销售额'].apply(lambda x: f"¥{x:,.2f}")
            display_df['销售额_新品'] = display_df['销售额_新品'].apply(lambda x: f"¥{x:,.2f}")
            display_df['新品占比'] = display_df['新品占比'].apply(lambda x: f"{x:.2f}%")
            display_df['单价（箱）'] = display_df['单价（箱）'].apply(lambda x: f"¥{x:.2f}")

            # 重命名列以便更好显示
            display_df.columns = ['客户简称', '客户类型', '总销售额', '新品销售额', '新品占比',
                                  '购买产品种类数', '总购买数量(箱)', '平均单价(元/箱)']

            st.dataframe(display_df, use_container_width=True)
    else:
        st.warning("当前筛选条件下没有客户数据。请调整筛选条件。")

with tabs[3]:  # 产品组合
    st.markdown('<div class="sub-header"> 🔄 产品组合分析</div>', unsafe_allow_html=True)

    if not filtered_df.empty and len(filtered_df['客户简称'].unique()) > 1 and len(
            filtered_df['产品代码'].unique()) > 1:
        # 共现矩阵分析 - 介绍
        st.markdown('<div class="highlight" style="margin-bottom: 20px;">', unsafe_allow_html=True)
        st.markdown("""
        <h3 style="font-size: 1.3rem; color: #3370FF; margin-bottom: 10px;">共现分析说明</h3>
        <p>共现分析展示了不同产品被同一客户一起购买的频率，有助于发现产品间的关联性和互补关系。这一分析对于产品组合营销、交叉销售和货架陈列优化具有重要指导意义。</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 准备数据 - 创建交易矩阵
        transaction_data = filtered_df.groupby(['客户简称', '产品代码'])['销售额'].sum().unstack().fillna(0)
        # 转换为二进制格式（是否购买）
        transaction_binary = transaction_data.applymap(lambda x: 1 if x > 0 else 0)

        # 创建产品共现矩阵
        co_occurrence = pd.DataFrame(0, index=transaction_binary.columns, columns=transaction_binary.columns)

        # 创建产品代码到简化名称的映射
        name_mapping = {code: df[df['产品代码'] == code]['简化产品名称'].iloc[0]
        if len(df[df['产品代码'] == code]) > 0 else code
                        for code in transaction_binary.columns}

        # 计算共现次数
        for _, row in transaction_binary.iterrows():
            bought_products = row.index[row == 1].tolist()
            for p1 in bought_products:
                for p2 in bought_products:
                    if p1 != p2:
                        co_occurrence.loc[p1, p2] += 1

        # 筛选新品的共现情况
        valid_new_products = [p for p in new_products if p in co_occurrence.index]

        # 新品产品共现分析 - 优化版
        if valid_new_products:
            st.markdown('<div class="sub-header section-gap">新品产品共现分析</div>', unsafe_allow_html=True)

            # 创建整合后的共现数据
            top_co_products = []
            for np_code in valid_new_products:
                np_name = name_mapping.get(np_code, np_code)
                top_co = co_occurrence.loc[np_code].sort_values(ascending=False).head(5)  # 增加到前5名
                for product_code, count in top_co.items():
                    if count > 0 and product_code not in valid_new_products:  # 只添加有共现且非新品的产品
                        top_co_products.append({
                            '新品代码': np_code,
                            '新品名称': np_name,
                            '共现产品代码': product_code,
                            '共现产品名称': name_mapping.get(product_code, product_code),
                            '共现次数': count
                        })

            # 转换为DataFrame
            co_df = pd.DataFrame(top_co_products)

            if not co_df.empty:
                # 创建改进的共现分析图表
                fig_co_analysis = go.Figure()

                # 添加新品与共现产品的网络图
                # 由于共现分析内容较多，我们使用更直观的条形图

                # 按新品分组并排序，展示每个新品的前3个共现产品
                for new_product in co_df['新品名称'].unique():
                    product_data = co_df[co_df['新品名称'] == new_product].sort_values('共现次数',
                                                                                       ascending=False).head(3)

                    # 为每个新品创建独立的分组条形图
                    for i, row in product_data.iterrows():
                        fig_co_analysis.add_trace(go.Bar(
                            x=[row['新品名称']],
                            y=[row['共现次数']],
                            name=row['共现产品名称'],
                            text=[row['共现产品名称']],
                            textposition='auto',
                            hovertemplate='<b>%{x}</b> + <b>%{text}</b><br>共现次数: %{y}<extra></extra>'
                        ))

                # 更新布局
                fig_co_analysis.update_layout(
                    title="新品与热门产品共现关系 (前3名)",
                    title_font=dict(size=16),
                    xaxis_title=dict(text="新品名称", font=dict(size=14)),
                    yaxis_title=dict(text="共现次数", font=dict(size=14)),
                    legend_title=dict(text="共现产品", font=dict(size=14)),
                    xaxis_tickfont=dict(size=12),
                    yaxis_tickfont=dict(size=12),
                    barmode='group',
                    height=500,
                    margin=dict(t=80, b=100, l=60, r=60),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.22,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=12)
                    )
                )

                st.plotly_chart(fig_co_analysis, use_container_width=True, config={'displayModeBar': False})

                # 添加图表解释
                add_chart_explanation(
                    "此图表显示每种新品与哪些产品最经常被同一客户一起购买，横轴表示新品名称，纵轴表示共同购买的次数，颜色区分不同的共现产品。",
                    "共现次数高的产品组合通常表明这些产品之间可能有互补关系或被消费者认为适合一起购买。识别这些关系可帮助优化产品组合策略。",
                    "针对共现频率高的产品组合，考虑：1）在销售系统中设置关联推荐；2）开发组合促销方案；3）调整货架陈列，将共现产品放在相近位置；4）在营销材料中展示产品搭配使用的场景。"
                )

                # 热力图分析 - 优化版
                st.markdown('<div class="sub-header section-gap">产品共现热力图</div>', unsafe_allow_html=True)

                # 筛选主要产品以避免图表过于复杂
                important_products = set(valid_new_products)  # 确保包含所有新品

                # 热力图分析 - 优化版
                st.markdown('<div class="sub-header section-gap">产品共现热力图</div>', unsafe_allow_html=True)

                # 筛选主要产品以避免图表过于复杂
                important_products = set(valid_new_products)  # 确保包含所有新品

                # 添加与新品高度相关的产品
                for np_code in valid_new_products:
                    top_related = co_occurrence.loc[np_code].sort_values(ascending=False).head(3).index.tolist()
                    important_products.update(top_related)

                important_products = list(important_products)

                if len(important_products) > 2:  # 确保有足够的产品进行分析
                    # 创建简化名称映射的列表
                    important_product_names = [name_mapping.get(code, code) for code in important_products]

                    # 创建热力图数据
                    heatmap_data = co_occurrence.loc[important_products, important_products].copy()

                    # 对角线设为0（产品不与自身共现）
                    np.fill_diagonal(heatmap_data.values, 0)

                    # 创建热力图
                    fig_heatmap = px.imshow(
                        heatmap_data,
                        labels=dict(x="产品", y="产品", color="共现次数"),
                        x=important_product_names,
                        y=important_product_names,
                        color_continuous_scale="Blues",
                        title="主要产品共现热力图",
                        height=500
                    )

                    # 更新布局
                    fig_heatmap.update_layout(
                        margin=dict(t=80, b=80, l=100, r=80),
                        font=dict(size=12),
                        xaxis_tickangle=-45,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )

                    # 添加数值注释
                    for i in range(len(important_products)):
                        for j in range(len(important_products)):
                            if heatmap_data.iloc[i, j] > 0:  # 只显示非零值
                                fig_heatmap.add_annotation(
                                    x=j,
                                    y=i,
                                    text=f"{int(heatmap_data.iloc[i, j])}",
                                    showarrow=False,
                                    font=dict(
                                        color="white" if heatmap_data.iloc[
                                                             i, j] > heatmap_data.max().max() / 2 else "black",
                                        size=11
                                    )
                                )

                    st.plotly_chart(fig_heatmap, use_container_width=True, config={'displayModeBar': False})

                    # 添加图表解释
                    add_chart_explanation(
                        "此热力图展示了主要产品之间的共现关系，颜色越深表示两个产品一起购买的频率越高，数字显示具体共现次数。",
                        "通过热力图可迅速识别产品间的强关联性，深色方块代表高频共现的产品组合，这些组合在市场上受到客户的普遍欢迎。",
                        "营销策略建议：1）对高共现值（深色区域）的产品组合设计捆绑促销方案；2）对中等共现值（中等深度）的组合进行交叉推荐增强关联性；3）对理论上互补但共现值低（浅色区域）的产品组合，可以通过货架邻近摆放或组合营销提升销售协同效应。"
                    )
                else:
                    st.info("共现产品数量不足，无法生成有意义的热力图。请扩大数据范围。")
            else:
                st.warning("在当前筛选条件下，未发现新品有明显的共现关系。可能是新品购买量较少或共现样本不足。")

                # 产品购买模式分析 - 优化版
            st.markdown('<div class="sub-header section-gap">产品购买模式分析</div>', unsafe_allow_html=True)

            # 计算平均每单购买的产品种类数
            avg_products_per_order = transaction_binary.sum(axis=1).mean()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""
                            <div class="card">
                                <div class="metric-label">平均每客户购买产品种类</div>
                                <div class="metric-value">{avg_products_per_order:.2f}</div>
                            </div>
                            """, unsafe_allow_html=True)

            with col2:
                # 计算含有新品的订单比例
                orders_with_new_products = transaction_binary[valid_new_products].any(
                    axis=1).sum() if valid_new_products else 0
                total_orders = len(transaction_binary)
                percentage_orders_with_new = (orders_with_new_products / total_orders * 100) if total_orders > 0 else 0

                st.markdown(f"""
                            <div class="card">
                                <div class="metric-label">含新品的客户比例</div>
                                <div class="metric-value">{percentage_orders_with_new:.2f}%</div>
                            </div>
                            """, unsafe_allow_html=True)

            # 购买产品种类数分布 - 改进版
            products_per_order = transaction_binary.sum(axis=1).value_counts().sort_index().reset_index()
            products_per_order.columns = ['产品种类数', '客户数']

            # 创建优化的条形图
            fig_products_dist = px.bar(
                products_per_order,
                x='产品种类数',
                y='客户数',
                text='客户数',
                title='客户购买产品种类数分布',
                labels={'产品种类数': '购买产品种类数', '客户数': '客户数量'},
                color='客户数',
                color_continuous_scale='Blues',
                height=400
            )

            # 优化图表样式
            fig_products_dist.update_traces(
                textposition='outside',
                textfont=dict(size=12),
                marker_line_color='rgb(8,48,107)',
                marker_line_width=1,
                hovertemplate='<b>购买%{x}种产品</b><br>客户数量: %{y}<extra></extra>'
            )

            fig_products_dist.update_layout(
                xaxis=dict(
                    title=dict(text="购买产品种类数", font=dict(size=14)),
                    tickfont=dict(size=12),
                    dtick=1  # 强制X轴只显示整数
                ),
                yaxis=dict(
                    title=dict(text="客户数量", font=dict(size=14)),
                    tickfont=dict(size=12)
                ),
                coloraxis_showscale=False,
                margin=dict(t=60, b=80, l=80, r=60),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(fig_products_dist, use_container_width=True, config={'displayModeBar': False})

            # 添加购买模式图表解释
            add_chart_explanation(
                "此图表展示客户购买产品种类数的分布情况，横轴表示购买的不同产品种类数，纵轴表示对应的客户数量，柱高反映具有特定购买多样性特征的客户群体规模。",
                "通过分析可以发现客户购买行为的多样性特征：是倾向于集中购买少数几种固定产品，还是喜欢尝试多种产品组合。这种分布特征反映了市场细分需求的多元化程度。",
                "营销策略建议：1）针对单一产品购买客户，设计阶梯式交叉销售激励方案，引导其尝试相关产品；2）对购买2-3种产品的客户，提供组合优惠增强购买意愿；3）对多种类购买客户，开发更具个性化的产品套餐或忠诚度奖励计划；4）根据多样性购买行为的分布特征，调整产品系列规划和库存管理策略。"
            )

            # 添加产品组合总结
            st.markdown('<div class="highlight" style="margin-top: 30px;">', unsafe_allow_html=True)
            st.markdown("""
                        <h3 style="font-size: 1.3rem; color: #3370FF; margin-bottom: 10px;">产品组合分析总结</h3>
                        <p>产品组合分析揭示了产品间的关联性和客户购买模式，为交叉销售、组合营销和产品开发提供了重要依据。通过新品与现有产品的共现关系，可以制定更有效的新品推广策略；通过客户购买模式分析，可以优化产品组合和个性化营销方案。</p>
                        """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # 产品组合表格
            with st.expander("查看产品共现矩阵数据"):
                # 转换产品代码为简化名称
                display_co_occurrence = co_occurrence.copy()
                display_co_occurrence.index = [name_mapping.get(code, code) for code in display_co_occurrence.index]
                display_co_occurrence.columns = [name_mapping.get(code, code) for code in display_co_occurrence.columns]
                st.dataframe(display_co_occurrence, use_container_width=True)
        else:
            st.warning("当前筛选条件下的数据不足以进行产品组合分析。请确保有多个客户和产品。")

        with tabs[4]:  # 市场渗透率
            st.markdown('<div class="sub-header"> 🌐 新品市场渗透分析</div>', unsafe_allow_html=True)

            if not filtered_df.empty:
                # 计算总体渗透率
                total_customers = filtered_df['客户简称'].nunique()
                new_product_customers = filtered_new_products_df['客户简称'].nunique()
                penetration_rate = (new_product_customers / total_customers * 100) if total_customers > 0 else 0

                # KPI指标卡 - 飞书风格优化
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                            <div class="card">
                                <div class="metric-label">总客户数</div>
                                <div class="metric-value">{total_customers}</div>
                                <div style="font-size: 0.9rem; color: #646A73; margin-top: 5px;">市场覆盖基数</div>
                            </div>
                            """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                            <div class="card">
                                <div class="metric-label">购买新品的客户数</div>
                                <div class="metric-value">{new_product_customers}</div>
                                <div style="font-size: 0.9rem; color: #646A73; margin-top: 5px;">新品接受客户</div>
                            </div>
                            """, unsafe_allow_html=True)

                with col3:
                    # 添加渗透率变化指示图标
                    indicator = "↑" if penetration_rate > 20 else "↓"
                    indicator_color = "#36B37E" if penetration_rate > 20 else "#F5222D"

                    st.markdown(f"""
                            <div class="card">
                                <div class="metric-label">新品市场渗透率</div>
                                <div class="metric-value">{penetration_rate:.2f}% <span style="color: {indicator_color}; font-size: 1.2rem;">{indicator}</span></div>
                                <div style="font-size: 0.9rem; color: #646A73; margin-top: 5px;">行业基准: 20%</div>
                            </div>
                            """, unsafe_allow_html=True)

                # 渗透率综合分析 - 优化版
                st.markdown('<div class="sub-header section-gap">区域渗透率综合分析</div>', unsafe_allow_html=True)

                if 'selected_regions' in locals() and selected_regions:
                    # 创建渗透率分析综合图表

                    # 按区域计算渗透率
                    region_customers = filtered_df.groupby('所属区域')['客户简称'].nunique().reset_index()
                    region_customers.columns = ['所属区域', '客户总数']

                    new_region_customers = filtered_new_products_df.groupby('所属区域')[
                        '客户简称'].nunique().reset_index()
                    new_region_customers.columns = ['所属区域', '购买新品客户数']

                    region_penetration = region_customers.merge(new_region_customers, on='所属区域', how='left')
                    region_penetration['购买新品客户数'] = region_penetration['购买新品客户数'].fillna(0)
                    region_penetration['渗透率'] = region_penetration['购买新品客户数'] / region_penetration[
                        '客户总数'] * 100
                    region_penetration['渗透率'] = region_penetration['渗透率'].round(2)

                    # 计算每个区域的新品销售额
                    region_new_sales = filtered_new_products_df.groupby('所属区域')['销售额'].sum().reset_index()
                    region_new_sales.columns = ['所属区域', '新品销售额']

                    # 合并渗透率和销售额数据
                    region_analysis = region_penetration.merge(region_new_sales, on='所属区域', how='left')
                    region_analysis['新品销售额'] = region_analysis['新品销售额'].fillna(0)

                    # 创建子图
                    fig_penetration_combined = make_subplots(
                        rows=1, cols=2,
                        specs=[[{"type": "bar"}, {"type": "scatter"}]],
                        subplot_titles=("各区域新品渗透率", "渗透率与销售额关系"),
                        column_widths=[0.5, 0.5],
                        horizontal_spacing=0.12
                    )

                    # 添加渗透率柱状图
                    colors = px.colors.sequential.Bluyl
                    for i, row in region_penetration.iterrows():
                        region = row['所属区域']
                        penetration = row['渗透率']
                        color_idx = min(len(colors) - 1, int((penetration / 100) * len(colors)) + 2)

                        fig_penetration_combined.add_trace(
                            go.Bar(
                                x=[region],
                                y=[penetration],
                                name=region,
                                marker_color=colors[color_idx],
                                text=[f"{penetration:.2f}%"],
                                textposition='outside',
                                textfont=dict(size=12),
                                hovertemplate='<b>%{x}区域</b><br>渗透率: %{text}<br>购买新品客户数: ' +
                                              f"{int(row['购买新品客户数'])}" +
                                              '<br>客户总数: ' + f"{int(row['客户总数'])}" + '<extra></extra>',
                                showlegend=False
                            ),
                            row=1, col=1
                        )

                    # 添加渗透率-销售额散点图（气泡图）
                    for i, row in region_analysis.iterrows():
                        region = row['所属区域']
                        penetration = row['渗透率']
                        sales = row['新品销售额']
                        customers = row['客户总数']

                        fig_penetration_combined.add_trace(
                            go.Scatter(
                                x=[penetration],
                                y=[sales],
                                mode='markers+text',
                                name=region,
                                marker=dict(
                                    size=customers / region_analysis['客户总数'].max() * 30 + 15,
                                    color=colors[min(len(colors) - 1, int((penetration / 100) * len(colors)) + 2)],
                                    opacity=0.7,
                                    line=dict(width=1, color='DarkSlateGrey')
                                ),
                                text=[region],
                                textposition='middle center',
                                textfont=dict(size=10, color='white'),
                                hovertemplate='<b>%{text}区域</b><br>渗透率: ' + f"{penetration:.2f}%" +
                                              '<br>新品销售额: ¥' + f"{sales:,.2f}" + '元<br>客户总数: ' +
                                              f"{int(customers)}" + '<extra></extra>'
                            ),
                            row=1, col=2
                        )

                    # 添加参考线 - 平均渗透率
                    fig_penetration_combined.add_shape(
                        type="line",
                        x0=0,
                        x1=region_analysis['渗透率'].max() * 1.1,
                        y0=region_analysis['新品销售额'].mean(),
                        y1=region_analysis['新品销售额'].mean(),
                        line=dict(color="#FFD166", width=1, dash="dash"),
                        row=1, col=2
                    )

                    fig_penetration_combined.add_shape(
                        type="line",
                        x0=region_analysis['渗透率'].mean(),
                        x1=region_analysis['渗透率'].mean(),
                        y0=0,
                        y1=region_analysis['新品销售额'].max() * 1.1,
                        line=dict(color="#FFD166", width=1, dash="dash"),
                        row=1, col=2
                    )

                    # 添加象限标签
                    # 计算象限中心点
                    max_penetration = region_analysis['渗透率'].max() * 1.1
                    max_sales = region_analysis['新品销售额'].max() * 1.1
                    mean_penetration = region_analysis['渗透率'].mean()
                    mean_sales = region_analysis['新品销售额'].mean()

                    # 象限I - 高渗透率，高销售额
                    fig_penetration_combined.add_annotation(
                        x=(mean_penetration + max_penetration) / 2,
                        y=(mean_sales + max_sales) / 2,
                        text="明星区域",
                        showarrow=False,
                        font=dict(size=12, color="#36B37E"),
                        row=1, col=2
                    )

                    # 象限II - 低渗透率，高销售额
                    fig_penetration_combined.add_annotation(
                        x=mean_penetration / 2,
                        y=(mean_sales + max_sales) / 2,
                        text="潜力区域",
                        showarrow=False,
                        font=dict(size=12, color="#3370FF"),
                        row=1, col=2
                    )

                    # 象限III - 低渗透率，低销售额
                    fig_penetration_combined.add_annotation(
                        x=mean_penetration / 2,
                        y=mean_sales / 2,
                        text="待开发区域",
                        showarrow=False,
                        font=dict(size=12, color="#F5222D"),
                        row=1, col=2
                    )

                    # 象限IV - 高渗透率，低销售额
                    fig_penetration_combined.add_annotation(
                        x=(mean_penetration + max_penetration) / 2,
                        y=mean_sales / 2,
                        text="效率提升区域",
                        showarrow=False,
                        font=dict(size=12, color="#FAAD14"),
                        row=1, col=2
                    )

                    # 更新布局
                    fig_penetration_combined.update_layout(
                        height=500,
                        showlegend=False,
                        margin=dict(t=80, b=80, l=60, r=60),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )

                    # 更新Y轴
                    fig_penetration_combined.update_yaxes(
                        title_text="渗透率 (%)",
                        range=[0, region_penetration['渗透率'].max() * 1.2],
                        row=1, col=1
                    )

                    fig_penetration_combined.update_yaxes(
                        title_text="新品销售额 (元)",
                        tickformat=',',
                        range=[0, region_analysis['新品销售额'].max() * 1.1],
                        row=1, col=2
                    )

                    # 更新X轴
                    fig_penetration_combined.update_xaxes(
                        title_text="渗透率 (%)",
                        range=[0, region_analysis['渗透率'].max() * 1.1],
                        row=1, col=2
                    )

                    st.plotly_chart(fig_penetration_combined, use_container_width=True,
                                    config={'displayModeBar': False})

                    # 添加图表解释
                    add_chart_explanation(
                        "左图展示各区域的新品市场渗透率，即购买新品的客户占总客户的比例；右图是渗透率与销售额的关系分析，气泡大小代表客户数量，虚线表示平均值，将区域分为四个象限。",
                        "通过四象限分析可见：1）明星区域（右上）：渗透率高且销售额高，新品推广最成功的区域；2）潜力区域（左上）：渗透率低但销售额高，说明单客户价值高但客户覆盖面不足；3）待开发区域（左下）：渗透率低且销售额低，需全面提升的区域；4）效率提升区域（右下）：渗透率高但销售额低，客单价需提升。",
                        "区域策略建议：1）明星区域：总结成功经验并推广到其他区域；2）潜力区域：扩大客户覆盖面，增加尝试新品的客户数量；3）待开发区域：加强销售团队培训和营销活动投入；4）效率提升区域：提高客单价，鼓励客户增加新品购买量。"
                    )

                    # 渗透率月度趋势分析
                    if '发运月份' in filtered_df.columns and not filtered_df.empty:
                        st.markdown('<div class="sub-header section-gap">新品渗透率月度趋势</div>',
                                    unsafe_allow_html=True)

                        try:
                            # 确保日期类型正确
                            filtered_df['发运月份'] = pd.to_datetime(filtered_df['发运月份'])
                            filtered_new_products_df['发运月份'] = pd.to_datetime(filtered_new_products_df['发运月份'])

                            # 计算月度渗透率
                            monthly_customers = filtered_df.groupby(pd.Grouper(key='发运月份', freq='M'))[
                                '客户简称'].nunique().reset_index()
                            monthly_customers.columns = ['月份', '客户总数']

                            monthly_new_customers = \
                            filtered_new_products_df.groupby(pd.Grouper(key='发运月份', freq='M'))[
                                '客户简称'].nunique().reset_index()
                            monthly_new_customers.columns = ['月份', '购买新品客户数']

                            # 计算月度销售额
                            monthly_sales = filtered_df.groupby(pd.Grouper(key='发运月份', freq='M'))[
                                '销售额'].sum().reset_index()
                            monthly_sales.columns = ['月份', '销售额总计']

                            monthly_new_sales = filtered_new_products_df.groupby(pd.Grouper(key='发运月份', freq='M'))[
                                '销售额'].sum().reset_index()
                            monthly_new_sales.columns = ['月份', '新品销售额']

                            # 合并数据
                            monthly_data = monthly_customers.merge(monthly_new_customers, on='月份', how='left')
                            monthly_data = monthly_data.merge(monthly_sales, on='月份', how='left')
                            monthly_data = monthly_data.merge(monthly_new_sales, on='月份', how='left')

                            # 填充缺失值
                            monthly_data['购买新品客户数'] = monthly_data['购买新品客户数'].fillna(0)
                            monthly_data['新品销售额'] = monthly_data['新品销售额'].fillna(0)

                            # 计算渗透率和销售占比
                            monthly_data['渗透率'] = (
                                        monthly_data['购买新品客户数'] / monthly_data['客户总数'] * 100).round(2)
                            monthly_data['销售占比'] = (
                                        monthly_data['新品销售额'] / monthly_data['销售额总计'] * 100).round(2)

                            # 创建月度趋势图
                            fig_monthly_trend = make_subplots(
                                rows=1, cols=1,
                                specs=[[{"secondary_y": True}]],  # 设置双Y轴
                            )

                            # 添加渗透率线
                            fig_monthly_trend.add_trace(
                                go.Scatter(
                                    x=monthly_data['月份'],
                                    y=monthly_data['渗透率'],
                                    mode='lines+markers+text',
                                    name='新品渗透率',
                                    line=dict(color='#3370FF', width=3),
                                    marker=dict(size=10, color='#3370FF'),
                                    text=[f"{x:.1f}%" for x in monthly_data['渗透率']],
                                    textposition='top center',
                                    textfont=dict(size=12),
                                    hovertemplate='<b>%{x|%Y-%m}</b><br>渗透率: %{text}<br>购买新品客户数: %{customdata[0]}<br>客户总数: %{customdata[1]}<extra></extra>',
                                    customdata=monthly_data[['购买新品客户数', '客户总数']].astype(int).values
                                ),
                                secondary_y=False
                            )

                            # 添加销售占比线
                            fig_monthly_trend.add_trace(
                                go.Scatter(
                                    x=monthly_data['月份'],
                                    y=monthly_data['销售占比'],
                                    mode='lines+markers+text',
                                    name='新品销售占比',
                                    line=dict(color='#FF6B6B', width=3, dash='dot'),
                                    marker=dict(size=10, color='#FF6B6B'),
                                    text=[f"{x:.1f}%" for x in monthly_data['销售占比']],
                                    textposition='bottom center',
                                    textfont=dict(size=12),
                                    hovertemplate='<b>%{x|%Y-%m}</b><br>销售占比: %{text}<br>新品销售额: ¥%{customdata[0]:,.2f}<br>总销售额: ¥%{customdata[1]:,.2f}<extra></extra>',
                                    customdata=monthly_data[['新品销售额', '销售额总计']].values
                                ),
                                secondary_y=True
                            )

                            # 更新布局
                            fig_monthly_trend.update_layout(
                                title="新品渗透率与销售占比月度趋势",
                                title_font=dict(size=16),
                                height=450,
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=-0.2,
                                    xanchor="center",
                                    x=0.5,
                                    font=dict(size=12)
                                ),
                                margin=dict(t=80, b=100, l=60, r=60),
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                hovermode="x unified"
                            )

                            # 更新X轴
                            fig_monthly_trend.update_xaxes(
                                title_text="月份",
                                tickformat='%Y-%m',
                                gridcolor='rgba(211,211,211,0.3)'
                            )

                            # 更新主Y轴（渗透率）
                            fig_monthly_trend.update_yaxes(
                                title_text="新品渗透率 (%)",
                                range=[0, max(monthly_data['渗透率'].max() * 1.2, 5)],
                                gridcolor='rgba(211,211,211,0.3)',
                                secondary_y=False
                            )

                            # 更新次Y轴（销售占比）
                            fig_monthly_trend.update_yaxes(
                                title_text="新品销售占比 (%)",
                                range=[0, max(monthly_data['销售占比'].max() * 1.2, 5)],
                                gridcolor='rgba(211,211,211,0.3)',
                                secondary_y=True
                            )

                            st.plotly_chart(fig_monthly_trend, use_container_width=True,
                                            config={'displayModeBar': False})

                            # 添加图表解释
                            add_chart_explanation(
                                "此图表展示新品渗透率（蓝色实线）和新品销售占比（红色虚线）的月度变化趋势，帮助识别新品市场表现的动态变化。",
                                "通过趋势分析可观察到：1）渗透率与销售占比的变化趋势是否一致，反映客户数量与销售额的协同性；2）月度波动反映了季节性因素或营销活动的影响；3）趋势线的方向揭示了新品市场接受度的整体发展态势。",
                                "基于趋势分析的建议：1）识别渗透率峰值月份，分析成功因素并在类似时机复制；2）针对渗透率低谷期，制定特别促销或客户激活计划；3）当渗透率上升但销售占比下降时，关注客单价提升；4）当整体呈下降趋势时，考虑产品创新或营销策略调整。"
                            )

                        except Exception as e:
                            st.warning(f"无法处理月度渗透率分析。错误：{str(e)}")

                    # 添加渗透率分析总结
                    st.markdown('<div class="highlight" style="margin-top: 30px;">', unsafe_allow_html=True)
                    st.markdown(f"""
                            <h3 style="font-size: 1.3rem; color: #3370FF; margin-bottom: 10px;">新品渗透分析总结</h3>
                            <p>当前新品整体市场渗透率为<strong>{penetration_rate:.2f}%</strong>，即在所有{total_customers}名客户中，有{new_product_customers}名客户购买了新品。通过区域渗透率分析和月度趋势观察，可识别渗透表现最佳的区域和时段，为后续新品推广策略制定提供数据支持。</p>
                            """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("请在侧边栏选择至少一个区域以查看区域渗透率分析。")
            else:
                st.warning("当前筛选条件下没有数据。请调整筛选条件。")

        # 底部下载区域
        st.markdown("---")
        st.markdown('<div class="sub-header"> 📊 导出分析结果</div>', unsafe_allow_html=True)


        # 创建Excel报告
        @st.cache_data
        def generate_excel_report(df, new_products_df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')

            # 工作簿设置
            workbook = writer.book

            # 创建标题格式
            header_format = workbook.add_format({
                'bold': True,
                'font_color': '#FFFFFF',
                'bg_color': '#3370FF',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })

            # 创建数字格式
            number_format = workbook.add_format({
                'num_format': '#,##0.00',
                'border': 1
            })

            # 创建百分比格式
            percent_format = workbook.add_format({
                'num_format': '0.00%',
                'border': 1
            })

            # 创建文本格式
            text_format = workbook.add_format({
                'border': 1
            })

            # 销售概览表
            df.to_excel(writer, sheet_name='销售数据总览', index=False)
            sales_sheet = writer.sheets['销售数据总览']

            # 格式化标题行
            for col_num, value in enumerate(df.columns.values):
                sales_sheet.write(0, col_num, value, header_format)

            # 设置列宽
            sales_sheet.set_column('A:Z', 15)

            # 新品分析表
            new_products_df.to_excel(writer, sheet_name='新品销售数据', index=False)
            new_sheet = writer.sheets['新品销售数据']

            # 格式化标题行
            for col_num, value in enumerate(new_products_df.columns.values):
                new_sheet.write(0, col_num, value, header_format)

            # 设置列宽
            new_sheet.set_column('A:Z', 15)

            # 区域销售汇总
            region_summary = df.groupby('所属区域').agg({
                '销售额': 'sum',
                '客户简称': pd.Series.nunique,
                '产品代码': pd.Series.nunique,
                '数量（箱）': 'sum'
            }).reset_index()
            region_summary.columns = ['区域', '销售额', '客户数', '产品数', '销售数量']

            region_summary.to_excel(writer, sheet_name='区域销售汇总', index=False)
            region_sheet = writer.sheets['区域销售汇总']

            # 格式化标题行
            for col_num, value in enumerate(region_summary.columns.values):
                region_sheet.write(0, col_num, value, header_format)

            # 应用数字格式
            for row_num in range(1, len(region_summary) + 1):
                region_sheet.write(row_num, 1, region_summary.iloc[row_num - 1, 1], number_format)  # 销售额
                region_sheet.write(row_num, 4, region_summary.iloc[row_num - 1, 4], number_format)  # 销售数量

            # 设置列宽
            region_sheet.set_column('A:E', 15)

            # 产品销售汇总
            product_summary = df.groupby(['产品代码', '简化产品名称']).agg({
                '销售额': 'sum',
                '客户简称': pd.Series.nunique,
                '数量（箱）': 'sum'
            }).sort_values('销售额', ascending=False).reset_index()
            product_summary.columns = ['产品代码', '产品名称', '销售额', '购买客户数', '销售数量']

            product_summary.to_excel(writer, sheet_name='产品销售汇总', index=False)
            product_sheet = writer.sheets['产品销售汇总']

            # 格式化标题行
            for col_num, value in enumerate(product_summary.columns.values):
                product_sheet.write(0, col_num, value, header_format)

            # 应用数字格式
            for row_num in range(1, len(product_summary) + 1):
                product_sheet.write(row_num, 2, product_summary.iloc[row_num - 1, 2], number_format)  # 销售额
                product_sheet.write(row_num, 4, product_summary.iloc[row_num - 1, 4], number_format)  # 销售数量

            # 设置列宽
            product_sheet.set_column('A:B', 18)
            product_sheet.set_column('C:E', 15)

            # 创建新品渗透率表
            if not filtered_new_products_df.empty:
                # 计算区域渗透率
                region_customers = filtered_df.groupby('所属区域')['客户简称'].nunique().reset_index()
                region_customers.columns = ['所属区域', '客户总数']

                new_region_customers = filtered_new_products_df.groupby('所属区域')['客户简称'].nunique().reset_index()
                new_region_customers.columns = ['所属区域', '购买新品客户数']

                region_penetration = region_customers.merge(new_region_customers, on='所属区域', how='left')
                region_penetration['购买新品客户数'] = region_penetration['购买新品客户数'].fillna(0)
                region_penetration['渗透率'] = (
                            region_penetration['购买新品客户数'] / region_penetration['客户总数']).round(4)

                # 计算每个区域的新品销售额
                region_new_sales = filtered_new_products_df.groupby('所属区域')['销售额'].sum().reset_index()
                region_new_sales.columns = ['所属区域', '新品销售额']

                # 合并渗透率和销售额数据
                region_analysis = region_penetration.merge(region_new_sales, on='所属区域', how='left')
                region_analysis['新品销售额'] = region_analysis['新品销售额'].fillna(0)

                # 添加区域总销售额
                region_total_sales = filtered_df.groupby('所属区域')['销售额'].sum().reset_index()
                region_total_sales.columns = ['所属区域', '总销售额']
                region_analysis = region_analysis.merge(region_total_sales, on='所属区域', how='left')

                # 计算新品销售占比
                region_analysis['新品销售占比'] = (region_analysis['新品销售额'] / region_analysis['总销售额']).round(4)

                # 导出到Excel
                region_analysis.to_excel(writer, sheet_name='区域新品渗透分析', index=False)
                penetration_sheet = writer.sheets['区域新品渗透分析']

                # 格式化标题行
                for col_num, value in enumerate(region_analysis.columns.values):
                    penetration_sheet.write(0, col_num, value, header_format)

                # 应用数字和百分比格式
                for row_num in range(1, len(region_analysis) + 1):
                    penetration_sheet.write(row_num, 3, region_analysis.iloc[row_num - 1, 3], percent_format)  # 渗透率
                    penetration_sheet.write(row_num, 4, region_analysis.iloc[row_num - 1, 4], number_format)  # 新品销售额
                    penetration_sheet.write(row_num, 5, region_analysis.iloc[row_num - 1, 5], number_format)  # 总销售额
                    penetration_sheet.write(row_num, 6, region_analysis.iloc[row_num - 1, 6], percent_format)  # 新品销售占比

                # 设置列宽
                penetration_sheet.set_column('A:G', 15)

            # 保存Excel
            writer.close()

            return output.getvalue()


        excel_report = generate_excel_report(filtered_df, filtered_new_products_df)

        # 下载按钮
        st.markdown('<div class="download-button">', unsafe_allow_html=True)
        st.download_button(
            label="📥 下载Excel分析报告",
            data=excel_report,
            file_name="销售数据分析报告.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # 底部注释
        st.markdown("""
                <div style="text-align: center; margin-top: 30px; color: #646A73; padding: 20px; background-color: #F2F3F5; border-radius: 8px;">
                    <p>© 2025 销售数据分析仪表盘 | 飞书风格UI</p>
                    <p style="font-size: 0.8rem; margin-top: 5px;">数据更新时间: 2025年03月31日</p>
                </div>
                """, unsafe_allow_html=True)
