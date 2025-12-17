# LLM分析prompt添加日期时间和时区配置

## 1. 需求分析
- 在所有LLM分析的prompt中加入当前日期和时间，帮助LLM了解当前时间进行分析
- 在env中添加时区相关配置，默认为中国上海
- 使用标准配置格式

## 2. 实现步骤

### 2.1 在config_manager.py中添加时区配置
- 在`default_config`字典中添加时区配置项
- 默认为Asia/Shanghai
- 添加到.env文件的保存逻辑中

### 2.2 修改LLM调用代码，在prompt中加入当前日期和时间
- 修改deepseek_client.py中的所有LLM分析方法
- 在prompt开头添加当前日期和时间信息
- 考虑时区配置，使用正确的时区获取当前时间

### 2.3 检查其他LLM调用文件
- 检查ai_agents.py中的LLM调用
- 检查longhubang_agents.py中的LLM调用
- 检查smart_monitor_deepseek.py中的LLM调用
- 确保所有LLM分析的prompt都包含日期和时间信息

## 3. 具体实现细节

### 3.1 配置管理修改
- 在config_manager.py的default_config中添加：
  ```python
  "TIMEZONE": {
      "value": "Asia/Shanghai",
      "description": "系统时区配置，默认为中国上海",
      "required": False,
      "type": "text"
  }
  ```
- 在write_env方法中添加时区配置到.env文件

### 3.2 LLM prompt修改
- 在deepseek_client.py中添加获取当前日期和时间的逻辑：
  ```python
  from datetime import datetime
  import pytz
  
  def get_current_datetime(timezone_str):
      tz = pytz.timezone(timezone_str)
      return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
  ```
- 在所有LLM分析方法的prompt开头添加：
  ```
  【分析时间】
  当前日期时间: {current_datetime}
  时区: {timezone}
  ```

### 3.3 验证修改
- 确保所有LLM调用的prompt都包含日期和时间信息
- 确保时区配置被正确使用
- 确保不破坏现有功能

## 4. 预期效果
- 所有LLM分析的prompt都包含当前日期和时间信息
- LLM可以利用当前时间进行更准确的分析
- 时区配置可以在.env文件中自定义
- 默认为中国上海时区

## 5. 注意事项
- 使用标准的配置格式
- 确保时区配置被正确应用到所有LLM调用
- 不要破坏现有的功能
- 确保所有LLM分析的prompt都包含日期和时间信息