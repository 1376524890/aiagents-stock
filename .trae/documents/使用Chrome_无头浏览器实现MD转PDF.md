# 使用Chrome/无头浏览器实现MD转PDF

## 问题分析
当前使用WeasyPrint实现MD转PDF存在系统依赖问题，用户要求使用Chrome/无头浏览器来替代，以提高跨平台兼容性。

## 解决方案
1. 安装Chrome/Chromium浏览器和无头浏览器支持
2. 使用Python库（如pyppeteer或selenium）控制浏览器进行MD转PDF
3. 修改PDF生成逻辑，实现基于浏览器的转换
4. 确保代码能够自适应不同系统环境

## 实施步骤

### 1. 安装系统依赖
```bash
# Debian/Ubuntu系统
# 安装Chromium浏览器
sudo apt-get update
sudo apt-get install -y chromium-browser

# 安装必要的系统库
sudo apt-get install -y libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libnss3 libcups2 libxss1 libxrandr2 libgconf2-4 libasound2 libatk1.0-0 libatk-bridge2.0-0 libpangocairo-1.0-0 libgtk-3-0
```

### 2. 安装Python库
```bash
pip install pyppeteer markdown-it-py
```

### 3. 修改pdf_generator.py代码
1. 移除WeasyPrint依赖，添加pyppeteer支持
2. 实现基于浏览器的MD转PDF逻辑
3. 添加环境检测和自适应机制

### 4. 更新requirements.txt
添加新的依赖包：
```
pyppeteer>=2.0.0
markdown-it-py>=4.0.0
```

### 5. 测试验证
- 在Linux系统上测试无头浏览器转换
- 在Windows系统上测试Chrome转换
- 确保生成的PDF格式正确

## 预期效果
1. 解决WeasyPrint的系统依赖问题
2. 提高跨平台兼容性
3. 利用浏览器强大的渲染能力，生成高质量PDF
4. 支持更丰富的Markdown特性和CSS样式

## 风险评估
1. 浏览器依赖：需要确保目标系统安装了Chrome/Chromium
2. 性能：浏览器转换可能比直接转换库稍慢
3. 资源消耗：浏览器实例会占用一定内存和CPU资源
4. 兼容性：不同浏览器版本可能产生细微差异

## 代码实现思路
```python
# 条件导入浏览器转换库
try:
    from pyppeteer import launch
has_pyppeteer = True
except ImportError:
    has_pyppeteer = False

def markdown_to_pdf(markdown_content, output_path):
    """使用浏览器将Markdown转换为PDF"""
    if has_pyppeteer:
        # 使用pyppeteer实现转换
        pass
    else:
        # 回退到其他转换方式
        pass
```