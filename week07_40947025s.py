#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import jieba
import os

def isNumber(Character):
    for i in ("0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9"):
        if Character == i:
            return 1
    return 0

#讀取 json 的程式
def jsonTextReader(jsonFilePath):
    with open(jsonFilePath , encoding="utf-8") as f:
        jsonFile = json.loads(f.read())
    return jsonFile

#將字串轉為「句子」列表的程式
def text2Sentence(inputSTR):
    for i in ("，" , "。" , "、" , "「" , "」" , "【" , "】" , "（" , "）" , "?" , "/" , ";" , ":" , "(" , ")"):
        inputSTR = inputSTR.replace( i , "MyCurringMark")
    for i in ("…" , "..."):
        inputSTR = inputSTR.replace( i, "")    
    #print("2: " + inputSTR)
    for i in range(len(inputSTR)):
        if inputSTR[i] == ",":
            if isNumber(inputSTR[i-1]) == 0 or isNumber(inputSTR[i+1]) == 0 :
                #print(inputSTR[i-1] , isNumber(inputSTR[i-1]) , inputSTR[i+1] , isNumber(inputSTR[i+1]) , inputSTR )
                inputSTR = inputSTR[0:i] + "MyCurringMark" + inputSTR[i+1:]
    #print("5: " + inputSTR)
    inputList = inputSTR.split("MyCurringMark")
    while "" in inputList:
        inputList.remove("")
    return inputList

#將資料夾內的所有文件jieba斷句
def text2cws(DocuPath , STR):
    allFileList = os.listdir(DocuPath)
    jsonFileList = []
    jiebaList = []
    #依標點符號斷句
    
    for j in allFileList:
        jsonFileText = jsonTextReader(DocuPath + j)[STR]
        jsonFileList.append(text2Sentence(jsonFileText))
    print("jsonFileList:")
    print(jsonFileList)
    
    #jieba斷句
    print("jiebaList:")
    for i in jsonFileList:
        jiebaList.append('/'.join(jieba.cut(i)))
    
    print(jiebaList)



if __name__== "__main__":
    #設定要讀取的 news.json 路徑
    docuTuple = ("finance/" , "health/")
    FilePath = "./example/"
    for i in docuTuple:
        text2cws(FilePath + i, "BODY")
        
            #print(jsonFileText)

""""
    #將 news.json 利用 [讀取 json] 的程式打開
    jsonFileText = jsonTextReader(jsonFilePath)["text"]
    #print("1: " + jsonFileText)
    #將讀出來的內容字串傳給 [將字串轉為「句子」 列表」]的程式，存為 newsLIST
    newsLIST = {"sentence" : text2Sentence(jsonFileText)}
    
    
    #設定要讀取的 test.json 路徑


    #將 test.json 的 sentenceLIST 內容讀出，存為 testLIST
    jsonFilePath = "./example/test.json"
    testLIST = jsonTextReader(jsonFilePath)
    
    
    #測試是否達到作業需求
    #print(newsLIST)
    #print(testLIST)
    if newsLIST == testLIST:
        print("作業過關！")
    else:
        print("作業不過關，請回到上面修改或是貼文求助！")
"""