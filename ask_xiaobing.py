# coding=utf8
# 使用前需关注小冰公众号
# inspired by: https://github.com/Lafree317/PythonChat/blob/master/chat.py
# also referred to: https://zhuanlan.zhihu.com/p/30899907

from __future__ import print_function
from threading import Timer
import itchat
import datetime
from itchat.content import *
from collections import deque

WAKEN_MSG = [u"小冰", u"小冰小冰", u"小冰呢", u"小冰呢？", u"小冰回来", u"小冰出来"]
HIBERNATE_MSG = [u"小冰住嘴", u"小冰闭嘴", u"滚", u"你滚", u"你闭嘴", u"下去吧", u"小冰下去", u"小冰退下"]
TRIGGER_MSG = WAKEN_MSG + HIBERNATE_MSG

FOLLOW_UP_Q_LIMIT = 2  # can ask at most 2 questions at a time

# --------------------------------------------- Handle Friend Chat ---------------------------------------------------


@itchat.msg_register([TEXT, PICTURE], isFriendChat=True)
def text_reply(msg):
    """ handle robot switch and friends messages """
    to_user = itchat.search_friends(userName=msg['ToUserName'])
    from_user = itchat.search_friends(userName=msg['FromUserName'])

    if is_my_outgoing_msg(msg):
        handle_outgoing_msg(msg, to_user)
    else:  # this is an incoming message from my friend
        handle_incoming_msg(msg, from_user)

@itchat.msg_register([TEXT,PICTURE], isGroupChat = True)
def group_reply(msg):
    from_user_name = msg['FromUserName']
    to_user_name = msg['ToUserName']
    if is_my_outgoing_msg(msg):
        group = itchat.search_chatrooms(userName=to_user_name)
        handle_outgoing_msg(msg, group)
    else:
        group = itchat.search_chatrooms(userName=from_user_name)
        handle_incoming_msg(msg, group)


def handle_outgoing_msg(msg, to_user):
    debug_print(u'I sent a message {} to {}'.format(msg['Text'], get_user_display_name(to_user)))
    if msg['Content'] in TRIGGER_MSG:
        handle_robot_switch(msg, to_user)


def handle_incoming_msg(msg, from_user):
    global peer_list

    debug_print(u'I received a message {} from {}'.format(msg['Text'], get_user_display_name(from_user)))
    if msg['Content'] in TRIGGER_MSG:
        handle_robot_switch(msg, from_user)
    else:  # don't ask xiaobing with trigger question
        if msg['FromUserName'] in peer_list:
            handle_message_queue(msg, from_user)


def handle_message_queue(msg, from_user):
    global message_queue

    from_user_id_name = msg['FromUserName']
    from_user_display_name = get_user_display_name(from_user)
    debug_print(u'Robot reply is on for {}! Adding message to queue...'.format(from_user_display_name))

    if len(message_queue) == 0:
        debug_print(u'No one has question for xiaobing yet. {} is the first!'.format(from_user_display_name))
        message_queue.append((from_user_id_name, [msg]))
    else:
        last_asker_id_name, last_questions = message_queue[-1]
        if last_asker_id_name == from_user_id_name and len(last_questions) < FOLLOW_UP_Q_LIMIT:
            debug_print(u'{} just asked a follow up question'.format(from_user_display_name))
            last_questions.append(msg)
        else:
            last_asker_display_name = get_user_display_name(user_id_name=last_asker_id_name)
            debug_print(u'{} has a question before {}. Queuing up...'.format(
                last_asker_display_name,
                from_user_display_name
            ))
            message_queue.append((from_user_id_name, [msg]))


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


@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isMpChat=True)
def map_reply(msg):
    """ relay back xiaobing's response """
    if msg['FromUserName'] == xiao_bing_user_name:
        handle_xiaobing_reply(msg)


def handle_xiaobing_reply(msg):
    global current_asker_id_name, last_xiaobing_response_ts, in_trans

    if not current_asker_id_name:
        debug_print('Xiaobing replied but has no one to contact')
        return

    last_xiaobing_response_ts = now()
    in_trans = False
    asker = itchat.search_friends(userName=current_asker_id_name)
    if msg['Type'] == 'Picture':
        debug_print(u'Xiaobing replied a picture. Relaying to {}'.format(get_user_display_name(asker)))
        send_img(msg, current_asker_id_name)
    elif msg['Type'] == 'Text':
        debug_print(u'Xiaobing replied {}. Relaying to {}'.format(msg['Text'], get_user_display_name(asker)))
        itchat.send_msg(u'小冰: {}'.format(msg['Text']), current_asker_id_name)
    else:
        # gracefully handle unsupported formats with generic reply
        debug_print(u'Xiaobing replied a {}, which is not yet supported'.format(msg['Type']))
        itchat.send_msg(u'小冰: 嘤嘤嘤', current_asker_id_name)


# ------------------------------------------ Message Queue Processor ------------------------------------------------


def process_message():
    global message_queue, current_asker_id_name, last_xiaobing_response_ts, in_trans

    if len(message_queue) == 0:
        # debug_print(u'Was asked to process message but the queue is empty')
        pass
    # if no one has asked xiaobing yet or xiaobing has been idle for 2 sec
    elif not last_xiaobing_response_ts or (not in_trans and now() - last_xiaobing_response_ts > datetime.timedelta(seconds=2)):
        current_asker_id_name, msgs = message_queue.popleft()
        debug_print(u'Xiaobing is available. Asking questions on behalf of {}'.format(
            get_user_display_name(user_id_name=current_asker_id_name)
        ))
        in_trans = True
        for i, msg in enumerate(msgs):
            debug_print(u'Question {}: {}'.format(i, msg['Text']))
            ask_xiaobing(msg)

    # check back in 1 sec
    Timer(1, process_message).start()


# --------------------------------------------- Helper Functions ---------------------------------------------------


def now():
    return datetime.datetime.now()


def debug_print(msg):
    if not debug:
        return

    try:
        print(u'{} {}'.format(now(), msg))
    except Exception as e:
        print(str(e))


def send_img(msg, user_name):
    """ wrapper around itchat's weird way of image forwarding """
    msg['Text'](msg['FileName'])
    itchat.send_image(msg['FileName'], user_name)


def ask_xiaobing(msg):
    if msg['Type'] == 'Picture':
        send_img(msg, xiao_bing_user_name)
    else:
        text = msg['Text']
        if text and text.startswith(u'小冰: '):
            # remove dialog prefix when bots talk to each other
            text = text.replace(u'小冰: ', '')
        itchat.send_msg(text, xiao_bing_user_name)


def get_user_display_name(user=None, user_id_name=None):
    if user:
        return user['RemarkName'] or user['NickName'] or user['Name']
    elif user_id_name:
        return get_user_display_name(user=itchat.search_friends(userName=user_id_name))
    else:
        return 'user not found'


def is_my_outgoing_msg(msg):
    return msg['FromUserName'] == my_user_name


if __name__ == '__main__':
    itchat.auto_login()

    my_user_name = itchat.get_friends(update=True)[0]["UserName"]
    xiao_bing_user_name = itchat.search_mps(name=u'小冰')[0]["UserName"]

    peer_list = set()
    message_queue = deque()
    current_asker_id_name = None
    last_xiaobing_response_ts = None
    debug = True
    in_trans = False

    process_message()
    itchat.run()
