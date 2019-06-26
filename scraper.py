import requests, json, collections, re, os
from bs4 import BeautifulSoup

boards = ['/g/', '/v/', '/tv/', '/sp/', '/fa/', '/pol/', '/vg/',
          '/a/', '/b/', '/c/', '/d/', '/e/',
          '/f/', '/gif/', '/h/', '/hr/', '/k/',
          '/m/', '/o/', '/p/', '/r/', '/s/',
          '/t/', '/u/', '/vr/',
          '/w/', '/wg/', '/i/', '/ic/', '/r9k/',
          '/s4s/', '/vip/', '/cm/', '/hm/', '/lgbt/',
          '/y/', '/3/', '/aco/', '/adv/', '/an/',
          '/asp/', '/bant/', '/biz/', '/cgl/', '/ck/',
          '/co/', '/diy/', '/fit/', '/gd/', '/hc/',
          '/his/', '/int/', '/jp/', '/lit/', '/mlp/',
          '/mu/', '/n/', '/news/', '/out/', '/po/',
          '/qst/', '/sci/', '/soc/', '/tg/', 'toy',
          '/trv/', '/vp/', '/wsg/', '/wsr/', '/x/']

######################### SETUP DIRECTORIES ####################################

def setupDirs():
    try:
        os.mkdir('chanImages')
    except:
        pass

    for board in boards:
        try:
            os.mkdir(board)
        except:
                pass

######################### CATALOG PARSERS ######################################

def getJSONCatalog(url):
    response = requests.get(url)
    data = response.json()

    if "4cdn" in url:
        return parseFourCatalog(data)

def parseFourCatalog(data):
    titles = collections.OrderedDict()
    for i in range(0, 10):
        page = data[i]
        threadsList = page["threads"]
        for j in range(0, len(threadsList)):
            titles[threadsList[j]["semantic_url"]] = str(threadsList[j]["no"]) + '::' + str(threadsList[j]["replies"]) + '::' + str(threadsList[j]["images"])
    return titles

########################### THREAD PARSERS #####################################

def getJSONThread(url, chan, threadNumber):
    if "4chan" in chan:
        response = requests.get(url + str(threadNumber) + '.json')
        data = response.json()
        return parseFourThread(data)

def parseFourThread(data):
    comments = collections.OrderedDict()
    posts = data["posts"]
    for post in posts:
        try:
            comments[str(post["no"]) + '   ' + post["now"]] = post["com"]
        except:
            comments[str(post["no"]) + '   ' + post["now"]] = ''
    return comments

def getImageUrls(url, board):

    def load(url):
        req = requests.get(url)
        return str(req.content)

    thread_link = url
    page = BeautifulSoup(load(thread_link), "lxml")
    # print(page)
    extensionList = ('.jpg', '.jpeg', '.png', '.gif', '.webm')
    images = []

    for img in page.find_all('a', href=True):
        if board in str(img) and 'i.4cdn.org' in str(img):
            tagList = str(img).split('"')
            for tag in tagList:
                if board in str(tag):
                    if any(extension in tag for extension in extensionList):
                        images.append(str(tag))

    print(images)
    return images

########################### MAIN ##############################################

if __name__ == "__main__":
    # setupDirs()

    board = '/g/'
    # for board in boards:
    jsonCatalog = getJSONCatalog('https://a.4cdn.org' + board + 'catalog.json')
    for k, v in jsonCatalog.items():
        threadNumber = v.split('::')[0]
        print('https://boards.4channel.org' + board + 'thread/' + str(threadNumber))
        getImageUrls('https://boards.4channel.org' + board + 'thread/' + str(threadNumber), board)
        # print(jsonCatalog)
