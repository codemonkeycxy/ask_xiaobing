# ask_xiaobing
WeChat bot powered by MS XiaoBing (小冰) 一个简单的微信自动回复机器人

快速入门（非开发者)：
1. 微信关注小冰公众号 (普通小冰公众号只支持纯文字，需[领养一只小冰](http://www.msxiaoice.com/)之后才能识图哦)
2. 下载运行文件，打开并扫码：
    - windows: [链接](https://github.com/codemonkeycxy/ask_xiaobing/blob/master/dist/ask_xiaobing_win-64.exe)
    - mac: [链接](https://github.com/codemonkeycxy/ask_xiaobing/blob/master/dist/ask_xiaobing)

快速入门（开发者）：
1. 微信关注小冰公众号 (普通小冰公众号只支持纯文字，需[领养一只小冰](http://www.msxiaoice.com/)之后才能识图哦)
2. `brew install python`
3. `pip install itchat`
4. `python ask_xiaobing.py`

人机对话：

![webp net-resizeimage 2](https://user-images.githubusercontent.com/32557706/34453150-0cc4b506-ed01-11e7-86d3-e705e12e8bc8.jpg)

两只小冰左右互搏：

![webp net-resizeimage 3](https://user-images.githubusercontent.com/32557706/34457303-6f47b902-ed61-11e7-9e00-62a575ad9faa.jpg)

综合借鉴了下面这些资源：
1. https://github.com/Lafree317/PythonChat/blob/master/chat.py
2. https://zhuanlan.zhihu.com/p/30899907

已知问题：
1. 多人同时和小冰讲话时会串号 (理论上已解决，待测试)
2. 本小冰目前还不能回传语音 （api目前还不能支持）
3. exe文件在64位的win7下不能运行
