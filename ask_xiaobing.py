# coding=utf8
# 使用前需关注小冰公众号
# inspired by: https://github.com/Lafree317/PythonChat/blob/master/chat.py
# also referred to: https://zhuanlan.zhihu.com/p/30899907

import itchat
from itchat.content import *


WAKEN_MSG = [u"小冰", u"小冰小冰", u"小冰呢", u"小冰呢？", u"小冰回来", u"小冰出来"]
HIBERNATE_MSG = [u"小冰住嘴", u"小冰闭嘴", u"滚", u"你滚", u"你闭嘴", u"下去吧"]
TRIGGER_MSG = WAKEN_MSG + HIBERNATE_MSG

# --------------------------------------------- Handle Friend Chat ---------------------------------------------------


@itchat.msg_register([TEXT, PICTURE], isFriendChat=True)
def text_reply(msg):
    """ handle robot switch and friends messages """
    to_user = itchat.search_friends(userName=msg['ToUserName'])
    from_user = itchat.search_friends(userName=msg['FromUserName'])

    if is_my_outgoing_msg(msg):
        handle_outgoing_msg(msg, to_user, from_user)
    else:  # this is an incoming message from my friend
        handle_incoming_msg(msg, to_user, from_user)


def handle_outgoing_msg(msg, to_user, from_user):
    debug_print(u'I sent a message {} to {}'.format(msg['Text'], get_user_display_name(to_user)))
    if msg['Content'] in TRIGGER_MSG:
        handle_robot_switch(msg, to_user)


def handle_incoming_msg(msg, to_user, from_user):
    global last_asker_id_name

    debug_print(u'I received a message {} from {}'.format(msg['Text'], get_user_display_name(from_user)))
    if msg['Content'] in TRIGGER_MSG:
        handle_robot_switch(msg, from_user)
    else:  # don't ask xiaobing with trigger question
        if msg['FromUserName'] in peer_list:
            debug_print(u'Robot reply is on for {}! Asking xiaobing...'.format(get_user_display_name(from_user)))
            last_asker_id_name = msg['FromUserName']
            ask_xiaobing(msg)


def handle_robot_switch(incoming_msg, outgoing_msg_target_user):
    """ Turn robot on/off according to the trigger message """
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

# --------------------------------------------- Handle Xiaobing Reply ------------------------------------------------


@itchat.msg_register([TEXT, PICTURE], isMpChat=True)
def map_reply(msg):
    """ relay back xiaobing's response """
    if msg['FromUserName'] == xiao_bing_user_name:
        handle_xiaobing_reply(msg)


def handle_xiaobing_reply(msg):
    global last_asker_id_name

    if not last_asker_id_name:
        debug_print('Xiaobing replied but has no one to contact')
        return

    asker = itchat.search_friends(userName=last_asker_id_name)
    if msg['Type'] == 'Picture':
        debug_print(u'xiaobing replied a picture. Relaying to {}'.format(get_user_display_name(asker)))
        itchat.send_msg(u'小冰: 看图', last_asker_id_name)
        send_img(msg, last_asker_id_name)
    else:
        debug_print(u'xiaobing replied {}. Relaying to {}'.format(msg['Text'], get_user_display_name(asker)))
        itchat.send_msg(u'小冰: {}'.format(msg['Text']), last_asker_id_name)

# --------------------------------------------- Helper Functions ---------------------------------------------------


def debug_print(msg):
    if debug:
        print(msg)


def send_img(msg, user_name):
    """ wrapper around itchat's weird way of image forwarding """
    msg['Text'](msg['FileName'])
    itchat.send_image(msg['FileName'], user_name)


def ask_xiaobing(msg):
    if msg['Type'] == 'Picture':
        send_img(msg, xiao_bing_user_name)
    else:
        itchat.send_msg(msg['Text'], xiao_bing_user_name)


def get_user_display_name(user):
    if user:
        return user['RemarkName'] or user['NickName'] or user['Name']
    else:
        return 'user not found'


def is_my_outgoing_msg(msg):
    return msg['FromUserName'] == my_user_name


if __name__ == '__main__':
    itchat.auto_login()

    my_user_name = itchat.get_friends(update=True)[0]["UserName"]
    xiao_bing_user_name = itchat.search_mps(name=u'小冰')[0]["UserName"]

    peer_list = set()
    last_asker_id_name = None
    debug = True

    itchat.run()
