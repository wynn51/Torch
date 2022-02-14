def get_file_content(full_report_path, size=1024):
    with open(full_report_path) as file:
    	# 每次读取1024字节，直至全部读取完
        while True:
            content = file.read(size)
            # content为空时证明文件读取完成，就不再继续读了
            if not content:
                break
        yield content
