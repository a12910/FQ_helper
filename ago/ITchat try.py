import itchat, time, re
from itchat.content import *
# from utilities import *
from sys import argv, exit
import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# room_list=itchat.get_chatrooms()
# givehelp_chatroom='a'
department_list = [{'grade':'15(\d){4}', 'id':'@@db79de1270df3ab5bea4f3420d051b34985744ec0e7fa83ef6ad00128fde2599', 'name':'宝宝今天不找小美'},#一手好牌
             {'grade':'16(\d){4}', 'id':'@85d012430517a0eb4497d3d1f972bc299b95b2a22519d0eea32e2a506205a46e', 'name':'李珅'},#李珅
             {'grade':'17(\d){4}', 'id':'@055bd39400ca01fdc0ef7d5df44d01a5b18bf5ec2dc0605e2ef6fd0ac6d7b0de', 'name':'李昕辰'},#李昕辰
                   {'grade':'18(\d){4}', 'id':'@1b47062b0ffd90e274d467b49082ca0c748cdcbff82e801f571d4f90077db4a8', 'name':'刘源洋'}] #刘源洋
information={}

tests = [
    {'id':'@@89f7dc53950d08f3e28edbccfbbbf201dd2f36eead7b0ff7bd3987e131032b1c','name':'机器人测试小白鼠', 'type':'group'},
    {'id':'@@ca03d731f7e0be6dfc104f280cebd7a80acda3969c9f109bd498c824b66fdd2c', 'name':'宝宝今天不找小美','type':'group'},
    {'id':'', 'type':'group'}
]


# print (department_list)
#chatroomNames = [ getNameForChatroomDisplayName(x) for x in chatroomDisplayNames ]
#chatroomObjs = [ getChatroomByName(chatrooms, x) for x in chatroomNames ]
#if len([ x for x in chatroomObjs if x is None ]) != 0:
    #exit(-1)
#chatroomIds = [ x['UserName'] for x in chatroomObjs ]
#nickNameLookup = NickNameLookup(chatroomObjs)
#logging.info('Fetched user ids for the chatrooms.')
itchat.auto_login(True)  #生成二维码  enableCmdQR=0.25 如果机器人有需要持久在线的需求，我们可以把脚本挂到服务器上，
    # 24小时跑，但是一般的云服务器是没有界面的，都是通过终端命令行进行操作，这个时候可以添加enableCmdQR=True enableCmdQR=-2参数，
    # 让二维码显示到命令行上，另外部分系统可能字符宽度有出入，如图19.2所示，可以通过把enableCmdQR赋值为特定的倍数进行调整。
# time.sleep(5)       #暂停秒数
print (itchat.get_chatrooms())

for i in tests:
    x = itchat.search_chatrooms(userName=i['name'])
    print(x)


itchat.run()
itchat.send(msg = "我在进行微信测试", toUserName="@@89f7dc53950d08f3e28edbccfbbbf201dd2f36eead7b0ff7bd3987e131032b1c")
         #if __name__ == '__main__':那就把不需要的代码段也当成函数运行，
# 但是这个函数有点特殊，他要区分是自身运行还是被调用导入而运行，
# 如果是自身运行那么就把那些代码段显示出来，如果被调用就屏蔽掉


@itchat.msg_register(TEXT,isGroupChat=True)
def reply_msg_rooms(msg):
    print(msg)
    mice= itchat.search_chatrooms(toUserName="@@db79de1270df3ab5bea4f3420d051b34985744ec0e7fa83ef6ad00128fde2599")
    if len(mice)>0:
         print("收到一条群信息：", msg['ActualNickName'], msg['Content'])   #测试代码

# @itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
def received_help(msg):
    if msg['isAt']:  # msg['isAt']msg['Content'] == u'@宝宝'
        itchat.send(msg['ActualNickName'] + ",你有什么需要帮助的吗?", msg['FromUserName']) # room_list[0]['UserName']
        itchat.send(u"有缘一线牵,寻找学子卡主人服务请回复‘要呀，宝宝’,找我玩玩请回复‘不要，宝宝’")
    elif msg['Content'] == (u'是呀，宝宝'):
        givehelp_chatroom = msg['id']
        itchat.send('网络一线牵，珍惜这段缘，我会叫傻FUFU主人联系你的微信')
        itchat.send('但是宝宝傻傻，请按照以下格式输入失主的信息和你的联系电话哦：姓名 学号 学院全称 11位电话号码')
        matching = re.match('@^[\u4E00-\u9FA5]{2,10}\s(\d*6)\s@^[\u4E00-\u9FA5]{2,30}\s((\d*11))', msg["Content"])
        getting = matching.group()
        information = transfer_words(getting)
        for item in department_list:  # 用字典把学院全称（key）转换成群ID（value），发送
            if item['name'] == information[2] and item['grade'] == information[0]:
                itchat.send('%s同学（学号为：%s）,你的学子卡被抓到了，快去联系小可爱,带学子卡回家' % (information[1], information[0]),toUserName=item['id'])
                itchat.send('捡到卡的小可爱是来自%s,ta的电话是%s' % (givehelp_chatroom , information[3]))
                itchat.send('宝宝好事做完，可以去找小美玩了噜', toUserName=item['id'])
                givehelp_chatroom = 'a'
            else:
                itchat.send('输入格式有误或者南开没有开设此院，你再试一下吧', toUserName=givehelp_chatroom)
    elif msg['Content'] == (u'不要，宝宝'):
        itchat.send("哼，那宝宝去找小美玩了噜")
        itchat.user.send_image(fileDir="20160923204424_NBG84.thumb.224_0[1].gif",toUserName=msg["FromUserName"])#ImageName.decode('utf-8')

def transfer_words(x):
    x1=re.search('\d{6}',x)
    x2=re.search('@^[\u4E00-\u9FA5]{2,10}',x)
    x3=re.search('@^[\u4E00-\u9FA5]{2,30}',x)
    x4 = re.search('\d{11}', x)####################################正则表达式很有问题
    result={}
    result[0]=x1
    result[1]=x2
    result[2]=x3
    result[3]=x4
    return result


