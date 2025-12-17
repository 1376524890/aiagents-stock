#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试基于浏览器的PDF生成功能
"""

from pdf_generator import create_pdf_report

# 创建测试数据
test_stock_info = {
    'symbol': '600000',
    'name': '浦发银行',
    'current_price': 8.50,
    'change_percent': 2.40,
    'pe_ratio': 5.80,
    'pb_ratio': 0.75,
    'market_cap': '3200亿',
    'market': 'A股',
    'exchange': '上海证券交易所'
}

test_agents_results = {
    'technical': '技术面分析：股票处于上升趋势，MACD金叉，成交量放大，建议买入。',
    'fundamental': '基本面分析：银行股估值较低，股息率高，长期投资价值突出。',
    'fund_flow': '资金面分析：主力资金净流入，北向资金持续买入。',
    'risk_management': '风险分析：银行股风险较低，适合稳健投资者。',
    'market_sentiment': '市场情绪：银行板块近期受到资金关注，情绪向好。'
}

test_discussion_result = '综合分析：浦发银行基本面良好，技术面走强，资金面支持，风险较低，市场情绪向好，建议买入。'

test_final_decision = {
    'rating': '买入',
    'target_price': 9.50,
    'operation_advice': '建议逢低买入',
    'entry_range': '8.00-8.50',
    'take_profit': '9.50',
    'stop_loss': '7.80',
    'holding_period': '3-6个月',
    'position_size': '20-30%',
    'confidence_level': 8,
    'risk_warning': '市场波动风险，政策风险'
}

print("测试基于浏览器的PDF生成功能...")
print("1. 调用create_pdf_report函数")
try:
    # 调用PDF生成函数
    pdf_content = create_pdf_report(test_stock_info, test_agents_results, test_discussion_result, test_final_decision)
    
    # 保存PDF文件
    with open("test_browser_report.pdf", "wb") as f:
        f.write(pdf_content)
    
    print(f"✓ PDF生成成功，文件大小: {len(pdf_content)} bytes")
    print(f"✓ PDF文件保存成功: test_browser_report.pdf")
    print("🎉 测试通过！基于浏览器的PDF生成功能正常工作。")
except Exception as e:
    print(f"✗ PDF生成失败: {str(e)}")
    import traceback
    traceback.print_exc()
