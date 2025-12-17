# 修复PDF生成的信号处理错误

## 1. 问题分析
- 错误信息：`signal only works in main thread of the main interpreter`
- 错误位置：`pyppeteer/launcher.py`第159行，尝试调用`signal.signal(signal.SIGINT, _close_process)`
- 触发原因：在非主线程中使用`asyncio.run()`调用异步函数`markdown_to_pdf_browser()`
- 影响范围：所有使用浏览器生成PDF的功能

## 2. 解决方案

### 2.1 主要解决方案：禁用pyppeteer的信号处理
- 在`launch()`函数调用中添加`handleSIGINT=False`参数
- 同时添加`handleSIGTERM=False`和`handleSIGHUP=False`参数，确保完全禁用信号处理
- 这样可以避免pyppeteer在非主线程中尝试调用`signal.signal()`

### 2.2 辅助解决方案：优化异步调用方式
- 确保异步函数在调用`launch()`时不会触发信号处理问题
- 保持现有代码结构不变，最小化修改

## 3. 具体修改

### 3.1 修改`pdf_generator.py`文件
- 在`markdown_to_pdf_browser`函数的`launch()`调用中添加信号处理禁用参数
- 修改位置：第169行
- 添加的参数：
  ```python
  handleSIGINT=False,
  handleSIGTERM=False,
  handleSIGHUP=False,
  ```

## 4. 预期效果
- PDF生成功能恢复正常
- 不再出现信号处理相关的错误
- 保持现有功能不变
- 兼容多线程环境

## 5. 验证方法
- 运行测试脚本`test_browser_pdf.py`
- 检查PDF生成是否成功
- 查看是否有错误输出

## 6. 备选方案
如果禁用信号处理仍不能解决问题，我们可以考虑：
- 完全切换到reportlab生成PDF
- 使用其他基于浏览器的PDF生成库
- 重构异步调用方式

这个修复方案简单直接，修改量小，风险低，能够有效解决当前的信号处理错误。