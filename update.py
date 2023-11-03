import os
import requests
import zipfile
import shutil
from datetime import datetime

# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 定义下载URL和文件名
download_url = "https://ymy.gay/https://zip.baipiao.eu.org"
zip_file_name = os.path.join(script_dir, "data.zip")
ip_txt_file_name = os.path.join(script_dir, "ip.txt")

# 记录脚本运行的时间
start_time = datetime.now()

# 输出开始时间
start_time_str = start_time.strftime('%Y-%m-%d %H:%M')
print(f"\n{start_time_str} 正在下载更新反代IP库\n")

# 下载ZIP文件
response = requests.get(download_url)
with open(zip_file_name, "wb") as zip_file:
    zip_file.write(response.content)

# 解压ZIP文件
with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
    zip_ref.extractall(os.path.join(script_dir, "data_folder"))

# 读取并合并txt文件
ip_set = set()
for root, _, files in os.walk(os.path.join(script_dir, "data_folder")):
    for file in files:
        if file.endswith(".txt"):
            with open(os.path.join(root, file), "r") as txt_file:
                for line in txt_file:
                    line = line.strip()
                    if line:
                        ip_set.add(line)

# 读取上次的IP记录
old_ip_list = []
if os.path.exists(ip_txt_file_name):
    with open(ip_txt_file_name, "r") as old_ip_file:
        for line in old_ip_file:
            line = line.strip()
            if line:
                old_ip_list.append(line)

# 检查新增和删除的IP
added_ips = list(ip_set - set(old_ip_list))
removed_ips = list(set(old_ip_list) - ip_set)

# 保存新的IP记录
with open(ip_txt_file_name, "w") as new_ip_file:
    for ip in sorted(ip_set, key=lambda x: [int(part) for part in x.split('.')]):
        new_ip_file.write(ip + '\n')

# 输出更新信息
end_time = datetime.now()
start_time_str = start_time.strftime('%Y-%m-%d %H:%M')

# 检查是否是第一次运行，如果是，则不输出变化信息
if not os.path.exists(ip_txt_file_name):
    print(f"第一次运行，共有 {len(ip_set)} 个IP\n")
else:
    if added_ips or removed_ips:
        if added_ips:
            print("+")
            for ip in sorted(added_ips, key=lambda x: [int(part) for part in x.split('.')]):
                print(ip)
        if removed_ips:
            print("-")
            for ip in sorted(removed_ips, key=lambda x: [int(part) for part in x.split('.')]):
                print(ip)
        print(f"本次更新之后共有 {len(ip_set)} 个IP\n")
    else:
        print(f"IP库更新完成，无变化，共有 {len(ip_set)} 个IP\n")

# 清理临时文件
os.remove(zip_file_name)
shutil.rmtree(os.path.join(script_dir, "data_folder"))
