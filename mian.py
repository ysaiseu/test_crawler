# -*- coding: utf-8 -*-

import weiboLogin
import urllib
import urllib2
import time
import Queue
from parserSaverThread import*
import getWeiboPage

def main(username = '', userurl = '/u/1765475181'):
    globalValue.mainusername = username
    globalValue.mainuserurl = userurl

    if globalValue.isLogIn:
        wbpage = getWeiboPage.getWeiboPage()
        #uid ='/u/1765475181' #master传过来的<key value>中的value

        t = parserSaverThread()#parserSaverThread是处理爬下来的网页，把所有@的用户提取出来。并保存在userque2salve中传给slave们
        t.setDaemon(False)#主线程结束，子线程不跟着结束
        t.start()
        wbpage.get_userpage(userurl)#爬网页咯
    else:
        filename = './conf/account'#保存微博账号的用户名和密码，第一行为用户名，第二行为密码
        WBLogin = weiboLogin.weiboLogin()
        if WBLogin.login(filename) == 1:
            globalValue.isLogIn = True
            print 'Login success!'
            wbpage = getWeiboPage.getWeiboPage()
            #uid ='/u/1765475181' #master传过来的<key value>中的value

            t = parserSaverThread()#parserSaverThread是处理爬下来的网页，把所有@的用户提取出来。并保存在userque2salve中传给slave们
            t.setDaemon(False)#主线程结束，子线程不跟着结束
            t.start()
            wbpage.get_userpage(userurl)#爬网页咯
        else:
            print 'Login error!'
            exit()

if __name__ == '__main__':
    main()