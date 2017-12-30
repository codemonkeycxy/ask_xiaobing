# coding=utf8
# 使用前需关注小冰公众号
# inspired by: https://github.com/Lafree317/PythonChat/blob/master/chat.py
# also referred to: https://zhuanlan.zhihu.com/p/30899907

import itchat
from itchat.content import *
from collections import deque


WAKEN_MSG = [u"小冰", u"小冰小冰", u"小冰呢", u"小冰呢？", u"小冰回来", u"小冰出来"]
HIBERNATE_MSG = [u"小冰住嘴", u"小冰闭嘴", u"滚", u"你滚", u"你闭嘴", u"下去吧"]
TRIGGER_MSG = WAKEN_MSG + HIBERNATE_MSG


def debug_print(msg):
    if debug:
        print(msg)


# wrapper around itchat's weird way of image forwarding
def send_img(msg, user_name):
    msg['Text'](msg['FileName'])
    itchat.send_image(msg['FileName'], user_name)


def ask_xiaobing(msg):
    if msg['Content'] in TRIGGER_MSG:
        # don't ask xiaobing with trigger message
        return

    if msg['Type'] == 'Picture':
        send_img(msg, xiao_bing_user_name)
    else:
        itchat.send_msg(msg['Text'], xiao_bing_user_name)


def get_user_display_name(user):
    if user:
        return user['RemarkName'] or user['NickName'] or user['Name']
    else:
        return 'user not found'


# to turn robot on/off
def handle_robot_switch(incoming_msg, outgoing_msg_target_user):
    global peer_list

    if not outgoing_msg_target_user:
        debug_print(u'Outgoing message target user not recognized. Can\'t turn on/off robot')
        return

    display_name = get_user_display_name(outgoing_msg_target_user)
    user_id_name = outgoing_msg_target_user['UserName']

    if incoming_msg['Content'] in WAKEN_MSG:
        if user_id_name not in peer_list:
            debug_print(u'Turning on robot for {}'.format(display_name))
            peer_list.add(user_id_name)
            itchat.send_msg(u'小冰: 我在这儿呢^_^', user_id_name)
        else:
            debug_print(u'Robot is already turned on for {}'.format(display_name))
    elif incoming_msg['Content'] in HIBERNATE_MSG:
        if user_id_name in peer_list:
            debug_print(u'Turning off robot for {}'.format(display_name))
            peer_list.remove(user_id_name)
            itchat.send_msg(u'小冰: (默默走开>.<)', user_id_name)
        else:
            debug_print(u'Robot is already turned off for {}'.format(display_name))


def handle_xiaobing_reply(msg):
    global contact_queue, last_contact

    if not last_contact:
        debug_print('Xiaobing replied but has no one to contact')
        return

    # allow xiaobing to send multiple replies to the last contact
    asker_id_name = contact_queue.popleft() if len(contact_queue) > 0 else last_contact
    asker = itchat.search_friends(userName=asker_id_name)

    if msg['Type'] == 'Picture':
        debug_print(u'xiaobing replied a picture. Relaying to {}'.format(get_user_display_name(asker)))
        itchat.send_msg(u'小冰: 看图', asker_id_name)
        send_img(msg, asker_id_name)
    else:
        debug_print(u'xiaobing replied {}. Relaying to {}'.format(msg['Text'], get_user_display_name(asker)))
        itchat.send_msg(u'小冰: {}'.format(msg['Text']), asker_id_name)


def is_my_outgoing_msg(msg):
    return msg['FromUserName'] == my_user_name


# handle robot switch and friends messages
@itchat.msg_register([TEXT, PICTURE], isFriendChat=True)
def text_reply(msg):
    global peer_list, contact_queue, last_contact

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
            contact_queue.append(msg['FromUserName'])
            last_contact = msg['FromUserName']
            ask_xiaobing(msg)


# relay back xiaobing's response
@itchat.msg_register([TEXT, PICTURE], isMpChat=True)
def map_reply(msg):
    if msg['FromUserName'] == xiao_bing_user_name:
        handle_xiaobing_reply(msg)


if __name__ == '__main__':
    itchat.auto_login()

    my_user_name = itchat.get_friends(update=True)[0]["UserName"]
    xiao_bing_user_name = itchat.search_mps(name=u'小冰')[0]["UserName"]

    peer_list = set()
    contact_queue = deque()
    last_contact = None
    debug = True

    itchat.run()
