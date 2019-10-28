import itchat, time, re
from itchat.content import *
from sys import argv, exit
import logging

import threading

itchat.auto_login(True)
    # 生成二维码  enableCmdQR=0.25 如果机器人有需要持久在线的需求，我们可以把脚本挂到服务器上，
    # 24小时跑，但是一般的云服务器是没有界面的，都是通过终端命令行进行操作，这个时候可以添加enableCmdQR=True enableCmdQR=-2参数，
    # 让二维码显示到命令行上，另外部分系统可能字符宽度有出入，如图19.2所示，可以通过把enableCmdQR赋值为特定的倍数进行调整。

chatroom1 = itchat.search_chatrooms(name='小小机器人发信')
chatroom2 = itchat.search_chatrooms(name='小小机器人收信')
#chatroom1 = itchat.search_chatrooms(name='Test01')
#chatroom2 = itchat.search_chatrooms(name='Test02')
chatroom_list = {'收信':chatroom2[0],'发信':chatroom1[0]}

# if __name__ == '__main__':那就把不需要的代码段也当成函数运行，
# 但是这个函数有点特殊，他要区分是自身运行还是被调用导入而运行，
# 如果是自身运行那么就把那些代码段显示出来，如果被调用就屏蔽掉
clist = [chatroom1[0]['UserName'],chatroom2[0]['UserName']]
isFound = [False,False]
#isFound = False #通过该参数分为两种模式，该值为true时机器人会试图提醒捡到卡的同学格式不对
#FGroup = None
refound = [False,False]
print(clist)

@itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
def received_help(msg):
	global isFound
	global refound
	if msg['FromUserName'] in clist:
		croom = clist.index(msg['FromUserName'])
		if True:
			if msg['isAt']:#被@的时候
				itchat.send(msg['ActualNickName'] + ",你有什么需要帮助的吗?", msg['FromUserName']) # room_list[0]['UserName']
				itchat.send("有缘一线牵，寻找学子卡主人服务请回复‘是呀，宝宝’,找我玩玩请回复‘不要，宝宝’", msg['FromUserName'])
			elif msg['Content'] == ('是呀，宝宝'):
				#givehelp_chatroom = msg['FromUserName']
				itchat.send('网络一线牵，珍惜这段缘，我会叫傻FUFU主人联系你的微信', msg['FromUserName'])
				itchat.send('但是宝宝傻傻，请按照以下格式输入失主的信息和你的联系电话：姓名 学号 学院全称 11位电话号码，每两项之间用空格隔开哦~', msg['FromUserName'])
				refound[croom]=True
				isFound[croom]=True
				#FGroup=msg['FromUserName']
				threading.Thread(target=timer,args=(croom,)).start()
			elif msg['Content'] == ('不要，宝宝'):
				itchat.send("哼，那宝宝去找小美玩了噜", msg['FromUserName'])
				itchat.send_image(fileDir="2014112510042586953[1].jpg",toUserName=msg["FromUserName"])
			elif isFound[croom]:
				if ' ' in msg['Content']:#由于通常的交流中较少出现空格，故此处若发言中出现空格再判断其格式正误
					# matching = re.match('([\u4E00-\u9FA5]{2,10})\s(\d{7})\s([\u4E00-\u9FA5]{2,30})\s(\d{11})$', msg["Content"])
					matching = msg['Content'].split(' ')
					if matching:
						r={}
						for i in range (4):
							r[i] = matching[i]
						itchat.send('哈哈哈哈！我知道失主信息啦噜：\n姓名：%s\n学号：%s\n学院：%s\n您的联系方式：%s' % (r[0],r[1],r[2],r[3]),msg['FromUserName'])
						isFound[croom]=False
						# grade=(re.match('\d{2}',r[1]).group(0))
						# room = chatroom_list[grade+r[2]]
						room = chatroom_list[r[2]]
						itchat.send('%s同学（学号为：%s）,你的学子卡被抓到了，快去联系小可爱,带学子卡回家' % (r[0], r[1]), room['UserName'])
						itchat.send('捡到你卡的小可爱的电话是%s' % r[3], room['UserName'])
						itchat.send('宝宝好事做完，可以去找小美玩了噜' , room['UserName'])
						itchat.send_image(fileDir="20181013213654_nuxff.jpg", toUserName=msg["FromUserName"])
					else:
						itchat.send('请输入正确的格式，否则宝宝看不懂哦~',msg['FromUserName'])
						itchat.send('格式：姓名 学号 学院全称 11位电话号码（每两项之间用空格隔开~）',msg['FromUserName'])
						itchat.send('回复“退出”即可退出本次服务,你又来胡闹，小坏蛋',msg['FromUserName'])
				if msg['Content'] == ('退出'):
					isFound[croom]=False
					itchat.send('那宝宝先告辞了，有事再来@我吧！',msg['FromUserName'])


def timer(TGroup):
	global isFound
	time.sleep(5)
	refound[TGroup] = False
	time.sleep(5)
	for i in range(4000):
		time.sleep(0.1)
		if refound[TGroup]:
			return
	if isFound[TGroup]:
		isFound[TGroup] = False
		itchat.send('哎呀，你的操作超时了，再发一次“@宝宝”可好？我就是有点傲娇',clist[TGroup])
		return

itchat.run()
