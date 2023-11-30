import os
import requests
from datetime import datetime

# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 定义下载URL和文件名
download_url = "https://proxy-ip.030101.xyz/iptxt"
ip_txt_file_name = os.path.join(script_dir, "ip.txt")

# 判断是否是第一次运行
is_first_run = not os.path.exists(ip_txt_file_name)

# 记录脚本运行的时间
start_time = datetime.now()

# 输出开始时间
start_time_str = start_time.strftime('%Y-%m-%d %H:%M')
print(f"\n{start_time_str} 正在下载更新反代IP库\n")

# 下载ip.txt文件，并跳过前三行
try:
    response = requests.get(download_url)
    response.raise_for_status()  # 检查是否有HTTP错误
    with open(ip_txt_file_name, "wb") as txt_file:
        lines = response.iter_lines()
        next(lines)  # 跳过第一行
        next(lines)  # 跳过第二行
        next(lines)  # 跳过第三行
        for line in lines:
            txt_file.write(line + b'\n')
except Exception as e:
    print(f"下载ip.txt文件时出现错误: {str(e)}")
    response = None

# 读取新的IP记录
new_ip_list = []
if response:
    try:
        with open(ip_txt_file_name, "r") as new_ip_file:
            for line in new_ip_file:
                line = line.strip()
                if line:
                    new_ip_list.append(line)
    except Exception as e:
        print(f"读取新的IP记录时出现错误: {str(e)}")

# 输出更新信息
end_time = datetime.now()
start_time_str = start_time.strftime('%Y-%m-%d %H:%M')
if response:  
    count = len(new_ip_list)
    if not is_first_run:  
        print(f"已更新IP库，共有 {count} 个IP\n")
    else:  
        print(f"首次运行，已下载最新IP库，共有 {count} 个IP\n")
else:  
    print("由于下载ip.txt文件时出现错误，无法进行IP库更新。\n")
