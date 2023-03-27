import requests
import bs4

headers = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
}

def getPosts():
    url = "https://gall.dcinside.com/board/lists?id=programming"


    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    trs = soup.find_all("tr", {"class": "ub-content us-post"})


    posts = [("num", "writer", "title")]

    for tr in trs:
        title = tr.find("td", {"class": "gall_tit"}).find("a").text
        num = tr.find("td", {"class": "gall_num"}).text
        writerInfo = tr.find("td", {"class": "gall_writer ub-writer"})
        writerIP = writerInfo["data-ip"]
        writerNick = writerInfo["data-nick"]

        writer = writerNick
        if writerIP != "":
            writer += "(%s)" % writerIP
        date = tr.find("td", {"class": "gall_date"}).text

        posts.append((num, writer, title))
    
    return posts

        # print(date)
        # print(writerNick)
        # print(title)
        # print()


def ReadPost(num):
    url = "https://gall.dcinside.com/board/view/?id=programming&no=" + num
    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    content = soup.find("div", {'class':'write_div'})

    return content.text
