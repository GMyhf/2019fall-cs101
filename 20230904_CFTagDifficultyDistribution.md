# codeforces.com 的题目类型、难度分布

Updated 2243 GMT+8 Sep 4, 2023								

2023 fall, Complied by Hongfei Yan



2023年9月4日 ，为了统计出如图1所示的 codeforces.com 的题目类型、难度分布的热力图，从 https://github.com/GMyhf/2019fall-cs101 找到了 20191120_CodeforceGuide.pptx，以及 codeforces_v0.3.py。

![image-20230904232838495](https://raw.githubusercontent.com/GMyhf/img/main/img/image-20230904232838495.png)

图1. codeforces.com 的题目类型、难度分布



## **1. 抓取部分修改部分代码**

因为过了三年，.py 程序需要修正，首先还是爬取网页，目前CF所有问题分布在89个页面中，可以构造89个url抓取。但是 codeforces.com现在封禁的很厉害，即使随机暂停20～90秒才抓取一个页面，多了还是会被封。所以只能10个页面一组抓取，都拿到后，再合并成一个文件 20230904_CodeForces-ProblemSet.csv。

```python
import urllib.request from 
urllib.request import Request 

# %% retrieve the problem set
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
```



```python
import random

#last_page = 89  # the total page number of problem set page
last_page = 30
url = ['http://codeforces.com/problemset/page/%d' % page for page in range(21, last_page + 1)]
for foo in url:
    print('Processing URL %s' % foo)
    spider(foo)
    # wait time to avoid the blocking of spider
    # 生成一个随机的等待时间，范围为20-90秒
    random.seed()
    wait_time = random.randint(20, 90)
    print('Wait %f seconds' % wait_time)
    time.sleep(wait_time)
```



## **2. 分析可视化部分修改代码**

之后要正确显示出热力图，.py 还需要修改两处，都是

```
tags = codeforces[id]['tags'] 
```

修改为 

```
tags = codeforces[id]['tags'].split(",")
```



修改部分代码

```python
# %% analyze the problem set
# initialize the difficult and tag list
difficult_level = {}
tags_level = {}
for id in codeforces:
    difficult = re.findall('([A-Z])', id)[0]
    tags = codeforces[id]['tags'].split(",")
    difficult_level[difficult] = difficult_level.get(difficult, 0) + 1
    for tag in tags:
        tags_level[tag] = tags_level.get(tag, 0) + 1
```



```python
# construct the 2D relationships matrix
for id in codeforces:
    difficult = re.findall('([A-Z])', id)[0]
    difficult_id = difficult_list.index(difficult)
    tags = codeforces[id]['tags'].split(",")
    solved = codeforces[id]['solved']
    for tag in tags:
        tag_id = tag_list.index(tag)
        matrix_solved[tag_id][difficult_id] += int(solved)
        matrix_freq[tag_id][difficult_id] += 1
```