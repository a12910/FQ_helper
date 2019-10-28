import itchat
import json
import itchat_class, itchat_transfer

DB = {}
listen_groups = []
logs = []

def main():
    global DB, listen_groups
    itchat.auto_login(True)
    f = open('db.JSON', encoding='utf-8')
    DB = json.loads(f.read())
    for department in DB['departments']:
        # 载入学院信息
        for group in department['groups']:
            group_search = itchat.search_chatrooms(name=group['group_name'])
            if len(group_search) == 0:
                print(group['group_name']+' not found')
            else:
                group['id'] = group_search[0]['UserName']
                listen_groups.append(group['id'])

            print(group['id'])

    center = DB['users']['center_group']
    DB['users']['center_group']['id'] = itchat.search_chatrooms(name=center['name'])[0]['UserName']
    print('init finished')
    itchat_class.DB = DB
    itchat_transfer.DB = DB
    itchat.run()

def send_msg(msgs, room):
    for m in msgs:
        itchat.send(m, room)

@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def recieve_help(msg):
    """主程序"""
    global DB, listen_groups, logs

    # 不属于监听群则取消
    if not msg['FromUserName'] in listen_groups:
        return
    print(msg)

    msg_log = {
        "user_id":msg['ActualUserName'],
        "group_id":msg['FromUserName'],
    }

    # 未完成作业
    now_log = None
    for logg in logs:
        if logg.is_equ(msg_log):
            now_log = logg

    # 建立新作业
    if now_log is None and msg['Content'] in DB['languages']['basic']['init_key']:
        new_log = itchat_class.Logg(msg_log)
        result, state = new_log.next()
        send_msg(result, msg['FromUserName'])

        logs.append(new_log)
        return

    if now_log is None:
        return


    if msg['Content'] in DB['languages']['basic']['quit_key']:
        # 退出
        del_log(now_log, True, msg['FromUserName'])
    else:
        # 下一步
        result, state = now_log.next(msg['Content'])
        print(result, state)
        send_msg(result, msg['FromUserName'])
        if not state:
            del_log(now_log, True, msg['FromUserName'])
    pass

def del_log(log, is_msg, room):
    # 结束任务
    global logs, DB
    logs.remove(log)
    del log
    if is_msg:
        send_msg(DB['languages']['basic']['quit_word'], room)



if __name__ == '__main__':
    main()