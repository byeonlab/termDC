import requests
import bs4

headers = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
}

def getPosts(galleryId):
    url = "https://gall.dcinside.com/board/lists?id=" + galleryId

    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    trs = soup.find_all("tr", {"class": "ub-content us-post"})

    posts = []

    for tr in trs:
        title = tr.find("td", {"class": "gall_tit"}).find("a").text
        num = tr.find("td", {"class": "gall_num"}).text
        writerInfo = tr.find("td", {"class": "gall_writer ub-writer"})
        writerIP = writerInfo["data-ip"]
        writerNick = writerInfo["data-nick"]

        if tr.find("span", {"class": "reply_num"}):
            title += tr.find("span", {"class": "reply_num"}).text

        writer = writerNick
        if writerIP != "":
            writer += "(%s)" % writerIP
        date = tr.find("td", {"class": "gall_date"}).text

        posts.append((num, writer, title))
    
    return posts

def GetPost(galleryId, num):
    url = "https://gall.dcinside.com/board/view/?id=" + galleryId + "&no=" + num
    response = requests.get(url, headers=headers)

    return response

def ParsePostHeader(html):
    soup = bs4.BeautifulSoup(html, "html.parser")

    content = soup.find("div", {"class": "gallview_head"})

    title = content.find("span", {"class": "title_subject"}).text
    date = content.find("span", {"class": "gall_date"}).text

    writerData = content.find("div", {"class": "gall_writer ub-writer"})
    nick = writerData["data-nick"]
    ip = writerData["data-ip"]
    uid = writerData["data-uid"]

    data = {} 
    data["title"] = title
    data["nick"] = nick
    if ip != "":
        data["nick"] += "(%s)" % ip
    data["date"] = date

    return data

def ParsePostBody(html):
    soup = bs4.BeautifulSoup(html, "html.parser")

    # postHeader = soup.find("div", {"class": "gall_writer ub-writer"})
    content = soup.find("div", {'class':'write_div'})

    PostBody = ""

    for element in content:
        if element.text =="":
            continue

        PostBody += element.text + "\n"

    return PostBody


def GetComment(html):
    soup = bs4.BeautifulSoup(html, "html.parser")

    galleryId = soup.find("input", {"id": "gallery_id"})["value"]
    no = soup.find("input", {"id": "no"})["value"]
    e_s_n_o = soup.find("input", {"id": "e_s_n_o"})["value"]

    cmt_headers = {
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "ko-KR,ko;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Host": "gall.dcinside.com",
        "Origin": "https://gall.dcinside.com",
        "Referer": "https://gall.dcinside.com/board/view/?id=" + galleryId + "&no=" + no,
        "Connection": "keep-alive",
        "X-Requested-With": "XMLHttpRequest"
    }

    url = "https://gall.dcinside.com/board/comment/"
    data = {
        "id": galleryId,
        "no": no,
        "cmt_id": galleryId,
        "cmt_no": no,
        # "comment_page": 1,
        "e_s_n_o": e_s_n_o,
        "_GALLTYPE_": "G"
    }

    raw = requests.post(url, data=data, headers=cmt_headers).json()
    data = {
        "header": "",
        "comments": []
    }

    data["header"] = "댓글 수: %s" % raw["total_cnt"]

    if raw["comments"] != None:
        for e in raw["comments"]:
            comment = {}
            comment["memo"] = e["memo"]
            comment["reg_date"] = e["reg_date"]
            comment["name"] = e["name"]
            if e["nicktype"] == "00":
                comment["name"] += "(" + e["ip"] + ")"
            
            data["comments"].append(comment)

    return data
