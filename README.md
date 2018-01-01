# ask_xiaobing
WeChat bot powered by MS XiaoBing via [itchat](https://github.com/littlecodersh/ItChat) (小冰) 
一个利用itchat接口制作的微信自动回复机器人

快速入门（非开发者)：
1. 微信关注小冰公众号
2. 下载运行文件，打开并扫码：
    - windows: [链接](https://github.com/codemonkeycxy/ask_xiaobing/blob/master/dist/ask_xiaobing_win-64.exe)
    - mac: [链接](https://github.com/codemonkeycxy/ask_xiaobing/blob/master/dist/ask_xiaobing_mac.zip)
3. 小冰唤醒方式：在对话中输入下列任意 ["小冰", "小冰小冰", "小冰呢", "小冰呢？", "小冰回来", "小冰出来"]
4. 小冰休眠方式：在对话中输入下列任意 ["小冰住嘴", "小冰闭嘴", "滚", "你滚", "你闭嘴", "下去吧", "小冰下去", "小冰退下"]

快速入门（开发者）：
1. 微信关注小冰公众号
2. `git clone https://github.com/codemonkeycxy/ask_xiaobing.git`
3. `brew install python`
4. `pip install itchat`
5. 进入ask_xiaobing文件夹并运行`python ask_xiaobing.py`

人机对话：

![webp net-resizeimage 2](https://user-images.githubusercontent.com/32557706/34453150-0cc4b506-ed01-11e7-86d3-e705e12e8bc8.jpg)

两只小冰左右互搏：

![webp net-resizeimage 3](https://user-images.githubusercontent.com/32557706/34457303-6f47b902-ed61-11e7-9e00-62a575ad9faa.jpg)

综合借鉴了下面这些资源：
1. https://github.com/Lafree317/PythonChat/blob/master/chat.py (在此基础上增加了message queue，解决了多人同时和小冰聊天时串号的问题)
2. https://zhuanlan.zhihu.com/p/30899907

已知问题：
1. 本小冰目前还不能回传语音 （itchat api目前还不能支持）
