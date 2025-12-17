#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试LLM prompt是否包含日期和时间信息
"""

from deepseek_client import DeepSeekClient

# 创建DeepSeekClient实例
client = DeepSeekClient()

# 测试call_api方法是否会自动添加日期和时间信息
test_messages = [
    {"role": "system", "content": "你是一个测试助手，负责验证prompt中是否包含日期和时间信息。"},
    {"role": "user", "content": "这是一个测试prompt，请告诉我这个prompt中是否包含日期和时间信息。"}
]

print("原始messages:")
for msg in test_messages:
    print(f"{msg['role']}: {msg['content'][:100]}...")

print("\n调用call_api方法...")
response = client.call_api(test_messages, max_tokens=100)

print("\nAPI响应:")
print(response)
