#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF报告生成器
只生成PDF格式的完整分析报告
"""

import base64
from datetime import datetime
import io
import tempfile
import os
from markdown_it import MarkdownIt
from weasyprint import HTML, CSS
import yaml

# 条件导入streamlit，只在需要时导入
try:
    import streamlit as st
except ImportError:
    st = None

def register_chinese_fonts():
    """注册中文字体 - 支持Windows和Linux系统"""
    try:
        # 检查是否已经注册过
        if 'ChineseFont' in pdfmetrics.getRegisteredFontNames():
            return 'ChineseFont'
        
        # Windows系统字体路径
        windows_font_paths = [
            'C:/Windows/Fonts/simsun.ttc',  # 宋体
            'C:/Windows/Fonts/simhei.ttf',  # 黑体
            'C:/Windows/Fonts/msyh.ttc',    # 微软雅黑
            'C:/Windows/Fonts/msyh.ttf',    # 微软雅黑（TTF格式）
        ]
        
        # Linux系统字体路径（Docker环境）
        linux_font_paths = [
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # 文泉驿正黑
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # 文泉驿微米黑
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',  # Noto Sans CJK
            '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc',  # Noto Serif CJK
            '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',  # Droid字体
        ]
        
        # 合并所有可能的字体路径
        all_font_paths = windows_font_paths + linux_font_paths
        
        # 尝试注册字体
        for font_path in all_font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                    print(f"✅ 成功注册中文字体: {font_path}")
                    return 'ChineseFont'
                except Exception as e:
                    print(f"⚠️ 尝试注册字体 {font_path} 失败: {e}")
                    continue
        
        # 如果没有找到中文字体，打印警告并使用默认字体
        print("⚠️ 警告：未找到中文字体，PDF中文可能显示为方框")
        print("建议：在Docker中安装中文字体包")
        return 'Helvetica'
    except Exception as e:
        print(f"❌ 注册中文字体时出错: {e}")
        return 'Helvetica'

def get_chinese_font_css():
    """获取中文支持的CSS样式"""
    # 定义支持中文的CSS
    css_content = """
    @page {
        size: A4;
        margin: 2cm;
    }
    
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', 'WenQuanYi Micro Hei', sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 100%;
        margin: 0 auto;
        padding: 0;
    }
    
    h1 {
        color: #2c3e50;
        text-align: center;
        font-size: 28px;
        margin-bottom: 20px;
        font-weight: bold;
    }
    
    h2 {
        color: #34495e;
        border-left: 4px solid #3498db;
        padding-left: 15px;
        margin-top: 30px;
        margin-bottom: 15px;
        font-size: 20px;
    }
    
    h3 {
        color: #2980b9;
        margin-top: 20px;
        margin-bottom: 10px;
        font-size: 18px;
    }
    
    p {
        margin-bottom: 15px;
        text-align: justify;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
    }
    
    th {
        background-color: #3498db;
        color: white;
        padding: 12px;
        text-align: left;
        font-weight: bold;
    }
    
    td {
        padding: 10px;
        border: 1px solid #ddd;
    }
    
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    
    hr {
        border: 0;
        height: 1px;
        background: #ccc;
        margin: 30px 0;
    }
    
    strong {
        font-weight: bold;
    }
    
    em {
        font-style: italic;
    }
    
    ul, ol {
        margin: 15px 0;
        padding-left: 30px;
    }
    
    li {
        margin-bottom: 8px;
    }
    """
    return css_content

def create_pdf_report(stock_info, agents_results, discussion_result, final_decision):
    """创建PDF格式的分析报告"""
    try:
        # 1. 生成Markdown内容
        markdown_content = generate_markdown_report(stock_info, agents_results, discussion_result, final_decision)
        
        # 2. 使用markdown-it-py将Markdown转换为HTML
        md = MarkdownIt()
        html_content = md.render(markdown_content)
        
        # 3. 添加完整的HTML结构
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>AI股票分析报告</title>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # 4. 生成PDF
        buffer = io.BytesIO()
        
        # 获取CSS样式
        css = CSS(string=get_chinese_font_css())
        
        # 使用weasyprint生成PDF
        HTML(string=full_html).write_pdf(buffer, stylesheets=[css])
        
        # 5. 获取PDF内容
        pdf_content = buffer.getvalue()
        buffer.close()
        
        return pdf_content
        
    except Exception as e:
        # 只在有streamlit时显示错误
        if st is not None:
            st.error(f"生成PDF时出错: {str(e)}")
            import traceback
            st.error(f"详细错误信息: {traceback.format_exc()}")
        # 总是抛出异常，让调用者处理
        raise

def create_download_link(pdf_content, filename):
    """创建PDF下载链接"""
    b64 = base64.b64encode(pdf_content).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}" style="display: inline-block; padding: 15px 30px; background-color: #e74c3c; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; margin: 10px;">📄 下载PDF报告</a>'
    return href

def generate_markdown_report(stock_info, agents_results, discussion_result, final_decision):
    """生成Markdown格式的分析报告"""
    
    # 获取当前时间
    current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    
    markdown_content = f"""
# AI股票分析报告

**生成时间**: {current_time}

---

## 📊 股票基本信息

| 项目 | 值 |
|------|-----|
| **股票代码** | {stock_info.get('symbol', 'N/A')} |
| **股票名称** | {stock_info.get('name', 'N/A')} |
| **当前价格** | {stock_info.get('current_price', 'N/A')} |
| **涨跌幅** | {stock_info.get('change_percent', 'N/A')}% |
| **市盈率(PE)** | {stock_info.get('pe_ratio', 'N/A')} |
| **市净率(PB)** | {stock_info.get('pb_ratio', 'N/A')} |
| **市值** | {stock_info.get('market_cap', 'N/A')} |
| **市场** | {stock_info.get('market', 'N/A')} |
| **交易所** | {stock_info.get('exchange', 'N/A')} |

---

## 🔍 各分析师详细分析

"""

    # 添加各分析师的分析结果
    agent_names = {
        'technical': '📈 技术分析师',
        'fundamental': '📊 基本面分析师',
        'fund_flow': '💰 资金面分析师',
        'risk_management': '⚠️ 风险管理师',
        'market_sentiment': '📈 市场情绪分析师'
    }
    
    for agent_key, agent_name in agent_names.items():
        if agent_key in agents_results:
            agent_result = agents_results[agent_key]
            if isinstance(agent_result, dict):
                analysis_text = agent_result.get('analysis', '暂无分析')
            else:
                analysis_text = str(agent_result)
            
            markdown_content += f"""
### {agent_name}

{analysis_text}

---

"""

    # 添加团队讨论结果
    markdown_content += f"""
## 🤝 团队综合讨论

{discussion_result}

---

## 📋 最终投资决策

"""
    
    # 处理最终决策的显示
    if isinstance(final_decision, dict) and "decision_text" not in final_decision:
        # JSON格式的决策
        markdown_content += f"""
**投资评级**: {final_decision.get('rating', '未知')}

**目标价位**: {final_decision.get('target_price', 'N/A')}

**操作建议**: {final_decision.get('operation_advice', '暂无建议')}

**进场区间**: {final_decision.get('entry_range', 'N/A')}

**止盈位**: {final_decision.get('take_profit', 'N/A')}

**止损位**: {final_decision.get('stop_loss', 'N/A')}

**持有周期**: {final_decision.get('holding_period', 'N/A')}

**仓位建议**: {final_decision.get('position_size', 'N/A')}

**信心度**: {final_decision.get('confidence_level', 'N/A')}/10

**风险提示**: {final_decision.get('risk_warning', '无')}
"""
    else:
        # 文本格式的决策
        decision_text = final_decision.get('decision_text', str(final_decision))
        markdown_content += decision_text

    markdown_content += """

---

## 📝 免责声明

本报告由AI系统生成，仅供参考，不构成投资建议。投资有风险，入市需谨慎。请在做出投资决策前咨询专业的投资顾问。

---

*报告生成时间: {current_time}*
*AI股票分析系统 v1.0*
"""

    return markdown_content

def create_markdown_download_link(markdown_content, filename):
    """创建Markdown下载链接"""
    b64 = base64.b64encode(markdown_content.encode()).decode()
    href = f'<a href="data:text/markdown;base64,{b64}" download="{filename}" style="display: inline-block; padding: 15px 30px; background-color: #9b59b6; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; margin: 10px;">📝 下载Markdown报告</a>'
    return href

def display_pdf_export_section(stock_info, agents_results, discussion_result, final_decision):
    """显示PDF导出区域"""
    
    st.markdown("---")
    st.markdown("## 📄 导出分析报告")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 生成PDF报告按钮（使用股票代码作为key的一部分，确保唯一性）
        pdf_button_key = f"pdf_btn_{stock_info.get('symbol', 'unknown')}"
        markdown_button_key = f"markdown_btn_{stock_info.get('symbol', 'unknown')}"
        
        # 生成PDF报告按钮
        if st.button("📄 生成并下载PDF报告", type="primary", width='content', key=pdf_button_key):
            with st.spinner("正在生成PDF报告..."):
                try:
                    # 生成PDF内容
                    pdf_content = create_pdf_report(stock_info, agents_results, discussion_result, final_decision)
                    
                    # 生成文件名
                    stock_symbol = stock_info.get('symbol', 'unknown')
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"股票分析报告_{stock_symbol}_{timestamp}.pdf"
                    
                    st.success("✅ PDF报告生成成功！")
                    st.balloons()
                    
                    # 显示下载链接
                    st.markdown("### 📄 报告下载")
                    
                    download_link = create_download_link(pdf_content, filename)
                    st.markdown(f"""
                    <div style="text-align: center; margin: 20px 0;">
                        {download_link}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info("💡 提示：点击上方按钮即可下载PDF格式的完整分析报告")
                    
                except Exception as e:
                    st.error(f"❌ 生成PDF报告时出错: {str(e)}")
                    import traceback
                    st.error(f"详细错误信息: {traceback.format_exc()}")
        
        # 生成Markdown报告按钮
        if st.button("📝 生成并下载Markdown报告", type="secondary", width='content', key=markdown_button_key):
            with st.spinner("正在生成Markdown报告..."):
                try:
                    # 生成Markdown内容
                    markdown_content = generate_markdown_report(stock_info, agents_results, discussion_result, final_decision)
                    
                    # 生成文件名
                    stock_symbol = stock_info.get('symbol', 'unknown')
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"股票分析报告_{stock_symbol}_{timestamp}.md"
                    
                    st.success("✅ Markdown报告生成成功！")
                    st.balloons()
                    
                    # 显示下载链接
                    st.markdown("### 📄 报告下载")
                    
                    download_link = create_markdown_download_link(markdown_content, filename)
                    st.markdown(f"""
                    <div style="text-align: center; margin: 20px 0;">
                        {download_link}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info("💡 提示：点击上方按钮即可下载Markdown格式的完整分析报告")
                    
                except Exception as e:
                    st.error(f"❌ 生成Markdown报告时出错: {str(e)}")
                    import traceback
                    st.error(f"详细错误信息: {traceback.format_exc()}")

