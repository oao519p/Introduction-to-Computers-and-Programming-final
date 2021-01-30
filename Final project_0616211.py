#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: UTF-8 -*-
import wikipedia
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import urllib.request, urllib.parse, urllib.error
from urllib.parse   import quote
from bs4 import BeautifulSoup
import argparse
import webbrowser

#---------------------------------define function::: 
##----------------------------------change the chinese input into japanese
def lanchange(page):
    url= page.url
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser') 
    soup1 = soup.find_all('li','interlanguage-link interwiki-ja')
    s = str(soup1)
    janame = s.split('"')[-2][:-5]
    return janame

##----------------------------------search the song in youtube
def youtube_search(anime, songname):
    youtube = build('youtube', 'v3',
        developerKey='AIzaSyDh6x3BFsh9_8wenURS6EZ2ChEJLNfPGDU')

    search_response = youtube.search().list(q=anime+' '+songname, part='id,snippet', maxResults=5).execute()
    print('---------------------------------------------------')
    print('Top 5 related videos on YouTube : \n')
    
    for i in range(5):
        print(str(i)+" "+search_response["items"][i]["snippet"]["title"])

    while True:
        try:
            youtubenum = int(input("\nPlease choose one and enter the num infront : "))
        except:
            print('*****Not number!*****\n')
            continue
        else:
            try:
                webbrowser.open_new_tab("https://youtu.be/"+search_response["items"][youtubenum]["id"]["videoId"])
                break
            except:
                print('*****Bad number!*****\n')
                continue

##----------------------------------cut the songpart in wiki
def section(janame):
    wikipedia.set_lang("ja")
    japage = wikipedia.page(janame)   #use the ja wikipage 
    songpart=japage.section("主題歌")
    return songpart
            
##----------------------------------find the songs in wiki

def findsong(janame):
    global songlist 
    songlist = []
    songpart = section(janame)  
    global songnum 
    songnum =0
    
    if songpart != None:
        songpart1 = songpart.replace('」','「')
        song = songpart1.split('「')
        i=0
        n=0     
        while i< len(song):
            if i%2==1:
                songlist = songlist + [song[i]]
                n = n+1
            i=i+1
        songnum = n  #n=1 means 1 song
        
        if songnum >0:
            print('---------------------------------------------------')
            print('Songs of this anime : \n')
            i=0
            for i in range(songnum):
                print(i, songlist[i])
                i = i+1
        else:#find no song or error
            print('*****Error finding songs!*****\n')
    
    else:  #find no song or error
            print('*****Error finding songs!*****\n')

##----------------------------------find the lyric from web
def lyric(songname):
    
    songname1= songname.replace(' ','+')
    url= 'http://lyric.evesta.jp/search.php?kind=title&keyword='+ quote(songname) +'&how=3&do=%E6%A4%9C%E7%B4%A2'
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    
    i=0
    tags = soup('a')
   
    for tag in tags:
        if tag.get('class', None)==['title']:
            i=i+1  #count the number of results
    
    if i>0:    
        if i>1:
            #save artist name in list
            artistlist = []
            artisttag = soup('p')
            for tagx in artisttag:
                if tagx.get('class', None)==['artist']:
                    artist = tagx.get_text()
                    artistlist = artistlist + [artist]

            #print out result
            i=0  
            print('\n')
            for tag in tags:
                if tag.get('class', None)==['title']:
                    print(str(i), tag.get_text(), artistlist[i])
                    i=i+1

            print('\nThere are more than one song has this name! ' )
            print('Please observe the youtube video\'s title and decide the artist of this song! ')

            while True:
                lyricnum = int(input('Please enter the number infront : '))
                if lyricnum >= i and lyricnum < 0:
                    print('*****Bad number!*****\n')
                    continue
                else:
                    break

            i=0
            for tag in tags:
                if tag.get('class', None)==['title']:
                    if i== lyricnum:
                        break
                    i=i+1

        else:  #only one result
            i=0
            for tag in tags:
                if tag.get('class', None)==['title']:
                    break
        print('---------------------------------------------------')
        print('Lyric of this song : ')
        #get the lyric
        href = str(tag.get('href',None))
        url = 'http://lyric.evesta.jp/' + href
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        soup1 = soup.find('div',id="lyricbody")
        print(soup1.get_text())
    else:
        print('*****Error finding lyric!*****\n')

##----------------------------------search in gamer 巴哈姆特 by using google custom search API
my_api_key = "AIzaSyC254DtyqnZr84kWViggkmAjy9UTciO36Y"
gamer_cse_id = "001769628158235379459:kxdttamr1i8"

def google_gamer_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey="AIzaSyC254DtyqnZr84kWViggkmAjy9UTciO36Y")
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

def gamer_search(zhname):
    res = google_gamer_search(zhname, my_api_key, gamer_cse_id, num=5)
    try:
        result = res['items']
        print('---------------------------------------------------')
        print('Related 5 Gamer page : \n')
        i=0
        for results in result:
            print(i, result[i]["title"])
            #print(result[i]["link"])
            i=i+1
        while True:
            try:
                gamernum = int(input('\nPlease enter the number infront: '))
            except:
                print('*****Not number!*****\n')
                continue
            else:
                if gamernum>=0 and gamernum<=4:
                    break
                else:
                    print('*****Bad number!*****\n')
        webbrowser.open_new_tab(result[gamernum]["link"]) 
        
    except:
        print('*****Bad Search in Gamer!*****\n')
    
##----------------------------------search in bilibili by using google custom search API    
bili_cse_id = "001769628158235379459:rqps90nqxlq"

def google_bili_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey="AIzaSyC254DtyqnZr84kWViggkmAjy9UTciO36Y")
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

def bili_search(zhname):
    res = google_bili_search(zhname, my_api_key, bili_cse_id, num=5)
    try:
        result = res['items']
        print('---------------------------------------------------')
        print('Top 5 videos on Bilibili : \n')
        i=0
        for results in result:
            print(i, result[i]["title"])
            #print(result[i]["link"])
            i=i+1
        while True:
            try:
                bilinum = int(input('\nPlease enter the number infront: '))
            except:
                print('*****Not number!*****\n')
                continue
            else:
                if bilinum>=0 and bilinum<=4:
                    break
                else:
                    print('*****Bad number!*****\n')

        webbrowser.open_new_tab(result[bilinum]["link"])
        
    except:
        print('*****Bad Search in bilibili!*****\n')
        
#---------------------------------main code part:::
zhname = input('Please enter an anime name: ')

while True:
    print('---------------------------------------------------')
    print('Function you can do : \n')
    print('0 Find the song in this anime')
    print('1 Search in gamer 巴哈姆特 ')
    print('2 Search in BiliBili (Top 5 related) \n')

    try:
        askdo1 = int(input('Please enter the number infront to do the function : '))
    except:
        print('*****Not number!*****\n')
        continue
    
    else:
        if askdo1 <0 or askdo1>2:
            print('*****Bad number!*****\n')
            continue
        else:           
##----------------------------------search in gamer
            if askdo1==1:
                gamer_search(zhname)
            
                askotherfun = input('> Do you want to do other function? \nEnter "y" if need, "n" if not : ')
                if askotherfun =='y' or askotherfun =='Y':
                    continue
                else:
                    break #end the pro
##----------------------------------search in bili
            if askdo1==2:
                bili_search(zhname)
            
                askotherfun = input('> Do you want to do other function? \nEnter "y" if need, "n" if not : ')
                if askotherfun =='y' or askotherfun =='Y':
                    continue
                else:
                    break
##----------------------------------search in wiki > songs
            if askdo1 == 0:

    ###----------------------------------find wiki page    
                wikipedia.set_lang("zh")
                wikisearch = wikipedia.search(zhname, 5)
                print('---------------------------------------------------')

                try:
                    n=0
                    print('Related wikipage : \n')
                    for result in wikisearch:
                        print(n, result)
                        n=n+1
                except:
                    print('*****Bad search! suggestion: Change a name!******\n')
                    break

                else:
                    while True: #get the correct wiki page
                        try:
                            num = int(input('\nPlease enter the number infront: '))
                        except:
                            print('*****Not number!*****\n')
                            continue
                        else:
                            try:
                                page = wikipedia.page(wikisearch[num])  
                                break
                            except:
                                print('*****Bad number!*****\n')
                                continue

                    #lan change by function    
                    try:
                        janame = lanchange(page)

                    except:
                        print('*****Bad change to Japanese! Fail of using this function*****\n')
                        continue

                ###----------------------------------find songs in page
                    else:
                        findsong(janame)

                ###----------------------------------select the song
                        while songnum >0:

                            while True: #get the songname
                                try:
                                    songnumber = int(input('\nPlease enter the song\'s number infront : '))
                                except:
                                    print('*****Not number!*****\n')
                                    continue

                                else:
                                    if songnumber>=0 and songnumber < songnum:
                                        songname = songlist[songnumber]
                                        break

                                    else:
                                        print('*****Bad number!*****\n')
                                        continue
                ###----------------------------------do things to the song 

                            print('---------------------------------------------------')
                            print('Function you can do : \n')
                            print('0 Search the song in Youtube (Top 5 related)(*prefer)')
                            print('1 Find the lyric \n')

                            while True: #get which function to do  
                                try:
                                    askdo2 = int(input('Please enter the number infront to do the function : '))
                                except:
                                    print('*****Not number!*****\n')
                                    continue
                                else: 
                                    if askdo2>=0 and askdo2 <=1:
                                        break
                                    else:
                                        print('*****Bad number!*****\n')
                                        continue

                ###----------------------------------search in youtube and ask lyric
                            if askdo2 == 0:
                                youtube_search(janame, songname)
                                asklyric = input('> Do you need the lyric of this song? \n> Enter "y" if need, "n" if not : ')

                                if asklyric =='y' or asklyric =='Y':
                                    lyric(songname)

                ###----------------------------------search lyric and ask song
                            if askdo2 == 1:
                                lyric(songname)
                                asksong = input('> Do you need the song? \n> Enter "y" if need, "n" if not : ')
                                if asksong =='y' or asksong =='Y':
                                    youtube_search(janame, songname)

                ###----------------------------------ask to repeat the loop or not
                            askothersong =input('> Do you want to use other song? \nEnter "y" if need, "n" if not : ')
                            print('---------------------------------------------------\n')
                            if askothersong =='y' or askothersong =='Y':
                                i=0
                                for i in range(songnum):
                                    print(i, songlist[i])
                                    i = i+1
                                continue
                            else:
                                break  #leave song loop
                
                askotherfun = input('> Do you want to do other function? \nEnter "y" if need, "n" if not : ')
                if askotherfun =='y' or askotherfun =='Y':
                    continue
                else:
                    break #end the pro
  
    
print('---------------------------------------------------')
print('Thanks for using this project! Bye Bye!')
print('       \(“￣▽￣)-o█ █o-(￣▽￣”)/        ')


# In[ ]:




