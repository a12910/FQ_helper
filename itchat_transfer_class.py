import time
import itchat_db as db

class Finder:

    root = None
    transfers = {}
    laus  = {}
    def __init__(self, root):
        self.root = root
        self.laus = db.lau['Find']
    def next(self, data=''):
        if self.root.state == 'choose':
            self.root.change_state('null')
            return self.laus['main'],'null'

    def dect(self, data):

        pass

    def load_transfer(self):
        pass


class FQFK:
    """服权反馈"""
    root = None
    transfers = {}
    laus = {}

    def __init__(self, root):
        self.root = root
        self.root.mode = 'FQFK'
        self.laus = db.lau['FQFK']

    def next(self, data=''):
        if self.root.state == 'choose':
            self.root.change_state('null')
            return self.laus['main'],'null'

    def dect(self, data):
        pass

    def load_transfer(self):
        pass


class Exam_time:
    """考试时间"""
    root = None
    transfers = {}
    laus = {}
    time_db = []
    def __init__(self, root):
        self.root = root
        self.root.mode = 'FQFK'
        self.laus = db.lau['Exam_time']

    def next(self, data=''):
        if self.root.state == 'choose':
            self.root.change_state('search')
            return self.laus['main'], 'search'
        elif self.root.state == 'search':
            if len(data.replace(" ", ""))<2:
                return self.laus['more'], 'search'
            result = []
            for item in self.time_db:
                if item['name'].find(data) != -1:
                    result.append(' '.join([item['name'], item['time']]))
            if len(result) == 0:
                return self.laus['fail'], 'search'
            else:
                self.root.change_state('null')
                return result, 'null'

    def dect(self, data):
        pass

    def load_transfer(self):
        pass

class Bus_time_612:
    root = None
    transfers = {}
    laus = {}
    time_db_way1 = []
    time_db_way2 = []

    def __init__(self, root):
        self.root = root
        self.root.mode = 'FQFK'
        self.laus = db.lau['Bus_time_612']
        self.time_db_way1 = db.load_csv('Bus_time_612_way1')
        self.time_db_way2 = db.load_csv('Bus_time_612_way2')

    def next(self, data=''):
        if self.root.state == 'choose':
            self.root.change_state('null')
            now_time = time.localtime()
            now_v = now_time.tm_hour * 60 + now_time.tm_min

            def select_time(db1):
                result0 = []
                for item in db1:
                    item_v = item['hour'] * 60 + item['min']
                    if now_v < item_v:
                        if len(result1)<3:
                            result0.append("%s:%s %s %s" % (item['hour'], item['min'], item['mode'], item['place']))
                        else:
                            break

                if len(result0) == 0:
                    result0 = self.laus['no_way']
                else:
                    result0 = '\n'.join(result0)

                return result0
            result1 = select_time(self.time_db_way1)
            result2 = select_time(self.time_db_way2)

            return self.laus['main'] +  \
                   [self.laus['way1'][0] % result1, self.laus['way2'][0] % result2], \
                   'null'


    def dect(self, data):
        pass

    def load_transfer(self):
        pass