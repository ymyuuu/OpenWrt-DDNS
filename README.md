# OpenWrt DDNS 安装指南

本指南将介绍如何在 OpenWrt 上安装和配置 DDNS（动态域名解析）服务。

## 依赖

在开始安装之前，请确保已安装以下依赖：

```shell
opkg update
opkg install wget unzip python3
```

## 安装步骤

执行以下命令以安装 OpenWrt DDNS：

```shell
mkdir -p /openwrt-ddns \
&& rm -rf /openwrt-ddns/* \
&& wget -O /openwrt-ddns/openwrt-ddns.zip https://ymy.gay/https://github.com/ymyuuu/openwrt-ddns/archive/refs/heads/main.zip \
&& unzip /openwrt-ddns/openwrt-ddns.zip -d /openwrt-ddns \
&& mv /openwrt-ddns/openwrt-ddns-main/* /openwrt-ddns/ \
&& rm -rf /openwrt-ddns/openwrt-ddns-main \
&& rm /openwrt-ddns/openwrt-ddns.zip \
&& cd /openwrt-ddns \
&& python3 update.py \
&& python3 menu.py
```

上述命令将执行以下操作：

1. 创建 `/openwrt-ddns` 目录（如果不存在）。
2. 清空 `/openwrt-ddns` 目录下的所有内容。
3. 使用 `wget` 下载 OpenWrt DDNS 源代码压缩包，并将其保存为 `/openwrt-ddns/openwrt-ddns.zip`。
4. 使用 `unzip` 解压缩源代码压缩包到 `/openwrt-ddns` 目录。
5. 将解压缩后的文件移动到 `/openwrt-ddns` 目录。
6. 删除不再需要的文件和目录。
7. 切换到 `/openwrt-ddns` 目录。
8. 使用 `python3` 运行 `update.py` 脚本以更新配置。
9. 使用 `python3` 运行 `menu.py` 脚本以启动菜单界面。

请根据实际需求修改配置文件和参数。

## 后续操作

在安装完成后，如果需要运行 OpenWrt DDNS，可以执行以下命令：

```shell
cd /Mingyu && python3 ip.py && python3 main.py
```

上述命令将切换到 `/Mingyu` 目录，并依次运行 `update.py` 和 `main.py` 脚本。

如果需要定时运行 OpenWrt DDNS，可以将以下内容添加到 OpenWrt 的计划任务中：

```
0 * * * * cd /Mingyu && python3 update.py && python3 main.py
```

这将使 OpenWrt 每小时执行一次 `/Mingyu` 目录下的 `update.py` 和 `main.py` 脚本。

