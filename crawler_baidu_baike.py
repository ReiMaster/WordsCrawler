#coding=utf-8
#----------------------------------------------------------------------------------------
# Name: Crawler_Baidu_Baike_v1(a temporary name)
# Author: YinYan
# Version: v1
# Date: 2014-01-21
# Language: Python 2.7
# Object: a crawler on http://baike.baidu.com/ for getting words information
#----------------------------------------------------------------------------------------

import time
import sys
import string
import urllib2
import re
import types
from bs4 import BeautifulSoup

class crawler_baidu_baike:

    # the start url:
    startUrl = u''

    # the prefix of baike url string
    urlPrefix = u'http://baike.baidu.com/view/'

    # the prefix of subview 
    urlSubPrefix = u'http://baike.baidu.com'

    # the suffix of baike url string
    urlSuffix = u'.htm'

    # the name of basic mean file
    basicMeanFileName = r'basic.txt'

    # the name of polysemy list file
    polysemyListFileName = r'list.txt'

    #------------------------------------------------------------
    # function:  test_page_type(self,contentStr)
    # description: deduce the page type by content string
    #
    # parameter:
    # self:
    # contentstring: string.
    #
    # return:
    # int
    #    0 --> basic mean
    #    1 --> polysemy list
    #    2 --> others
    #------------------------------------------------------------
    def test_page_type(self,contentStr):

        bs = BeautifulSoup(contentStr)
        
        # some html sign of baike of baidu    
        mean_content = bs.find_all('div',{'class':'card-summary-content'})
        list_content = bs.find_all('div',{'id':'lemma-list'})
        lyric_content = bs.find_all('div',{'id':'lemmaContent-0'})
        none_content = bs.find_all('div',{'class':'grid container'})
            
        if '[]' != str(lyric_content) :
            
            if '[]' != str(mean_content) : # a mean page
                print u'it is a mean page'
                return 0

            else:# a lyric page
                print u'it is a lyric page'
                return 2
        
        else:# page has been deleted
            if '[]' != str(none_content):
                print u'this page has been deleted'
                return 3
            
            else:# a list page
                print u'it is a list page'
                return 1

   
    #------------------------------------------------------------
    # function:  write_local_file(self,categoryInt,countNum,contentStr,basicfile,polyfile)
    # description: write into basic mean file and others with para of type
    #
    # parameter:
    # self:
    # categoryInt: int. 
    #              0 --> basic mean
    #              1 --> polysemy list
    #              2 --> others
    # countNum: int
    # contentStr: string
    # basicfile: file type
    # polyfile: file type
    #------------------------------------------------------------
    def write_local_file(self,categoryInt,contentStr,countNum,basicfile,polyfile):
        
        # encounter a deleted page
        if 3 == categoryInt:
            print u'it a deleted page'
            print str(countNum) + ' is OK\n'
            return None

        # use BeautifulSoup to analyze page
        bs = BeautifulSoup(contentStr)
        
        # get the symbol of the word, and put into 'title'
        titleText = bs.find('title')
        pattern = re.compile('(.*?)_(.*?)')
        match = pattern.match(titleText.text)
        title = match.group(1)
 
      
        # the basic mean 
        if 0 == categoryInt:
           
            # get the first para of description of the word. 
            # generally there are several paras beyond description, 
            # but i only crawl the first one which i regard it as the most important one 
            content = bs.find('div',{'class':'card-summary-content'})
            contents = BeautifulSoup(str(content))
            para = contents.find('div',{'class':'para'})
 	    
            #print para.text
            #para = para.next_sibling
            
            if None != title and None != para.text:
                one_content = str(countNum) + u':' + title + u':\n' + para.text + u'\n'
                basicfile.write(one_content)
                print str(countNum) + ' is OK\n'
        
        # polysemy list
        elif 1 == categoryInt:
            
            list_content = bs.find_all('ul',{'class':'custom_dot para-list list-paddingleft-1'})
            items = BeautifulSoup(str(list_content))             
            item = items.find('li',{'class':'list-dot list-dot-paddingleft'})
            
            if None != title:
               
                one_content =   str(countNum) + u':' + title + u':\n'
                polyfile.write(one_content)
                basicfile.write(one_content)
 
                while None != item:
                    sub_content = item.p.a.text + u':' + self.__class__.urlSubPrefix + item.p.a['href'] + u'\n'
                    polyfile.write(sub_content)
                    print str(countNum) + ' is OK\n'
                    item = item.next_sibling

        # others 
        else:

            # now i only know the rylic page, but i think there maybe be more types of pages
            # and i do not need these pages
            # so i postpone to write code for this process
            if None != title:
                one_content = str(countNum) + ':\n' + title + 'other type!\n'
                basicfile.write(ont_content)
                print str(countNum) + ' is OK\n'
            


    #------------------------------------------------------------
    # function:  open_url_and_getContent(self,url)
    # description: use urllib2 to open url and get page content 
    #
    # parameter:
    # self:
    # url: string
    #
    # retrun:
    # string
    #------------------------------------------------------------
    def open_url_and_getContent(self,url):
         
        pageContent = urllib2.urlopen(url).read()
        return str(pageContent)


    #------------------------------------------------------------
    # function:  main(self)
    # description: the main function
    # parameter:
    # self:
    #------------------------------------------------------------
    def main(self):
       
        # change the default code type of sys
        # very important.
        reload(sys)
        sys.setdefaultencoding('utf-8') 
        
        # init the count(page number) --> maybe i would make it a new function, but not now.
        count = 1

        # get the handle(legacy habit from windows) of two files
        basicFile = open(self.__class__.basicMeanFileName,'a+')
        polyFile = open(self.__class__.polysemyListFileName,'a+') 

        # write the working time into file
        beginStr = 'begin time:\n' + time.asctime() + u'\n'
        basicFile.write(beginStr)
        polyFile.write(beginStr)

        while count <= 5:            
            # generate the url
            countStr = str(count)
            currentUrl =  self.__class__.urlPrefix + countStr + self.__class__.urlSuffix
            
            # test if have an exception
            req = urllib2.Request(currentUrl)  
            try:
                urllib2.urlopen(req)
            except urllib2.URLError, e:
                count += 1    
                print e.reason
                continue
      
            # get content of the url
            theContentStr = self.open_url_and_getContent(currentUrl)

            # deduce the type of page
            pageType = self.test_page_type(theContentStr)

            # write appropriate things in files
            resultState = self.write_local_file(pageType,theContentStr,count,basicFile,polyFile)
            #if 0 == resultState:
                #print u'-----the write process is ok!-----'
                #print u' '

            print currentUrl
            print u'----------------------------------'
            count += 1
        

        # write the end time into file
        endStr = 'end time:\n' + time.asctime() + u'\n'
        basicFile.write(endStr)
        polyFile.write(endStr)

        print u'the main function is finish!'
        basicFile.close()
        polyFile.close()







#-------------------------------------------------------------------------
#
#                            Program Entrance
#
#-------------------------------------------------------------------------

print """
--------------------------------------------------------------------------
                       a crawler on baike of baidu(v1)
--------------------------------------------------------------------------

    content is in files:
    basic.txt
    list.txt

    the program is working......


"""

mycrawler = crawler_baidu_baike()
mycrawler.main()

