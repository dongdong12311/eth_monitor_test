# -*- coding: utf-8 -*-
"""
Created on Mon May 21 14:20:29 2018

@author: Administrator
"""
import datetime
import os 
class Log:
    def __init__(self,filename):
        self.filename = filename
    def write(self,s):
        self.__file = open(self.filename,'a+')
        timestr = str(datetime.datetime.now())
        self.__file.write(timestr+"\t"+ s + '\n')
        self.__file.close()
     
        
        

    

    
        
		
