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

# 关闭代理工具，不输出结果和报错
def stop_proxies():
    commands = [
        "/etc/init.d/passwall stop",
        "/etc/init.d/passwall2 stop",
        "/etc/init.d/ssr-plus stop",
        "/etc/init.d/openclash stop",
        "/etc/init.d/bypass stop",
        "/etc/init.d/helloworld stop"
        # Add more stop commands for other proxies if needed
    ]
    for command in commands:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 启动代理工具，不输出结果和报错
def start_proxies():
    commands = [
        "/etc/init.d/passwall start",
        "/etc/init.d/passwall2 start",
        "/etc/init.d/ssr-plus start",
        "/etc/init.d/openclash start",
        "/etc/init.d/bypass start",
        "/etc/init.d/helloworld start"
        # Add more start commands for other proxies if needed
    ]
    for command in commands:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_command_from_config():
    # 先关闭代理工具
    stop_proxies()
    print(f"已自动关闭代理工具（如果存在）\n")

    if os.path.exists(config_file):
        with open(config_file, "r") as config:
            config_data = json.load(config)
            command = config_data["command"]
            # 直接执行命令
            try:
                subprocess.call(command, shell=True)
            except Exception as e:
                print(f"运行命令时发生错误: {str(e)}")
                return

        extract_top_ips()
    else:
        print("未找到配置文件，请先配置参数。")

def extract_top_ips():
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

        print("\n需要推送的 IP 已保存到push-ip.txt。")
    else:
        print("未找到 result.csv 文件，请确保命令执行成功并生成该文件.")

def configure_dns_records():
    # 从 'cf-dns.json' 获取DNS配置
    dns_config_file = 'cf-dns.json'
    if os.path.exists(dns_config_file):
        with open(dns_config_file, 'r') as file:
            dns_config = json.load(file)

        api_token = dns_config["api_token"]
        zone_id = dns_config["zone_id"]
        record_name = dns_config["record_name"]

        # 从 'push-ip.txt' 获取IP地址列表
        ip_addresses = []
        with open(ip_result_file, 'r') as file:
            for line in file:
                ip_addresses.append(line.strip())

        # 构建API请求头
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        # DNS记录的基本URL
        base_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

        # 删除所有'A'记录
        print("\n正在删除所有 DNS 'A'记录")
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for record in data["result"]:
                record_type = record["type"]
                if record_type == "A":  # 仅删除'A'记录
                    delete_url = f"{base_url}/{record['id']}"
                    response = requests.delete(delete_url, headers=headers)
                    if response.status_code != 200:
                        print(f"删除'A'记录时出错，HTTP响应代码：{response.status_code}")
                        return
            print("已删除所有DNS 'A'记录")
        else:
            print(f"无法获取DNS记录信息。响应代码: {response.status_code}")
            return

        # 创建新的'A'记录
        for ip in ip_addresses:
            dns_record = {
                "type": "A",
                "name": record_name,
                "content": ip,
                "ttl": 600,
                "proxied": False
            }

            # 发送POST请求创建DNS记录
            response = requests.post(base_url, headers=headers, json=dns_record)

            if response.status_code == 200:
                print(f"成功创建 (IPv4) DNS记录，IP地址: {ip}")
            else:
                print("创建DNS记录时出错")
                print(f"创建DNS记录时出错，HTTP响应代码：{response.status_code}")
                return
    else:
        print("未配置DNS参数 cf-dns.json 。")

if __name__ == "__main__":
    run_command_from_config()
    configure_dns_records()
    start_proxies()  # 最后重新启动代理工具
    print(f"\n已自动开启代理工具（如果存在）")
