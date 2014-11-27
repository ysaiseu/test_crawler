# -*- coding: utf-8 -*-
'''
Created on 2014年4月1日

@author: JuliaJu
'''
import threading,time
import Queue
import re
import globalValue

class parserSaverThread(threading.Thread):
    '''
    classdocs
    '''
    #linkWdict={}
    def __init__(self):
        '''
        Constructorjui
        '''
        threading.Thread.__init__(self)
        self.linkWdict={}

    def writeall(self,filename):
        fw = file(filename,'w')
        for (k,v) in  self.linkWdict.items():
            fw.write(globalValue.mainusername + '::::' + \
                     str(k).encode('utf-8')+"::::"+ \
                     str(v)+"\r\n")
        fw.close()  
    def run(self):
        count=0
        while not globalValue.crawlerFinish:
            if not globalValue.contentque2myparser.empty():
                print 'run'
                count=0
                content = globalValue.contentque2myparser.get(True)
    # at_items = re.findall(r'feed_list_content.*?href="\\/n\\/(.*?)" usercard="name(=.*?)"', content,re.M)
                at_items = re.findall(r'href="[(/n/)(\\/n\\/)](.*?)" usercard="name=(.*?)">', content,re.M)
                if at_items:
                    for item in at_items:
                        if not item[1] in self.linkWdict:
                            userdict =(item[1],'/n/'+str(item[0]).split('/')[-1])
                            globalValue.userque2slave.put(userdict)
                            self.linkWdict[item[1]]=1
                        else:
                            self.linkWdict[item[1]]=int(self.linkWdict[item[1]])+1
                at_items = re.findall(r'feed_list_forwardContent.*?\n.*?\n.*?nick-name="(.*?)".*?href="(.*?)"', content,re.M)
                if at_items:
                    for item in at_items:
                        if not item[0] in self.linkWdict:
                            userdict =(item[0],item[1])
                            globalValue.userque2slave.put(userdict)
                            self.linkWdict[item[0]]=1
                        else:
                            self.linkWdict[item[0]]=int(self.linkWdict[item[0]])+1
            else:
                #print 'sleep'
                count+=1
                print 'sleep count:'+str(count)
                if count>=10:
                    break
                else:
                    time.sleep(2)
        if globalValue.crawlerFinish:
            print 'haha'
            globalValue.adjRelation[globalValue.mainusername]=self.linkWdict
            if self.linkWdict:
                print 'write'
                self.writeall('./output/resulthuhuha')