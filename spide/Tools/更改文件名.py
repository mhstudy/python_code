import os

folder_path = "D:\\BaiduNetdiskDownload\\new 孙宇晨：财务自由革命之路文字和语音版\\101~155"

# 列出指定文件夹下所有的文件和文件夹名称
for filename in os.listdir(folder_path):
    print(filename)
    old_file = os.path.join(folder_path, filename)
    if os.path.isfile(old_file):
        new_file = os.path.join(folder_path, filename[0:len(filename)-19] + ".mp3")  # 修改文件名规则
        print("old_file = " + old_file)
        print("new_file = " + new_file)

        os.rename(old_file, new_file)
        # print(f"已将 {filename} 重命名为 new_{filename}")

        print('########################\n')
