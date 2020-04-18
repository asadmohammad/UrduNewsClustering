# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 08:42:43 2019

@author: Mohammad Asad
"""


import re
import os
import glob
from tkinter import *
from urduhack import normalize
import subprocess

stop_words = frozenset("""
 آ آئی آئیں آئے آتا آتی آتے آس آنا آنی آنے آپ آیا ابھی از اس اسی اسے البتہ
 الف ان انہوں انہی انہیں اور اپ اپنا اپنی اپنے اکثر اگر اگرچہ ایسا ایسی ایسے ایک اے بار بارے
 باوجود باہر بعض بغیر بلکہ بن بنا بناؤ بند بڑی بھر بھریں بھی بہت بیس بے تا تاکہ تب تجھ
 تجھے تحت تر تم تمہارا تمہاری تمہارے تمہیں تو تک تھا تھی تھیں تھے تیری جا جاؤ جائیں جائے جاتا
 جاتی جاتے جانی جانے جب جبکہ جس جن جنہوں جنہیں جو جہاں جیسا جیسوں جیسی جیسے حالانکہ حالاں حصہ خالی
 خود درمیان دوران دوسرا دوسروں دوسری دوسرے دوں دکھائیں دی دیئے دیا دیتا دیتی دیتے دیر دینا دینی دینے
 دیکھو دیں دیے دے ذریعے رکھا رکھتا رکھتی رکھتے رکھنا رکھنی رکھنے رکھو رکھی رکھے رہ رہا رہتا رہتی رہتے
 رہنا رہنی رہنے رہو رہی رہیں رہے سا ساتھ سامنے سب سو سکا سکتا سکتے سی سے شاید صرف طرح
 طرف طور علاوہ عین لئے لا لائی لائے لاتا لاتی لاتے لانا لانی لانے لایا لو لوجی لوگ لوگوں لگ
 لگا لگتا لگتی لگی لگیں لگے لہذا لی لیا لیتا لیتی لیتے لیکن لیں لیے لے مجھ مجھے مزید مطابق
 مل مگر میرا میری میرے میں نا نہ نہیں نے وار واقعی والا والوں والی والے
 وجہ وغیرہ وہ وہاں وہی وہیں وی ویسے پایا پر پھر پیچھے چاہئے چاہتے چاہیئے چاہے چلا چلو چلیں چلے
 چونکہ چکی چکیں چکے ڈالنی ڈالنے ڈالے کئے کا کب کبھی کر کرتا کرتی کرتے کرنا کرنے کرو کریں کرے
 کس کسی کسے کم کو کوئی کون کونسا کچھ کہ کہا کہاں کہہ کہی کہیں کہے کی کیا کیسے کیونکہ
 کیوں کیے کے گئی گئے گا گویا گی گیا گے ہاں ہر ہم ہمارا ہماری ہمارے ہو ہوئی ہوئیں ہوئے
 ہوا ہوتا ہوتی ہوتیں ہوتے ہونا ہونگے ہونی ہونے ہوں ہی ہیں ہے یا یات یعنی یہ یہاں یہی یہیں
""".split())



"Word Split"
def splitWords(headlines):
    words = []
    splitHL = []
    for headline in headlines:  
        words = re.split('\W+',headline)
        
        splitHL.append(words)
        words = [""]
    
    return splitHL

"Word Tokenisation"
def tokeniseWords(wordList):
    newWord = []
    newWord = re.sub(r'[^\w]', '', wordList)
    #print(newWord)
    return newWord


"Stop Word Removal"
def removeStopwords(jumla):    
    emp = ''
    finalwordsWoSW = []
    for alfaz in jumla:
        wordsWoSW = []
        for lafz in alfaz:
            if lafz in stop_words or lafz == emp:
                continue
            wordsWoSW.append(lafz)
        
        finalwordsWoSW.append(wordsWoSW)
        del wordsWoSW 
        
        
    return finalwordsWoSW

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
END OF PRE PROCESSING

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



"Path of The Folders"
def dataFolders(path):
    folders = []
    foldferPath = path
    for root, directories, files in os.walk(foldferPath):
        for folder in directories:
            folders.append(os.path.join(root,folder))
        
    return folders


"Read Title of the File"
def headlineReader(path):
    headlines = []
    extraWords = ['.doc','Urdu NEWS dataset\\','voa','bbc','dataset','entertainment','sports','miscleneous','politics','\\',"'"]
    folderPath = path
    files = [file for file in glob.glob(folderPath + "**/*.DOC", recursive=True)]
    
    for file in files:
        file = re.sub(r'|'.join(map(re.escape, extraWords)), '', file)
        headlines.append(file)
        
        
    return headlines


"Path of the document"
def documentReturn(path):
    headlines = []
    extraWords = ['.doc','Urdu NEWS dataset\\','voa','bbc','dataset','entertainment','sports','miscleneous','politics','\\',"'"]
    folderPath = path
    files = [file for file in glob.glob(folderPath + "**/*.DOC", recursive=True)]
    return files


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
PAPER ALGORITHM IMPLEMENTATION
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def relatedNews(dataSet,inputNews):
    relatedNewsList = []
    t = 0.5
    dataSetList = dataSet
    ni = inputNews
    sizeofDataSetList = len(dataSetList)
    for j in range(0,sizeofDataSetList):
        nj = dataSetList[j]
        Sij = getSimilarityScore(ni,nj)
        if Sij >= t:
            relatedNewsList.append(nj)
        
    return relatedNewsList


"Similarity between input document(ith) and the jth document(document in the corpus)"
def getSimilarityScore(ni,nj):
    tli = getTokensList(ni)
    tlj = getTokensList(nj)
    sti = len(tli)
    stj = len(tlj)
    Sij = 0
    mij = 0
    
    for x in range(0,sti):
        for y in range(0,stj):
            if tli[x] == tlj[y]:
                mij = mij + 1
    
    if mij > 0:
        avg = (sti + stj)/2
        Sij = mij / avg
    
    return Sij



"Returns the token of the headlines with removed stop words"
def getTokensList(n):
    wordsWoSW = []
    words = []
    words = normalize(n)
    words = re.split('\W+',words)
    for word in words:
        if word in stop_words:
            continue
        wordsWoSW.append(word)
        
    return wordsWoSW



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


"MAIN FUNCTION"
def main():
    root = Tk()
    root.geometry('640x480')
    root.title("URDU NEWS CLUSTERRING")
    
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    
    
    "OnCLickViewListner: Trigger after the search Qeury"
    def OnClickViewListner():
        inputNews = entry_1.get()
        path = 'Urdu NEWS dataset\\'
        
        headlines = headlineReader(path)
        alfaz = splitWords(headlines)
        processedHeadlines = removeStopwords(alfaz)
        cluster = relatedNews(headlines,inputNews)
        docu = documentReturn(path)
        i = 0
        fop = open("InputNews.txt","w",encoding="utf-8")
        
       
        
        "ClickOnViewListner for the document view"
        def open_url(url):
            result = [s for s in docu if url[3:len(url)-1] in s]
            rs = str(result)
            ab =  "F:\\Subjects\\Python-WORKSPACE\\UrduNewsClusterring\\"
            ab = ab + rs[2:len(rs)-2]
            fp = open(ab.replace("\\\\","\\"),"r",encoding="utf-8")
            stri = fp.read()
            
            wind = Toplevel(root)
            window = Text(wind,height = 200, width = 100)
            window.pack()
            window.insert(END,stri)
            

        for j,url in enumerate(cluster):
            label=Label(root,text=url)
            label.bind("<Button-1>",lambda e,url=url:open_url(url))
            label.pack()
            fop.write("خبر"+": "+str(i+1))
            fop.write(str(url))
            fop.write("\n")
            i = i + 1
            
    
    label_1 = Label(root, text="Enter Query",font=('Courier',15))
    label_1.pack()
    entry_1 = Entry(root)    
    entry_1.config(width=50)    
    entry_1.pack()    
    button_1 = Button(root,text='Search',command= OnClickViewListner)
    button_1.pack()    
    root.mainloop()

    
    
if __name__ == '__main__':
    main()
