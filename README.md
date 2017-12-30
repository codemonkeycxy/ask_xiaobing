# ask_xiaobing
WeChat bot powered by MS XiaoBing (小冰)

一个简单的微信自动回复机器人，使用前需要关注小冰公众号。
![img_0351](https://user-images.githubusercontent.com/32557706/34450087-1e7fddac-ecb6-11e7-9c1b-04be6333dfa4.JPG)

综合借鉴了下面这些资源：
1. https://github.com/Lafree317/PythonChat/blob/master/chat.py
2. https://zhuanlan.zhihu.com/p/30899907

目前的版本有一众比较明显的缺陷：
1. 如果同时收到来自两个不同联系人的信息，小冰会犯浑
2. 小冰只受host本人控制，对方无法通过“小冰呢”和“小冰闭嘴”打开或者关闭小冰
3. 小冰目前只支持纯文字，无法斗图
4. 即使小冰公众号回复了多条信息，当前版本只能回传其中一条
5. 小冰输入时不显示“对方正在输入”， 难以以假乱真
