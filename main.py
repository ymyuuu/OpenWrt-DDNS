import os
import json
import subprocess
import csv
import requests

# 获取当前脚本的目录
script_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_directory)

# 配置文件路径
config_file = os.path.join(script_directory, "speed-test.json")

# 结果文件路径
result_file = os.path.join(script_directory, "result.csv")
ip_result_file = 'push-ip.txt'

def run_command_from_config():
    error_encountered = False  # 初始化错误标志为False

    if os.path.exists(config_file):
        with open(config_file, "r") as config:
            config_data = json.load(config)
            command = config_data["command"]
            # 直接执行命令
            result = subprocess.call(command, shell=True)
            if result != 0:
                print("执行命令时出错")
                error_encountered = True  # 设置错误标志为True

        if not error_encountered:
            extract_top_ips()
    else:
        print("未找到配置文件，请先配置参数.")
        error_encountered = True  # 设置错误标志为True

    return not error_encountered  # 返回True表示没有遇到错误，可以继续执行下面的代码

def extract_top_ips():
    error_encountered = False  # 初始化错误标志为False

    if os.path.exists(result_file):
        with open(result_file, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            ips = []
            # 读取前十行的 IP 地址
            for i, row in enumerate(csv_reader):
                if i == 0:
                    continue  # Skip header row
                ips.append(row[0])
                if i == 10:
                    break

        # 保存前十个 IP 地址到文件
        with open(ip_result_file, "w") as top_ips_file:
            top_ips_file.write("\n".join(ips))

        print("需要推送的 IP 已保存到push-ip.txt.")
    else:
        print("未找到 result.csv 文件，请确保命令执行成功并生成该文件.")
        error_encountered = True  # 设置错误标志为True

    return not error_encountered  # 返回True表示没有遇到错误，可以继续执行下面的代码

# 其余部分不需要修改

if __name__ == "__main__":
    if run_command_from_config():
        extract_top_ips()
