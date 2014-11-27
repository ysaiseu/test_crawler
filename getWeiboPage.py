# -*- coding: utf-8 -*-

import urllib
import urllib2
import sys
import time
import re
import json
import globalValue
#from boto.manage.propget import get
reload(sys)
sys.setdefaultencoding('utf-8') 

class getWeiboPage:
    pre_url_roll ='http://weibo.com/p/aj/mblog/mbloglist?'
    pre_main_url ='http://weibo.com'
    FINISH_PAGE =1
    body_roll0 = {
        'is_search':'0',
        'visible':'0',
        'is_tag':'0',
        'profile_ftype':'1',
        'page':''
    }
    body_roll1 = {
        'domain':'',
        'pre_page':'',#第几页，则为几
        'page':'',#同page
        'max_id':'',#已访问到的最下面的微薄id
        'end_id':'',#该页最一开始的微薄id
        'count':'15',
        'pagebar':'0',
        'max_msign':'',
        'filtered_min_id':'',
        'pl_name':'Pl_Official_LeftProfileFeed__20',
        'id':'',
        'script_uri':'',#/p/1002061643971635/weibo
        'feed_type':'0',
        '__rnd':''#访问这一页面的时间
    }
    body_roll2 = {
        'domain':'',
        'pre_page':'',#第几页，则为几
        'page':'',#同page
        'max_id':'',#已访问到的最下面的微薄id
        'end_id':'',#该页最一开始的微薄id
        'count':'15',#unchangeable
        'pagebar':'1',#unchangeable
        'max_msign':'',#/ unchangeable
        'filtered_min_id':'',#/ unchangeable
        'pl_name':'Pl_Official_LeftProfileFeed__20',
        'id':'',
        'script_uri':'',#/p/1002061643971635/weibo
        'feed_type':'0',
        '__rnd':''#访问这一页面的时间
    }
    page=1
    id=""
    charset = 'utf8'
    def get_userpage(self,url):
        try:
            url = url.replace('\/','/')
            url = self.pre_main_url+url
            req = urllib2.Request(url)
            result = urllib2.urlopen(req)
            text = result.read()
            #self.writefile('./output/firstpage',text)
            try:
                content = eval("u'''"+text+"'''").encode('latin-1').decode('utf-8')
            except Exception as err:
                print '[worker] <get_useroage> some except:',err
                return 1
            #self.writefile('./output/firstpageR'+str(self.page),content)
            id_item = re.findall(r'PRF_feed_list_more SW_fun_bg S_line2".*?href="\\/p\\/(.*?)\\/',content)
            if id_item:
                self.get_msg(id_item[0])
            return
        except BaseException as e:
            print '[worker] <get_userpage> some except: ',e
        finally:
            return 1

    def get_msg(self,id):
        self.id = id
        globalValue.mainuserid=id
        self.body_roll1['domain'] = id[0:6]
        self.body_roll2['domain'] = self.body_roll1['domain']
        self.body_roll1['id'] = id
        self.body_roll2['id'] = id
        self.body_roll1['script_uri']='/p/'+id+'weibo'
        self.body_roll2['script_uri']='/p/'+id+'weibo'
        url = self.get_url(id)
        while True:
            if self.page<=self.FINISH_PAGE:
                if not self.get_firstpage(url):
                    globalValue.crawlerFinish=True
                    return 0
                print str(self.page)+'\r\n'
                self.get_secondpage()
                self.get_thirdpage()
            else:
                globalValue.crawlerFinish=True
                return 0
    def get_firstpage(self,url):
        #url:http://weibo.com/p/1002062844714572/weibo
        self.body_roll0['page']=self.page
        url = url +urllib.urlencode(self.body_roll0)
        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
        text = result.read()
        #self.writefile('./output/roll0null',text)  
        content = eval("u'''"+text+"'''").encode('latin-1').decode('utf-8')
        globalValue.contentque2myparser.put(content)
        if not self.getMaxEnd(content):
            self.page=1;
            print 'last page finish'
            return False
       #  self.writefile('./output/'+str(self.page)+'result_roll0',content) #need to encode and then decode
        return True
        #return eval("u'''"+text+"'''").encode('latin-1').decode('utf-8')
    def get_secondpage(self):
        self.body_roll1['page'] = self.page
        self.body_roll1['pre_page'] = self.body_roll1['page']
        self.body_roll1['__rnd'] = time.time()
        url = self.pre_url_roll +urllib.urlencode(self.body_roll1)
        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
        text = result.read()
       # self.writefile('./output/roll1',text)  
        jsonstr = json.loads(text)
        text = jsonstr['data']   
        content = eval("u'''"+text+"'''")
        globalValue.contentque2myparser.put(content)
       #  self.writefile('./output/'+str(self.page)+'result_roll1',content)
        self.getMaxID(content)
    def get_thirdpage(self):
        self.body_roll2['page'] = self.page
        self.body_roll2['pre_page'] = self.body_roll1['page']
        self.body_roll2['__rnd'] = time.time()
        self.page+=1
        url = self.pre_url_roll +urllib.urlencode(self.body_roll2)
        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
        text = result.read()
        #self.writefile('./output/roll2',text)   
        jsonstr = json.loads(text)
        text = jsonstr['data']   
        content = eval("u'''"+text+"'''") 
        globalValue.contentque2myparser.put(content)
       #  self.writefile('./output/'+str(self.page)+'result_roll2',content)
    def get_url(self,uid):
        url = 'http://weibo.com/p/' + uid + '/weibo?' 
        return url
    def get_uid(self,filename):
        fread = file(filename)
        for line in fread:
            self.uid_list.append(line)
            print line
            time.sleep(1)
    def getMaxEnd(self,content):#将下一个roll的参数设置好
        mid_items = re.findall(' mid="(\d+)"', content)
        if mid_items:
            self.body_roll1['end_id'] = mid_items[0]
            self.body_roll1['max_id'] = mid_items[-1]
            self.body_roll2['end_id'] = mid_items[0]
            return True
        else:
            return False
    def getMaxID(self,content):
        mid_items = re.findall(' mid="(\d+)"', content)
        if mid_items:
            self.body_roll2['max_id'] = mid_items[-1]
    def writefile(self,filename,content):
        fw = file(filename,'w')
        fw.write(content)
        fw.close()
        
        
