# coding: utf-8
import datetime,os,codecs

def now():
    return datetime.datetime.now()

def choice():
    while True:
        ans=input()
        if ans=='y':
            return True
        if ans=='n':
            return False

def select(options,prompt=''):
    while True:
        ans=input(prompt)
        if ans in options:
            return ans
    
def printHl():
    print('--------------------------------')

def serialOptions(n):
    a=[]
    for b in range(n):
        a.append(str(b))
    return a

def waitForReturn():
    print(u'続けるにはEnterキーを押してください。')
    _=input()