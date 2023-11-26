# OpenWrt DDNS 安装指南

本指南将介绍如何在 OpenWrt 上安装和配置优选反代IP或自定义测速 IP 的 DDNS（动态域名解析）服务。

<img width="1430" alt="image" src="https://github.com/ymyuuu/OpenWrt-DDNS/assets/135582157/bc9cd339-c598-4a94-b0ca-8ba882f46fdf">

## 依赖

在开始安装之前，请确保已安装以下依赖：

```shell
opkg update &&
opkg install wget unzip python3 python3-pip &&
pip3 install requests

```

## 安装步骤

执行以下命令以安装 OpenWrt DDNS：

```shell
mkdir -p /OpenWrt-DDNS &&
rm -rf /OpenWrt-DDNS/* &&
wget -O /OpenWrt-DDNS/OpenWrt-DDNS.zip https://github.com/ymyuuu/openwrt-ddns/archive/refs/heads/main.zip &&
unzip /OpenWrt-DDNS/OpenWrt-DDNS.zip -d /OpenWrt-DDNS &&
mv /OpenWrt-DDNS/OpenWrt-DDNS-main/* /OpenWrt-DDNS/ &&
rm -rf /OpenWrt-DDNS/OpenWrt-DDNS-main &&
rm /OpenWrt-DDNS/OpenWrt-DDNS.zip &&
rm /OpenWrt-DDNS/README.md &&
rm /OpenWrt-DDNS/LICENSE &&
cd /OpenWrt-DDNS &&
python3 update.py &&
python3 menu.py

```

上述命令将执行以下操作：

1. 创建 `/OpenWrt-DDNS` 目录（如果不存在）。
2. 清空 `/OpenWrt-DDNS` 目录下的所有内容。
3. 使用 `wget` 下载 OpenWrt DDNS 源代码压缩包，并将其保存为 `/OpenWrt-DDNS/openwrt-ddns.zip`。
4. 使用 `unzip` 解压缩源代码压缩包到 `/OpenWrt-DDNS` 目录。
5. 将解压缩后的文件移动到 `/OpenWrt-DDNS` 目录。
6. 删除不再需要的文件和目录。
7. 切换到 `/openwrt-ddns` 目录。
8. 使用 `python3` 运行 `update.py` 脚本以更新配置。
9. 使用 `python3` 运行 `menu.py` 脚本以启动菜单界面。

请根据实际需求修改配置文件和参数。

## 后续操作

在安装完成后，如果后续需要运行 OpenWrt DDNS，可以直接执行以下命令：

```shell
cd /OpenWrt-DDNS && python3 update.py && python3 main.py

```

上述命令将切换到 `/OpenWrt-DDNS` 目录，并依次运行 `update.py` 和 `main.py` 脚本。

如果需要定时运行 OpenWrt DDNS，可以将以下内容添加到 OpenWrt 的计划任务中：

```
0 * * * * cd /OpenWrt-DDNS && python3 update.py && python3 main.py
```

这将使 OpenWrt 每小时执行一次 `/OpenWrt-DDNS` 目录下的 `update.py` 和 `main.py` 脚本。

## 自定义测速 IP

如果您需要自定义测速 IP，请按照以下步骤进行操作：

1. 打开 `/OpenWrt-DDNS` 目录。
2. 找到名为 `ip.txt` 的文件。
3. 使用文本编辑器打开 `ip.txt` 文件。
4. 在文件中输入您想要使用的测速 IP 地址。
5. 保存并关闭 `ip.txt` 文件。

**请确保您输入的测速 IP 地址格式正确，并且每个 IP 地址占据一行。**

**在编辑自定义测速 IP 列表完成后，您必须执行以下命令来运行自定义测速 IP 列表的 OpenWrt DDNS：**

```shell
cd /OpenWrt-DDNS && python3 main.py

```

上述命令将切换到 `/OpenWrt-DDNS` 目录，并运行 `main.py` 脚本。

OpenWrt DDNS 将使用您在 `ip.txt` 文件中指定的测速 IP 地址来进行测速和更新。

## 免责声明

**在使用本指南提供的信息和指令之前，请您务必仔细阅读并理解以下免责声明：**

1. OpenWrt DDNS 是一个第三方开发的项目，作者不对该项目的功能、安全性或可靠性提供任何担保或保证。使用 OpenWrt DDNS 时请自行承担风险。
2. 在安装和配置 OpenWrt DDNS 之前，请确保您已备份重要的系统和数据。OpenWrt DDNS 的安装和配置可能会对您的设备和网络环境产生影响，包括但不限于数据丢失、网络中断等问题。
3. OpenWrt DDNS 的使用可能涉及到您的网络设置和域名解析服务商的配置。请确保您已获得相关的授权和权限，并按照服务提供商的规定使用该服务。
4. OpenWrt DDNS 的安装和配置可能需要您对系统进行修改和调整。请确保您具备相应的技术知识和经验，并在操作之前充分了解相关的指令和操作风险。
5. **服务对象限定：** 本指南仅针对非中国大陆地区用户提供。中国大陆地区用户不得使用本指南提供的信息和指令。
6. OpenWrt DDNS 不对因使用本指南提供的信息和指令而导致的任何直接或间接损失或损害承担任何责任。

**请在使用 OpenWrt DDNS 之前仔细考虑，并自行评估风险和可行性。如果您对安装和配置有任何疑问或担忧，请咨询专业人士或寻求技术支持。**

## 许可证

本项目采用 MIT 许可证。详细信息请参阅 [LICENSE](LICENSE) 文件。

感谢你的使用！如果你对这个项目有任何改进或建议，也欢迎贡献代码或提出问题。
