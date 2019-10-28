# from itchat_hrd import DB
import copy

DB = {}

find_lau = {}

def find_start(self, string):
    self.change_state('find_edit', string)
    return find_lau['find_edit'], True

def find_edit(self, string):
    pstate, result = to_user_parse(self, string)
    if pstate:
        self.change_state('find_confirm', string)
        return result + find_lau['find_confirm'], True
    else:
        return result + find_lau['find_edit_err'], True

def find_confirm(self, string):
    if self.is_yes(string):
        self.send_msg('find')
        return find_lau['find_success'], False
    else:
        return find_lau['find_failed'], False

def load():
    return {
        'find_start':find_start,
        'find_edit':find_edit,
        'find_confirm':find_confirm
    }

def to_user_parse(self, string):
    """解析失主信息"""
    string2 = string.split(' ') # 姓名 学号 学院 联系方式 (空格分开)
    to_user = {
        "name": string2[0],
        "name_id": string2[1],
        "department": string2[2],
        "contact": string2[3]
    }

    if len(to_user["name_id"]) != 7:
        return False, ["仅限于本科生学号 " + to_user['name_id']]
    find_dep_result = find_dep(to_user)
    if find_dep_result != 'no':
        to_user['department_info'] = find_dep_result
    else:
        return False, ["没有找到这个学院,请检查下输入格式 " + to_user['department']]
    self.to_user = to_user
    return True, ["姓名：%s，学号：%s，学院：%s" % \
                  (to_user['name'], to_user["name_id"], to_user['department_info']['main_name'])]

def find_dep(to_user):
    """解析学院"""
    grade = to_user['name_id'][:2]
    dep0 = to_user['department']

    # 如果找不到学院则转到default
    result = None
    for dep in DB['departments']:
        if dep0 == dep['name'] or dep0 in dep['s_name']:
            for dep2 in dep['groups']:
                if grade == dep2['grade'] or (grade == 'default' and result is None):
                    result = copy.deepcopy(dep2)
                    result['main_name'] = dep['name']

    if result is None:
        return 'no'
    else:
        return result