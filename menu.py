import os
import json
import subprocess

# 获取当前脚本的目录
script_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_directory)

# 配置文件路径
config_file = os.path.join(script_directory, "speed-test.json")
dns_file = os.path.join(script_directory, "cf-dns.json")

def configure_parameters():
    # 询问其他参数
    n = input("先配置点参数，你别急\n\n延迟测速线程 (-n, 默认 200): ") or "200"
    t = input("延迟测速次数 (-t, 默认 4): ") or "4"
    tp = input("测速端口 (-tp, 默认 80): ") or "80"
    tl = input("平均延迟上限 (-tl, 默认 200 ms): ") or "200"
    tll = input("平均延迟下限 (-tll, 默认 0 ms): ") or "0"
    tlr = input("丢包几率上限 (-tlr, 默认 1.00): ") or "1.00"
    p = input("显示结果数量 (-p, 默认10个): ") or "10"

    # 根据测速端口自动设置默认测速地址
    if tp in ["80", "8080", "8880", "2052", "2086", "2095"]:
        url = "http://speed.bestip.one/__down?bytes=50000000"
    elif tp in ["443", "8443", "2053", "2096", "2087", "2083"]:
        url = "https://speed.bestip.one/__down?bytes=50000000"
    else:
        url = input("测速地址 (-url, 默认 https://speed.bestip.one/__down?bytes=50000000): ") or "https://speed.bestip.one/__down?bytes=50000000"

    # 根据是否启用下载测速询问
    download_enabled = input("\n是否启用下载测速 (-dd, 默认回车启用, 输入任何字符禁用): ").strip().lower()
    if download_enabled:
        download_option = '-dd'
        dn = dt = sl = "0"
    else:
        download_option = ''
        dn = input("下载测速数量 (-dn, 默认 10): ") or "10"
        dt = input("下载测速时间 (-dt, 默认 3秒): ") or "3"
        sl = input("下载速度下限 (-sl, 默认 10.00 MB/s): ") or "10.00"

    # 生成命令
    command = f"./CloudflareST -n {n} -t {t} {download_option} -dn {dn} -dt {dt} -tp {tp} -url {url} -tl {tl} -tll {tll} -tlr {tlr} -sl {sl} -p {p}"

    # 添加执行权限
    subprocess.call(f"chmod +x {script_directory}/CloudflareST", shell=True)
    
    # 保存参数到配置文件
    with open(config_file, "w") as config:
        config_data = {
            "command": command
        }
        json.dump(config_data, config)
    
    # 询问用户是否进行DNS推送
    dns_push = input("\n是否要进行DNS推送到Cloudflare (回车是，输入任何字符否): ").strip()
    if dns_push == "":
        # 如果用户选择进行DNS推送 (按回车)，继续询问DNS相关信息。
        api_token = input("请输入您的 Cloudflare API 令牌: ")
        zone_id = input("请输入您的区域ID: ")
        record_name = input("请输入DNS记录名称 (默认为 '@'): ") or "@"
        # 保存DNS信息到文件
        with open(dns_file, "w") as dns_config:
            dns_data = {
                "api_token": api_token,
                "zone_id": zone_id,
                "record_name": record_name
            }
            json.dump(dns_data, dns_config)
    else:
        # 如果用户选择不进行DNS推送（输入任何字符），删除 cf-dns.json 文件（如果存在）。
        if os.path.exists(dns_file):
            os.remove(dns_file)

    # 运行 main.py
    run_main_py()

def run_main_py():
    print("\n开始了哦，不许调皮哦\n")  # 输出开始提示
    subprocess.call(f"python3 {script_directory}/main.py", shell=True)
    exit(0)

def main():
    if os.path.exists(config_file):
        while True:
            print("\n菜单:")
            print("1. 重新配置命令参数")
            print("2. 执行 main.py")
            print("3. 退出")

            choice = input("请选择一个选项: ")
            if choice == "1":
                configure_parameters()
            elif choice == "2":
                run_main_py()
            elif choice == "3":
                break
            else:
                print("请选择一个有效的选项。")
    else:
        configure_parameters()

if __name__ == "__main__":
    main()
