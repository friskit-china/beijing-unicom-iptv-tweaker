# 北京联通IPTV相关脚本。

项目进行中。
敬请期待具体教程（尤其是user_token的获取方法）。

不想跑code的话可以直接用iptv_channel.m3u这个我抽取好的列表文件（我在2020年5月25日直接通过机顶盒抓包抽取的），用法和[bj-unicom-iptv.m3u](https://gist.github.com/sdhzdmzzl/93cf74947770066743fff7c7f4fc5820)一样。

然而我发现[bj-unicom-iptv.m3u](https://gist.github.com/sdhzdmzzl/93cf74947770066743fff7c7f4fc5820)的网段是239.3.0.0/16，直接用rdp组播的方式打开就能流畅运行。而我抓包得到的地址网段是239.2.0.0/16，然而用rdp协议打开会发现这些频道都非常卡。然而电视用了同样的频道却完全不卡。。。然后我发现用udpxy转发成http协议之后也完全不卡。。。所以建议用239.2.0.0/16时开启udpxy的转发。

## 功能
## 使用教程 
