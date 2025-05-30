import os
from pypdf import PdfMerger

def merge_pdfs_in_folder(folder_path, output_filename="merged_output.pdf"):
    """
    合并指定文件夹下所有PDF文件到一个新的PDF文件。
    使用场景：对于某些开会员才能批量pdf打印的情况，可以直接合并成一个文件然后打印
    Args:
        folder_path (str): 包含要合并的PDF文件的文件夹路径。
        output_filename (str): 合并后生成的新PDF文件的名称。
                                默认保存到 folder_path 文件夹下。
    """
    if not os.path.isdir(folder_path):
        print(f"错误：文件夹 '{folder_path}' 不存在或不是一个有效的文件夹。")
        return

    # 构建输出文件的完整路径
    output_path = os.path.join(folder_path, output_filename)

    # 创建一个PdfMerger对象
    merger = PdfMerger()

    pdf_files = []
    # 遍历文件夹查找所有以 .pdf 结尾的文件（不区分大小写）
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_files.append(filename)

    if not pdf_files:
        print(f"在文件夹 '{folder_path}' 中未找到任何PDF文件。")
        return

    # 按文件名排序，以确保合并顺序的可预测性
    pdf_files.sort()

    print(f"找到 {len(pdf_files)} 个PDF文件，准备合并：")
    for pdf_file in pdf_files:
        print(f"- {pdf_file}")

    # 逐个将PDF文件添加到merger中
    for pdf_file in pdf_files:
        file_path = os.path.join(folder_path, pdf_file)
        try:
            # 以二进制读取模式打开PDF文件
            with open(file_path, 'rb') as f:
                merger.append(f) # 将当前PDF的所有页面添加到merger
        except Exception as e:
            print(f"警告：处理文件 '{pdf_file}' 时发生错误：{e}。该文件将被跳过。")
            continue # 跳过当前文件，继续处理下一个

    # 将合并后的内容写入新的PDF文件
    try:
        with open(output_path, 'wb') as output_file:
            merger.write(output_file)
        print(f"\n成功合并所有文件到 '{output_path}'")
    except Exception as e:
        print(f"\n写入合并文件 '{output_path}' 时发生错误：{e}")
    finally:
        # 关闭merger对象，释放资源
        merger.close()



import PyPDF2

def split_pdf(input_pdf_path, output_folder, split_size=4):
    """
    将 PDF 文件按每 split 页拆分成多个 PDF 文件, 依次输出到output_folder下。
    Args:
        input_pdf_path (str): 输入的 PDF 文件路径。
        output_folder (str): 输出文件夹路径，用于存放拆分后的 PDF 文件。
        split_size (int): 每个新 PDF 文件包含的页面数，默认为 4 页。
    使用场景：对于需要将大 PDF 文件拆分成小文件的情况（例如对pdf文件上传大小有限制，需要分开上传），可以使用此函数。
    """
    # 打开原始 PDF 文件
    with open(input_pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)  # 获取总页数

        # 每 4 页拆分成一个新 PDF
        for start_page in range(0, total_pages, split_size):
            # 创建一个新的 PDF 写入器
            writer = PyPDF2.PdfWriter()
            
            # 添加当前组的页面
            for page_num in range(start_page, min(start_page + 4, total_pages)):
                writer.add_page(reader.pages[page_num])
            
            # 生成输出文件名
            output_filename = f"{output_folder}/output_{start_page + 1}_to_{min(start_page + 4, total_pages)}.pdf"
            
            # 写入新的 PDF 文件
            with open(output_filename, "wb") as output_file:
                writer.write(output_file)
            
            print(f"Created: {output_filename}")
