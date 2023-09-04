#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#http://blog.greenwicher.com/2017/01/03/codeforces-problemset/

"""
Created on Tue Jan  3 10:29:52 2017 by liuweizhi

updated on Nov. 3, 2019 by Hongfei Yan
"""

import re
import urllib.request
from urllib.request import Request
from bs4 import BeautifulSoup
import os
import csv
import time

#%% retrieve the problem set
def spider(url):
    req = Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print("Error:", e.code)
        import sys;
        sys.exit(0)

    #response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response.read(), 'html.parser')
    pattern = {'name': 'tr'}
    content = soup.findAll(**pattern)
    #content = soup.findAll('tr')
    for row in content:
        item = row.findAll('td')
        try:
            # get the problem id
            id = item[0].find('a').string.strip()
            #print('====item[0]====\n {}\n\n', item[0])
            col2 = item[1].findAll('a')
            #print('====item[1]====\n {}\n\n',item[1])
            # get the problem title 
            title = col2[0].string.strip()
            # get the problem tags
            tags = [foo.string.strip() for foo in col2[1:]]
            # get the number of AC submissions
            solved = re.findall('x(\d+)', str(item[4].find('a')))[0]
            #print('====item[4]====\n {}\n\n', item[4])
            # update the problem info         
            codeforces[id] = {'title':title, 'tags':tags, 'solved':solved, 'accepted':0}
            #print("id = {}".format(id))
            #print(codeforces[id])
        except:
            continue
    return soup
    
codeforces = {}
wait = 15 # wait time to avoid the blocking of spider
last_page = 89 # the total page number of problem set page
url = ['http://codeforces.com/problemset/page/%d' % page for page in range(1,last_page+1)]
for foo in url:
    print('Processing URL %s' % foo)
    spider(foo)
    print('Wait %f seconds' % wait)
    time.sleep(wait)

#%% mark the accepted problems
def accepted(url):
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response.read(), 'html.parser')
    pattern = {'name':'table', 'class':'status-frame-datatable'}
    table = soup.findAll(**pattern)[0]
    pattern = {'name': 'tr'}
    content = table.findAll(**pattern)
    for row in content:
        try:
            item = row.findAll('td')
            # check whether this problem is solved 
            if 'Accepted' in str(row):
                #print('====accepted: item[3]====\n {}\n\n', item[3])
                line = item[3].find('a')
                #print('==line: {}'.format(line))
                link = line.get('href')
                #print('==link: {}'.format(link))
                id_pre = re.findall('(\d+)', link)[0]
                #print('==id_pre: {}'.format(id_pre))
                id = str(id_pre) + line.string.split('-')[0].strip()
                #print("id = {}".format(id))
                
                codeforces[id]['accepted'] = 1
        except:
            continue
    return soup
    
wait = 15 # wait time to avoid the blocking of spider
#last_page = 10 # the total page number of user submission
last_page = 8 # the total page number of user submission
handle = 'GMyhf' # please input your handle
url = ['http://codeforces.com/submissions/%s/page/%d' % (handle, page) for page in range(1, last_page+1)]
for foo in url:
    print('Processing URL %s' % foo)
    accepted(foo)
    print('Wait %f seconds' % wait)
    time.sleep(wait) 

#%% output the problem set to csv files
root = os.getcwd()
with open(os.path.join(root,"CodeForces-ProblemSet.csv"),"w", encoding="utf-8") as f_out:
    f_csv = csv.writer(f_out)
    f_csv.writerow(['ID', 'Title', 'Tags', 'Solved', 'Accepted'])
    for id in codeforces:
        title = codeforces[id]['title']
        tags = ', '.join(codeforces[id]['tags'])
        solved = codeforces[id]['solved']
        accepted = codeforces[id]['accepted']
        f_csv.writerow([id, title, tags, solved, accepted])
    f_out.close()
    
#%% analyze the problem set
# initialize the difficult and tag list
difficult_level = {}
tags_level = {}
for id in codeforces:
    difficult = re.findall('([A-Z])', id)[0]
    tags = codeforces[id]['tags']
    difficult_level[difficult] = difficult_level.get(difficult, 0) + 1
    for tag in tags:
        tags_level[tag] = tags_level.get(tag, 0) + 1
import operator        
tag_level = sorted(tags_level.items(), key=operator.itemgetter(1))[::-1]
tag_list = [foo[0] for foo in tag_level]
difficult_level = sorted(difficult_level.items(), key=operator.itemgetter(0))
difficult_list = [foo[0] for foo in difficult_level]

# initialize the 2D relationships matrix 
# matrix_solved: the number of AC submission for each tag in each difficult level
# matrix_freq: the number of tag frequency for each diffiicult level
matrix_solved, matrix_freq = [[[0] * len(difficult_list) for _ in range(len(tag_list))] for _ in range(2)]


# construct the 2D relationships matrix
for id in codeforces:
    difficult = re.findall('([A-Z])', id)[0]
    difficult_id = difficult_list.index(difficult)
    tags = codeforces[id]['tags']
    solved = codeforces[id]['solved']
    for tag in tags:
        tag_id = tag_list.index(tag)
        matrix_solved[tag_id][difficult_id] += int(solved)
        matrix_freq[tag_id][difficult_id] += 1

#%% visualization
root = os.getcwd()

def outputMatrix(name, data):
    with open(os.path.join(root,name),"w", encoding="utf-8") as f_out:
        f_csv = csv.writer(f_out)
        f_csv.writerow(['Tags/Difficult '] + difficult_list)
        for i in range(len(tag_list)):
            tag = tag_list[i]
            f_csv.writerow([tag]+data[i])        
        f_out.close()
    return
    
outputMatrix('Matrix-Solved.csv', matrix_solved)
outputMatrix('Matrix-Freq.csv', matrix_freq)

