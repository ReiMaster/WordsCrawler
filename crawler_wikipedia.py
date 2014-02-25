#encoding=utf-8
#------------------------------------------------------------------
#  File Name: crawler_wikipedia_v0.py
#  Author: yy
#  Mail: RNHisnothuman@gmail.com
#  Date: 2014年02月12日 星期三 15时15分24秒
#-------------------------------------------------------------------

import time
import sys
import string
import urllib2
import re
import types
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET


class crawler_wikipedia:

    # the start url:
    startUrl = u''

    # the prefix of wikipedia api string
    apiPrefix = u'http://zh.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&pageids='

    # the surfix of wikipedia api string
    apiSurfix = u'&format=xml'

    # the name of mean file
    MeanFileName = r'wiki.txt'

    # the name of error pageids list file
    ErrorListFileName = r'wiki_error.txt'

	#------------------------------------------------------------
    # function:  get_content_helper(self,apistr)
    # description: deduce the page type by content string
    #
    # parameter:
    # self:
    # apistr: string.
    #
    # return:
    # string
    #------------------------------------------------------------
    def get_content_helper(self,apistr):
		return u'tset the function.'



    #------------------------------------------------------------
    # function:  get_content_by_api(self,apistr)
    # description: get content by wikipedia api
    #
    # parameter:
    # self:
    # apistr: string.
    #
    # return:
    # string
    #------------------------------------------------------------
    def get_content_by_api(self,apistr):
        pagecontent = urllib2.urlopen(apistr).read()
        bs = BeautifulSoup(str(pagecontent))
		
        content = bs.find('page')
        if None == content:
            print apistr + u'    is empty!!'
            return None		
        else:
			flag_title = False
			for attribute in content.attrs:
				if attribute == u'title':
					flag_title = True
			
			if flag_title:
				print apistr + u'     has content!!'
				contentStr = self.get_content_helper(apistr)
				return contentStr
			else:
				return None	
    
	#------------------------------------------------------------
	#
	#------------------------------------------------------------
    def main(self):
		
		#change the default code type of sys
		reload(sys)
		sys.setdefaultencoding('utf-8')

		#init the pageid
		count = 121213#a exsit word

		#get the handle of output file
		outputfile = open(self.__class__.MeanFileName,'a+')

		#write the working time into file
		beginStr = 'begin time:\n' + time.asctime() + u'\n'
		outputfile.write(beginStr)

		#while(count < 2):
		#	#generate url
		#	countstr = str(count)
		#	currentApiStr = self.__class__.apiPrefix + countstr + self.__class__.apiSurfix

		#	#test if have an exception
		#	req = urllib2.Request(currentApiStr)
		#	try:
		#		urllib2.urlopen(req)
		#	except urllib2.URLError,e:
		#		count += 1
		#		print e.reason
		#		continue

		#	#get content by apistr
		#	content = self.get_content_by_api(currentApiStr)

		#	print currentApiStr
		#	print u' '
		#	print content
		#	print u'-----------------------------------------------------'
		#	count += 1
		#	print count
	
		countstr = str(count)
		currentApiStr = self.__class__.apiPrefix + countstr + self.__class__.apiSurfix
		content = self.get_content_by_api(currentApiStr)
		
		print content

		endStr = 'end time:\n' + time.asctime() + u'\n'
		outputfile.write(endStr)
		
		print currentApiStr
		print u'the main function is finished!!'

		outputfile.close()


#----------------------------------------------------------------
#
#                        program entrance
#
#----------------------------------------------------------------

print """
-----------------------------------------------------------------
                     a crawler on wikipedia
-----------------------------------------------------------------

	content is in file:
	wiki.txt

	the program is working......
"""

mycrawler = crawler_wikipedia()
mycrawler.main()
