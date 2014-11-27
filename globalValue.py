# -*- coding: utf-8 -*-
'''
Created on 2014年4月2日

@author: JuliaJu
'''
import Queue
crawlerFinish=False #判定网页是否爬完的标志
isLogIn = False #标识是否登录成功
mainuserid="" #现在在爬谁的网页，到时候要把这个传回给master
mainusername = ''  #现在爬取得user的网页，user的名字
mainuserurl = ''   #现在爬取得user的网页，user的网址
userque2slave = Queue.Queue(-1)#给slave的 user队列 每个user是由<昵称，网址>组成
contentque2myparser = Queue.Queue(-1)#爬虫给解析其的内容队列，内容为原始网页
slavebackQueue = Queue.Queue(-1)#slave传回给master的队列
adjRelation={} #最后的一个关系，,每个元素为：<userA,{"abc":3,"cdd":5}>
