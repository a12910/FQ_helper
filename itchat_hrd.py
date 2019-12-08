import itchat
import json
import itchat_class, itchat_transfer
import itchat_db as db

# DB = {}
# listen_groups = []
# logs = []

def main():

    itchat.auto_login(True)
    db.load_DB()

    for department in db.DB['departments']:
        # 载入学院信息
        for group in department['groups']:
            group_search = itchat.search_chatrooms(name=group['group_name'])
            if len(group_search) == 0:
                print(group['group_name']+' not found')
            else:
                group['id'] = group_search[0]['UserName']
                db.listen_groups.append(group['id'])

            print(group['id'])

    center = db.DB['users']['center_group']
    db.DB['users']['center_group']['id'] = itchat.search_chatrooms(name=center['name'])[0]['UserName']
    print('init finished')
    itchat.run()

def send_msg(msgs, room):
    # for m in msgs:
    #     for n in m[0]:
    #         itchat.send(n, m[1])

    for m in msgs:
        itchat.send(m, room)

@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def recieve_help(msg):
    """主程序"""

    # 不属于监听群则取消
    if not msg['FromUserName'] in db.listen_groups:
        return
    print(msg)

    msg_log = {
        "user_id":msg['ActualUserName'],
        "group_id":msg['FromUserName'],
    }

    # 删除过期回话
    time_check()

    # 未完成作业
    now_log = None
    for logg in db.logs:
        if logg.is_equ(msg_log):
            now_log = logg

    # 建立新作业
    if now_log is None and msg['Content'] in db.DB['languages']['basic']['init_key']:
        new_log = itchat_class.Logg(msg_log)
        result, state = new_log.next()
        send_msg(result, msg['FromUserName'])

        db.logs.append(new_log)
        return

    if now_log is None:
        return


    if msg['Content'] in db.DB['languages']['basic']['quit_key']:
        # 退出
        del_log(now_log, True, msg['FromUserName'])
    else:
        # 下一步
        result, state = now_log.next(msg['Content'])
        print(result, state)
        send_msg(result, msg['FromUserName'])
        if not state:
            del_log(now_log, True, msg['FromUserName'])

def time_check():
    move = []
    for item in db.logs:
        if not item.update_timer(False):
            move.append(item)
    for i in move:
        del_log(i, False)


def del_log(log, is_msg, room=None):
    # 结束任务
    db.logs.remove(log)
    del log
    if is_msg and not room is None:
        send_msg(db.DB['languages']['basic']['quit_word'], room)



if __name__ == '__main__':
    main()