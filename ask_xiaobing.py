# 使用前需关注小冰公众号
# inspired by: https://github.com/Lafree317/PythonChat/blob/master/chat.py
# also referred to: https://zhuanlan.zhihu.com/p/30899907

# coding=utf8
import itchat
from itchat.content import *


def debug_print(msg):
    if debug:
        print(msg)


def ask_xiaobing(msg):
    quest = msg.get('Text', 'Hey')
    itchat.send_msg(quest, xiaobingUserName)


def get_user_display_name(user):
    if user:
        return user['RemarkName'] or user['NickName'] or user['Name']
    else:
        return 'user not found'


# to turn robot on/off
def handle_robot_switch(incoming_msg, outgoing_msg_target_user):
    global peer_list

    display_name = get_user_display_name(outgoing_msg_target_user)
    user_id_name = outgoing_msg_target_user['UserName']

    if incoming_msg['Content'] in [u"小冰", u"小冰小冰", u"小冰呢", u"小冰呢？", u"小冰回来"]:
        if user_id_name not in peer_list:
            debug_print(u'Turning on robot for {}'.format(display_name))
            peer_list.add(user_id_name)
            itchat.send_msg(u'小冰: 我在这儿呢^_^', user_id_name)
        else:
            debug_print(u'Robot is already turned on for {}'.format(display_name))
    elif incoming_msg['Content'] in [u"小冰住嘴", u"小冰闭嘴", u"滚", u"你滚", u"你闭嘴"]:
        if user_id_name in peer_list:
            debug_print(u'Turning off robot for {}'.format(display_name))
            peer_list.remove(user_id_name)
            itchat.send_msg(u'小冰: (默默走开>.<)', user_id_name)
        else:
            debug_print(u'Robot is already turned off for {}'.format(display_name))


def is_my_outgoing_msg(msg):
    return msg['FromUserName'] == myUserName


# handle robot switch and friends messages
@itchat.msg_register(TEXT, isFriendChat=True)
def text_reply(msg):
    global peer_list, whosasking

    to_user = itchat.search_friends(userName=msg['ToUserName'])
    from_user = itchat.search_friends(userName=msg['FromUserName'])

    if is_my_outgoing_msg(msg):
        debug_print(u'I sent a message {} to {}'.format(msg['Text'], get_user_display_name(to_user)))
        handle_robot_switch(msg, to_user)
    else:  # this is an incoming message from my friend
        handle_robot_switch(msg, from_user)
        debug_print(u'I received a message {} from {}'.format(msg['Text'], get_user_display_name(from_user)))
        if msg['FromUserName'] in peer_list:
            debug_print(u'Robot reply is on for {}! Asking xiaobing...'.format(get_user_display_name(from_user)))
            whosasking = msg['FromUserName']
            ask_xiaobing(msg)


# relay back xiaobing's response
@itchat.msg_register(TEXT, isMpChat=True)
def map_reply(msg):
    global whosasking

    if whosasking and msg['FromUserName'] == xiaobingUserName:
        asker = itchat.search_friends(userName=whosasking)
        debug_print(u'xiaobing replied {}. Relaying to {}'.format(msg['Text'], get_user_display_name(asker)))
        itchat.send_msg(u'小冰: {}'.format(msg['Text']), whosasking)
        whosasking = None


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)

    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    xiaobingUserName = itchat.search_mps(name=u'小冰')[0]["UserName"]

    peer_list = set()
    whosasking = None
    debug = True

    itchat.run()
