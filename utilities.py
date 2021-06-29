def getPrevPage(name, page):
    if(int(page) <= 1):
        return 'none'
    nextpage = int(page) - 1
    link = 'http://localhost:5000/comic/' + name + '/' + str(nextpage)
    return link

def getNextPage(name, page):
    if(int(page) >= 3):
        return 'none'
    nextpage = int(page) + 1
    link = 'http://localhost:5000/comic/' + name + '/' + str(nextpage)
    return link