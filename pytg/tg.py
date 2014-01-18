# -*- coding: utf-8 -*-
from types import GeneratorType
from datetime import datetime
from utils import *
from regex import *

@coroutine
def dialog_list(target):
    if type(target) is not GeneratorType:
        raise TypeError('target must be GeneratorType')
    try:
        while True:
            line = (yield)
            if '{print_message}' in line or '{end_print_message}' in line or \
               '{user_status}' in line:
                continue
            m = unread_user.search(clear_prompt(remove_color(line)).strip())
            if m:
                if m.group('uid'):
                    user, uid = m.group('user'), m.group('uid')
                    cmduser = user.replace(' ', '_')
                else:
                    user, cmduser, uid = None, None, m.group('user')
                unread = m.group('unread')
                arg = {'type': 'dialog_list', 'uid': uid, 'user': user, 'cmduser': cmduser, 'unread': unread}
                target.send(arg)
                continue
            m = unread_chat.search(clear_prompt(remove_color(line)).strip())
            if m:
                if m.group('gid'):
                    group, gid = m.group('group'), m.group('gid')
                    cmdgroup = group.replace(' ', '_')
                else:
                    group, cmdgroup, gid = None, None, m.group('group')
                unread = m.group('unread')
                arg = {'type': 'dialog_list', 'gid': gid, 'group': group, 'cmdgroup': cmdgroup, 'unread': unread}
                target.send(arg)
                #sys.stdout.write('User info -> User: %s, Unread: %s\n' % (user, unread))
                #sys.stdout.flush()
    except GeneratorExit:
        pass
        #sys.stdout.write('dialog_info_user coroutine exit cleanly\n')
        #sys.stdout.flush()

@coroutine
def chat_info(target):
    if type(target) is not GeneratorType:
        raise TypeError('target must be GeneratorType')
    try:
        while True:
            line = (yield)
            if '{print_message}' in line or '{end_print_message}' in line or \
               '{user_status}' in line:
                continue
            m = chat_info_header.search(clear_prompt(remove_color(line)).strip())
            if m:
                if m.group('gid'):
                    group, gid = m.group('group'), m.group('gid')
                    cmdgroup = group.replace(' ', '_')
                else:
                    group, cmdgroup, gid = None, None, m.group('group')
                arg = {'type': 'chat_info', 'group': group,
                    'cmdgroup': cmdgroup, 'gid': gid}
                target.send(arg)
                continue
            m = chat_info_body.search(clear_prompt(remove_color(line)).strip())
            if m:
                if m.group('uid'):
                    user, uid = m.group('user'), m.group('uid')
                    cmduser = user.replace(' ', '_')
                else:
                    user, usercmd, uid = None, None, m.group('user')
                if m.group('iuid'):
                    iuser, iuid = m.group('iuser'), m.group('iuid')
                    cmdiuser = iuser.replace(' ', '_')
                else:
                    iuser, cmdiuser, iuid = None, None, m.group('iuser')
                timestamp = datetime(int(m.group('yr')), int(m.group('mth')),
                    int(m.group('day')), int(m.group('hr')),
                    int(m.group('min')), int(m.group('sec')))
                arg = {
                    'type': 'chat_info_member', 'group': group, 'gid': gid,
                    'user': user, 'cmduser': cmduser, 'uid': uid,
                    'iuser': iuser, 'cmdiuser': cmdiuser, 'iuid': uid,
                    'timestamp': timestamp
                }
                target.send(arg)
    except GeneratorExit:
        pass
        #sys.stdout.write('chat_info coroutine exit cleanly\n')
        #sys.stdout.flush()

@coroutine
def message(target):
    if type(target) is not GeneratorType:
        raise TypeError('target must be GeneratorType')
    try:
        while True:
            line = (yield)
            if '{print_message}' not in line or '{end_print_message}' not in line:
                continue
            m = print_message.search(clear_prompt(remove_color(line)).strip())
            if m:
                arg = {
                    'type': 'message', 'msgid': m.group('msgid'),
                    'timestamp': m.group('timestamp'),
                    'message': m.group('message')
                }
                tmpchat, tmpuser = m.group('chat'), m.group('user')
                arg['peer'] = 'group' if tmpchat else 'user'
                if tmpchat:
                    if '#' in tmpchat:
                        arg['group'], arg['gid'] = tmpchat.split('#')
                    else:
                        arg['group'], arg['gid'] = None, tmpchat
                if '#' in tmpuser:
                    arg['user'], arg['uid'] = tmpuser.split('#')
                else:
                    arg['user'], arg['uid'] = None, tmpuser
                if arg['peer'] == 'user':
                    arg['ownmsg'] = True if m.group('dir') == '«««' else False
                target.send(arg)
    except GeneratorExit:
        pass
        #sys.stdout.write('group_post coroutine exit cleanly\n')
        #sys.stdout.flush()

@coroutine
def user_status(target):
    if type(target) is not GeneratorType:
        raise TypeError('target must be GeneratorType')
    try:
        while True:
            line = (yield)
            if '{user_status}' not in line:
                continue
            m = user_status.search(clear_prompt(remove_color(line)).strip())
            if m:
                user, uid, status = m.group('user'), m.group('uid'), m.group('status')
                if not uid:
                    uid, user = user, None
                arg = {
                    'type': 'user_status', 'uid': uid, 'user': user
                }
                target.send(arg)
    except GeneratorExit:
        pass
        #sys.stdout.write('group_post coroutine exit cleanly\n')
        #sys.stdout.flush()