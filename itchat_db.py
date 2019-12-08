import json, csv, time



DB = {}
lau = {}
listen_groups = []
logs = []


def load_DB():
    global DB, lau
    f = open('db.JSON', encoding='utf-8')
    DB = json.loads(f.read())
    lau = DB['languages']

def load_csv(string):
    with open('./data/%s.csv' % string)as f:
        f_csv = csv.reader(f)
        result = []
        for row in f_csv:
            result.append(row)
        return result

def get_time():
    return time.localtime()
