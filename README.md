# 北京联通IPTV相关脚本。

## 功能
一个用来从北京联通IPTV专网上自动下载频道列表并生成m3u播放列表的脚本

不想跑code的话可以直接用iptv_channel.m3u这个我抽取好的列表文件（可能会偶尔更新），用法和[bj-unicom-iptv.m3u](https://gist.github.com/sdhzdmzzl/93cf74947770066743fff7c7f4fc5820)一样。


## 使用教程 

首先根据[这篇](http://127.0.0.1:4000/2020/05/31/bjunicom-network.html#%E8%8E%B7%E5%8F%96iptv%E9%A2%91%E9%81%93%E5%88%97%E8%A1%A8%E7%9A%84%E8%84%9A%E6%9C%AC)文章里写的通过抓包获取到适合你的IPTV专网鉴权地址和UserToken。（这个UserToken应该能生效很久，所以「一次抓包、长久使用」）。

然而我发现[bj-unicom-iptv.m3u](https://gist.github.com/sdhzdmzzl/93cf74947770066743fff7c7f4fc5820)的网段是239.3.0.0/16，直接用rdp组播的方式打开就能流畅运行。而我抓包得到的地址网段是239.2.0.0/16，然而用rdp协议打开会发现这些频道都非常卡。然而电视用了同样的频道却完全不卡。。。然后我发现用udpxy转发成http协议之后也完全不卡。。。所以建议用239.2.0.0/16时开启udpxy的转发。所以这个脚本对生成udpxy的prefix进行了优化。

然后执行脚本：

```
# 生成udp播放列表：
python3 main.py --user_token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx --auth_server "http://210.13.0.147:8080" --output_channel_playlist_filename "iptv_channel.udp.m3u"

# 生成udpxy播放列表，需要指明--udpxy_base_url参数
python3 main.py --user_token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx --auth_server "http://210.13.0.147:8080" --udpxy_base_url "http://192.168.2.1:4022/udp/" --output_channel_playlist_filename "iptv_channel.udpxy.m3u"
```

默认的参数除了user_token之外都可以用默认值或者例子中的值。

其中参数：

--user_token 就是UserToken

--auth_server 鉴权服务器的prefix

--udpxy_base_url udpxy的prefix，如果设置了这个参数，则生成的播放列表前面都会加上这个prefix。需要在路由器上安装udpxy之后才能正常使用。

--output_channel_playlist_filename 生成播放列表文件名

## Future Work

有空的话打算做成OpenWRT KoolShare软件中心插件或者OpenWRT的软件包，每天自动更新列表，让IINA能够直接打开播放。也欢迎大神来贡献code哈～