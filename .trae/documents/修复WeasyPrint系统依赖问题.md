# 修复WeasyPrint系统依赖问题

## 问题分析
当前错误是由于WeasyPrint库需要系统级依赖`libgobject-2.0-0`，但该库未安装导致的。WeasyPrint依赖多个系统库来处理字体渲染和PDF生成，在Linux环境下需要手动安装这些依赖。

## 解决方案
1. **安装系统依赖**：在Linux环境下安装WeasyPrint所需的系统库
2. **优化代码设计**：添加条件导入和优雅降级机制
3. **更新文档**：提供清晰的安装指南

## 实施步骤

### 1. 安装系统依赖
在Linux系统中运行以下命令安装所需依赖：
```bash
# Debian/Ubuntu系统
sudo apt-get update
sudo apt-get install -y libgobject-2.0-0 libcairo2 libpango1.0-0 libgdk-pixbuf2.0-0

# CentOS/RHEL系统
sudo yum install -y gobject-introspection gobject-introspection-devel cairo cairo-devel pango pango-devel gdk-pixbuf2 gdk-pixbuf2-devel
```

### 2. 优化pdf_generator.py代码
修改代码以添加条件导入和优雅降级机制：
```python
# 条件导入WeasyPrint，添加异常处理
try:
    from weasyprint import HTML, CSS
has_weasyprint = True
except (ImportError, OSError) as e:
    # 当WeasyPrint无法导入时，使用reportlab作为备选
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    has_weasyprint = False
    print(f"WeasyPrint导入失败，将使用reportlab作为备选: {e}")

# 修改create_pdf_report函数
def create_pdf_report(stock_info, agents_results, discussion_result, final_decision):
    """创建PDF格式的分析报告"""
    try:
        # 1. 生成Markdown内容
        markdown_content = generate_markdown_report(stock_info, agents_results, discussion_result, final_decision)
        
        if has_weasyprint:
            # WeasyPrint方式生成PDF
            # ... 现有WeasyPrint代码 ...
        else:
            # reportlab备用方式生成PDF
            # ... 原reportlab代码 ...
            
        return pdf_content
        
    except Exception as e:
        # 错误处理
        raise
```

### 3. 更新requirements.txt
确保requirements.txt包含所有需要的依赖：
```
markdown-it-py>=4.0.0
weasyprint>=67.0
pyyaml>=6.0.0
reportlab>=4.0.0  # 保留作为备选
```

### 4. 添加安装文档
在README.md或安装文档中添加系统依赖安装说明，确保用户知道如何在不同环境下安装所需依赖。

## 预期效果
1. 解决当前环境下的运行错误
2. 提供优雅的降级机制，确保在WeasyPrint无法使用时仍能通过reportlab生成PDF
3. 提供清晰的安装指南，帮助用户在不同环境下正确部署
4. 增强系统的鲁棒性和兼容性

## 风险评估
1. **系统依赖性**：WeasyPrint的系统依赖在不同Linux发行版上可能有所不同，需要提供不同发行版的安装指南
2. **性能差异**：reportlab和WeasyPrint生成的PDF在样式和性能上可能存在差异，需要测试确保两种方式生成的PDF质量一致
3. **代码复杂度**：添加条件分支会增加代码复杂度，需要确保代码结构清晰易维护