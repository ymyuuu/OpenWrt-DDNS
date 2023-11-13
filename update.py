import os
import requests
import zipfile
import shutil
from datetime import datetime

# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 定义下载URL和文件名
download_url = "https://proxy-ip.030101.xyz"
zip_file_name = os.path.join(script_dir, "data.zip")
ip_txt_file_name = os.path.join(script_dir, "ip.txt")

# 判断是否是第一次运行
is_first_run = not os.path.exists(ip_txt_file_name)

# 记录脚本运行的时间
start_time = datetime.now()

# 输出开始时间
start_time_str = start_time.strftime('%Y-%m-%d %H:%M')
print(f"\n{start_time_str} 正在下载更新反代IP库\n")

# 下载ZIP文件
try:
    response = requests.get(download_url)
    response.raise_for_status()  # 检查是否有HTTP错误
    with open(zip_file_name, "wb") as zip_file:
        zip_file.write(response.content)
except Exception as e:
    print(f"下载ZIP文件时出现错误: {str(e)}")
    response = None

# 解压ZIP文件
if response:
    try:
        with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
            zip_ref.extractall(os.path.join(script_dir, "data_folder"))
    except Exception as e:
        print(f"解压ZIP文件时出现错误: {str(e)}")

# 读取并合并txt文件
ip_set = set()
for root, _, files in os.walk(os.path.join(script_dir, "data_folder")):
    for file in files:
        if file.endswith(".txt"):
            try:
                with open(os.path.join(root, file), "r") as txt_file:
                    for line in txt_file:
                        line = line.strip()
                        if line:
                            ip_set.add(line)
            except Exception as e:
                print(f"读取并合并txt文件时出现错误: {str(e)}")

# 读取上次的IP记录
old_ip_list = []
if not is_first_run:
    try:
        with open(ip_txt_file_name, "r") as old_ip_file:
            for line in old_ip_file:
                line = line.strip()
                if line:
                    old_ip_list.append(line)
    except Exception as e:
        print(f"读取上次的IP记录时出现错误: {str(e)}")

# 检查新增和删除的IP
added_ips = list(ip_set - set(old_ip_list))
removed_ips = list(set(old_ip_list) - ip_set)

# 保存新的IP记录
try:
    with open(ip_txt_file_name, "w") as new_ip_file:
        for ip in sorted(ip_set, key=lambda x: [int(part) for part in x.split('.')]):
            new_ip_file.write(ip + '\n')
except Exception as e:
    print(f"保存新的IP记录时出现错误: {str(e)}")

# 输出更新信息
end_time = datetime.now()
start_time_str = start_time.strftime('%Y-%m-%d %H:%M')
if response and not is_first_run:  # 只在不是第一次运行且没有下载错误时输出变化信息
    if added_ips or removed_ips:
        if added_ips:
            print("+")
            for ip in sorted(added_ips, key=lambda x: [int(part) for part in x.split('.')]):
                print(ip)
        if removed_ips:
            print("-")
            for ip in sorted(removed_ips, key=lambda x: [int(part) for part in x.split('.')]):
                print(ip)
        count = len(ip_set)
        print(f"本次更新之后共有 {count} 个IP\n")
    else:
        count = len(ip_set)
        print(f"IP库已是最新，共有 {count} 个IP\n")
elif response and is_first_run:  # 只在不是第一次运行且没有下载错误时输出首次运行信息
    count = len(ip_set)
    print(f"首次运行，已下载最新IP库，共有 {count} 个IP\n")
elif not response:
    print("由于下载ZIP文件时出现错误，无法进行IP库更新。\n")

# 清理临时文件
try:
    os.remove(zip_file_name)
    shutil.rmtree(os.path.join(script_dir, "data_folder"))
except Exception as e:
    print(f"清理临时文件时出现错误: {str(e)}")
