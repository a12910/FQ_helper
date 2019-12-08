import itchat_db as db
import itchat_transfer
import itchat, time
import itchat_hrd as main
import itchat_transfer_class as trans_class

class Logg:
    from_user = {}
    to_user = {}
    state = 'null'
    transfer  = None
    time_stamp = None
    def __init__(self, user):
        self.from_user = user
        self.time_stamp = db.get_time()

        # self.transfer = itchat_transfer.load()

    def next(self, string='find'):
        """下一步"""
        self.update_timer(True)

        if self.state == 'null':
            self.change_state('choose')
            return db.lau['choose']['main'],'choose'

        elif self.state == 'choose':
            trans_list = {
                "1":["612时间表",trans_class.Bus_time_612],
                "2":["考试时间查询",trans_class.Exam_time],
                "3":["服权反馈",trans_class.FQFK]
            }
            for key in trans_list.keys():
                if string == key or trans_list[key][0].find(string) != -1:
                    self.transfer = trans_list[key][1](self)
                    return self.transfer.next(string)
            if self.transfer is None:
                return db.lau['choose']['fail'], 'choose'
        else:
            return self.transfer.next(string)

    def update_timer(self, update=True):
        time0 = db.get_time()
        time_limit = 600
        time1 = self.time_stamp
        result = (time0.tm_hour - time1.tm_hour) * 3600 + \
                 (time0.tm_min - time1.tm_hour) * 60 + (time0.tm_sec - time1.tm_sec)
        if result < time_limit:
            if update:
                self.time_stamp = time0
            return True
        else:
            return False



        #
        # find_lau = DB['languages']['find']
        # itchat_transfer.find_lau = find_lau
        # if self.state == 'null' and string == 'find' :
        #     self.change_state('find_start')
        # return self.transfer[self.state](self, string)

    def change_state(self, new_state, str=''):
        """改变状态"""
        print(self.state + ' -> ' + new_state + ' ' + str)
        self.state = new_state
        if self.state == 'null':
            self.transfer = None

    def send_msg(self, string):
        """独立发送信息"""
        global DB
        if string == 'find':
            send_str01 = DB['languages']['find']['find_send']
            send_str02 = DB['languages']['find']['find_send2']
            send_str1 =  send_str01[0] % (self.to_user['name'], \
                                          self.to_user['name_id'], self.to_user['department_info']['dep_contact'])
            send_str2 =  send_str02[0] % (self.to_user['name'], self.to_user['name_id'], \
                                          self.to_user['department_info']['main_name'], self.to_user['contact'])

            itchat.send(send_str1, self.to_user['department_info']['id'])
            itchat.send(send_str2, DB['users']['center_group']['id'])


    def is_yes(self, string):
        """ 判断是/否 """
        yess = ['是', '确认','yes','Yes']
        # nos = ['否','不确认', 'no', 'No']
        return string in yess


    def is_equ(self, msg_log):
        """ 判断是否为相同log """
        if msg_log['user_id'] == self.from_user['user_id'] and \
            msg_log['group_id'] == self.from_user['group_id']:
            return True
        else:
            return False

    def logging(self, string):

        file = open('log.txt', 'a')

    def __del__(self):
        pass