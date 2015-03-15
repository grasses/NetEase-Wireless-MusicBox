# 关于

NetEase Wireless MusicBox是一个基于网易云音乐API的无线音箱系统。

系统包括树莓派服务器，手机web客户端，两者必须在一个网段内，通过web搜索、播放音乐。

详细情况可以看这篇文章：[《基于网易云音乐API的无线音箱》](http://homeway.me/2015/03/15/netease-wireless-music-box/)

<hr><br>

# 效果演示

![MusicBox](http://homeway.me/image/2015-03-15-netease-wireless-music-box-01.jpg)

<br>

![MusicBox](http://homeway.me/image/2015-03-15-netease-wireless-music-box-02.jpg)

<br>

![MusicBox](http://homeway.me/image/2015-03-15-netease-wireless-music-box-03.jpg)

<br>

<video src="http://homeway.mexiaocao.u.qiniudn.com/@/blog/netease-wireless-music-box.mp4" controls="controls"></video>


<br><hr><br>

# 设备原理

![MusicBox](http://homeway.me/image/2015-03-15-netease-wireless-music-box-04.png)

树莓派做服务器，手机web端作为客户端，两者必须在一个网段内。

服务器端使用Python的框架Tornado作为web访问，pygame模块负责播放音乐，所有音乐信息均采用网易云音乐API。

关于网易云音乐api是不开放的，用的是一位前辈写过的api改编，前辈api被网易封了，网易后来加了个csrf防护。

<hr><br>

# 更新日志

15.03.15 

* Demo版：完成基本搜索、播放、调节音量功能

* 多线程切换音乐，防播放时卡死

# License

GPL
