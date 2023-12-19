from docx import Document
# 导入 docx 模块 可以使用安装命令 pip install python-docx

class WordDocumentLayout:
    def __init__(self, doc_path):
        """
        初始化 WordDocumentLayout 类的实例。

        参数:
        - doc_path: Word 文档的路径
        """
        self.doc_path = doc_path
        self.doc = Document(self.doc_path)
        self.headings = []

    def extract_headings(self):
        """
        提取文档中的标题。
        """
        # 遍历文档的段落
        for paragraph in self.doc.paragraphs:
            # 检查段落的样式是否以 'Heading' 开头
            if paragraph.style.name.startswith('Heading'):
                text = paragraph.text.strip()  # 获取标题文本并去除首尾空格
                level = int(paragraph.style.name.replace('Heading', ''))  # 获取标题级别
                self.headings.append({'level': level, 'text': text})  # 将标题级别和文本添加到列表中

    def print_markdown_headings(self):
        """
        打印 Markdown 格式的标题。
        """
        # 遍历所有标题
        for heading in self.headings:
            level = heading['level']
            text = heading['text']
            markdown_heading = '#' * level + ' ' + text  # 构建 Markdown 格式的标题
            print(markdown_heading)  # 打印 Markdown 格式的标题

    def print_all_headings(self):
        """
        打印所有标题。
        """
        # 遍历所有标题
        for heading in self.headings:
            level = heading['level']
            text = heading['text']
            print(f"Level {level}: {text}")  # 打印标题级别和文本

    def generate_layout(self):
        """
        生成文档布局。
        调用 extract_headings 方法提取标题，
        然后调用 print_markdown_headings 方法打印 Markdown 格式的标题。
        """
        self.extract_headings()  # 提取标题
        self.print_markdown_headings()  # 打印 Markdown 格式的标题

# 在这里替换为你的 Word 文档路径
# doc_path = "path/to/your/document.docx"
doc_path = "D:\IT学习\大数据学习资料\尚硅谷大数据技术之Flink(1.17)\\1.笔记\尚硅谷大数据技术之Flink.docx"

# 创建 WordDocumentLayout 实例
layout = WordDocumentLayout(doc_path)

# 生成布局
layout.generate_layout()

print(" 打印所有标题")
# 打印所有标题
# layout.print_all_headings()