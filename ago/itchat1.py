import itchat
from itchat.content import TEXT
import time
main_list = [{'type':'1', 'id':'@@2b970b68c2b1cf28fadc58bfc714a311d3f8341a0aa9827fa47f943ceab8a2cc', 'name':''},
             {'type':'2', 'id':'@@45fde7a3081aabd24f14b14b601dc75c4c323ed1319bfc6c29bb472b9d5b5ae4', 'name':''},
             {'type':'3', 'id':'@c911a77b1cbd630c747ee5f3c5e74eb75d76def0dd1519daf01c5aa7f26b2ead', 'name':''}
            ]

now_history = [{'id':'', 'res':'', 'rep':''}]

test1 = '@@89f7dc53950d08f3e28edbccfbbbf201dd2f36eead7b0ff7bd3987e131032b1c'
test2 = '@@ca03d731f7e0be6dfc104f280cebd7a80acda3969c9f109bd498c824b66fdd2c'
@itchat.msg_register(TEXT, isGroupChat = True)
def text_reply(msg):
    t = msg['Content']
    itchat.send_msg(msg="我不是复读机 " + t,toUserName=test2)
    print(msg)

    # print(t)
    # return "jjk"
    if t.find('失物招领')!=-1:
        rep = parse(t)
        res = encode(rep)
        his = {'id':msg['ActualUsername'], 'res':res, 'rep':rep}
        now_history.append(his)
        return res

    elif t == '是' or t == 'yes' or t == 'Y':
        for i in now_history:
            if i['id']==msg['ActualUsername']:
                send_msg(i['rep'], i['res'])
                now_history.remove(i)
                return "已转发!"
    elif t == '否' or t == 'no' or t == 'N':
        for i in now_history:
            if i['id']==msg['ActualUsername']:
                now_history.remove(i)
                return "已取消转发!"

# @itchat.msg_register(TEXT, isGroupChat = False)
# def text_reply(msg):
#     # itchat.send_msg(msg=msg['Content'],toUserName= '@@45fde7a3081aabd24f14b14b601dc75c4c323ed1319bfc6c29bb472b9d5b5ae4')
#     print(msg)
#     return ''

def encode(rep):
    return '[失物招领]\n学子卡号 '+rep['number']+ '\n学院：'+ rep['to2'] +'\n联系方式：'+ rep['contact']+ '\n时间：'+ rep['time']

def parse(msgg):
    if msgg=='':
        return ''
    list1=msgg.split()
    rep = {}
    for i in list1:
        if i.find('学院')!=-1:
            rep['to'] = dect_to(i)
            rep['to2'] = i
            continue
        elif len(i)==11 or i.find('微信号')!=-1:
            rep['contact'] = i
            continue
        elif len(i)==7:
            rep['number'] = i
    tim = time.localtime(time.time())
    # rep['time'] = 'at '+ tim[1]+'.'+ tim[2]+ ' '+ tim[3]+ ':' +tim[4]
    rep['time']=''
    return rep

def dect_to(msgg):
    tos = [{'name':'数学科学学院', 's_name':['数学'],'id':'1'},
           {'name':'化学科学学院', 's_name':['化学'],'id':'2'}
          ]
    for i in tos:
        for p in i['s_name']:
            if msgg.find(p)!=-1:
                return i['id']

def send_msg(rep, res):
    for i in main_list:
        if i['type']==rep['to']:
            itchat.send_msg(msg=res, toUserName=i['id'])
            print(res)

itchat.auto_login(True)
# itchat.send_msg(msg='hello',toUserName= '@@45fde7a3081aabd24f14b14b601dc75c4c323ed1319bfc6c29bb472b9d5b5ae4')

itchat.run()




# test2  @@2b970b68c2b1cf28fadc58bfc714a311d3f8341a0aa9827fa47f943ceab8a2cc
# group  @@45fde7a3081aabd24f14b14b601dc75c4c323ed1319bfc6c29bb472b9d5b5ae4
# test   @c911a77b1cbd630c747ee5f3c5e74eb75d76def0dd1519daf01c5aa7f26b2ead
# me     @a7badf8bf629442b0f0ab0373ec14d25ec6337e0686178df7d04d607b04f4a61

