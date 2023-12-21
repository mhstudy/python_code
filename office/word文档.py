from docx import Document
import os

def convert_heading_to_markdown(doc, heading_level=None):
    markdown_content = ""
    for paragraph in doc.paragraphs:
        if paragraph.style.name.startswith('Heading'):
            level = int(paragraph.style.name.split(' ')[-1])
            if heading_level is None or level <= heading_level:
                markdown_content += '#' * level + ' ' + paragraph.text + '\n'
    return markdown_content

def write_to_markdown_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def convert_word_to_markdown(word_file, heading_level=None):
    doc = Document(word_file)
    markdown_content = convert_heading_to_markdown(doc, heading_level)
    print(markdown_content)
    # markdown_file = os.path.splitext(word_file)[0] + '.md'
    # write_to_markdown_file(markdown_file, markdown_content)

# 使用方法
# convert_word_to_markdown('your_word_file.docx', 2)  # 只输出到二级标题
# convert_word_to_markdown('your_word_file.docx')  # 输出所有标题

path = "E:\\BaiduNetdiskDownload\\尚硅谷大数据技术之Hive on Spark调优.docx"
convert_word_to_markdown(path)

