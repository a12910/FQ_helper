from itchat_hrd import logs
import itchat_transfer
import itchat

DB = {}

class Logg:
    from_user = {}
    to_user = {}
    state = 'null'

    def __init__(self, user):
        self.from_user = user
        self.transfer = itchat_transfer.load()

    def next(self, string='find'):
        """下一步"""
        global DB
        find_lau = DB['languages']['find']
        itchat_transfer.find_lau = find_lau
        if self.state == 'null' and string == 'find' :
            self.change_state('find_start')
        return self.transfer[self.state](self, string)

    def change_state(self, new_state, str=''):
        """改变状态"""
        print(self.state + ' -> ' + new_state + ' ' + str)
        self.state = new_state

    def send_msg(self, string):
        """独立发送信息"""
        global DB
        if string == 'find':
            send_str01 = DB['languages']['find']['find_send']
            send_str02 = DB['languages']['find']['find_send2']
            send_str1 =  send_str01[0] % (self.to_user['name'], self.to_user['name_id'], self.to_user['department_info']['dep_contact'])
            send_str2 =  send_str02[0] % (self.to_user['name'], self.to_user['name_id'], self.to_user['department_info']['main_name'], self.to_user['contact'])
            itchat.send(send_str1, self.to_user['department_info']['id'])
            itchat.send(send_str2, DB['users']['center_group']['id'])
            pass


    def is_yes(self, string):
        """判断是/否"""
        yess = ['是', '确认','yes','Yes']
        # nos = ['否','不确认', 'no', 'No']
        return string in yess


    def is_equ(self, msg_log):
        """判断是否为相同log"""
        if msg_log['user_id'] == self.from_user['user_id'] and \
            msg_log['group_id'] == self.from_user['group_id']:
            return True
        else:
            return False



    def __del__(self):
        pass