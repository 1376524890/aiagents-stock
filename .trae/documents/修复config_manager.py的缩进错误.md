# 修复config_manager.py的缩进错误

## 1. 问题分析
- 错误信息：`SyntaxError: expected 'except' or 'finally' block`
- 错误位置：`config_manager.py`第178行
- 触发原因：try块内的代码缩进不一致
- 影响范围：所有使用配置管理的功能

## 2. 解决方案

### 2.1 修复缩进错误
- 确保write_env方法中try块内的所有代码都保持正确的缩进
- 从第178行到第216行的代码应该缩进4个空格，与try块内的其他代码保持一致
- 修复后的代码结构应该是：
  ```python
try:
    lines = []
    lines.append(...)  # 正确缩进
    lines.append(...)  # 正确缩进
    # 其他代码保持正确缩进
    with open(...) as f:
        f.write(...)
    return True
except Exception as e:
    print(...)
    return False
  ```

## 3. 具体修改

### 3.1 修改`config_manager.py`文件
- 修复write_env方法中try块内的缩进错误
- 修改范围：第178行到第216行
- 确保所有代码都缩进4个空格，与try块内的其他代码保持一致

## 4. 预期效果
- 语法错误消失
- 配置管理功能恢复正常
- 应用程序可以正常启动

## 5. 验证方法
- 运行应用程序
- 检查是否有语法错误
- 查看配置管理功能是否正常工作

这个修复方案简单直接，只需要调整代码缩进，就能解决语法错误问题。