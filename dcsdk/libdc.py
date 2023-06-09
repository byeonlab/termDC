import requests
import bs4
from collections import OrderedDict

"""HTTP Headers for gallery requests"""
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
}

class Gallery:
    BASE_URL = "https://gall.dcinside.com/board/lists/"
    TYPE = "major"

    """Represents specific gallery with gallery id"""
    def __init__(self, id: str, page: int = 1):
        self.id = id
        self.page = page

    """Set page number"""
    def set_page(self, page_number):
        self.page = page_number

    """Increments page number""" 
    def increment_page(self) -> None:
        self.page += 1

    """Decrements page number"""
    def decrement_page(self) -> None:
        if self.page > 1:
            self.page -= 1

    """Returns list of posts of current page"""
    def posts(self) -> list:
        response = requests.get(
            url=self.BASE_URL, 
            headers=HEADERS,
            params={
                "id" : self.id,
                "page" : self.page
            }
        )

        soup = bs4.BeautifulSoup(response.text, "html.parser")
        trs = soup.find_all("tr", {"class": "ub-content us-post"})
        posts = []

        for tr in trs:
            # title
            title = tr.find("td", {"class": "gall_tit"}).find("a").get_text()
            if tr.find("span", {"class": "reply_num"}):
                title += tr.find("span", {"class": "reply_num"}).get_text()

            # num
            num = tr.find("td", {"class": "gall_num"}).get_text()

            # writer
            writer_data = tr.find("td", {"class": "gall_writer ub-writer"})
            ip = writer_data["data-ip"]
            nick = writer_data["data-nick"]
            writer = nick
            if ip:
                writer += f"({ip})" 

            # date
            date = tr.find("td", {"class": "gall_date"}).get_text()

            posts.append((num, writer, title, date))

        return posts

class MinorGallery(Gallery):
    """Represents a minor gallery with given gallery id"""
    BASE_URL = "https://gall.dcinside.com/mgallery/board/lists/"
    TYPE = "minor"

class Post:
    BASE_URL = "https://gall.dcinside.com/board/view/"

    """Represents a post with a specific gallery id and post number"""
    def __init__(self, gallery_id: str, no: str):
        self.gallery_id = gallery_id
        self.no = no
        self.http_response = requests.get(
            url=self.BASE_URL,
            headers=HEADERS,
            params={
                "id" : gallery_id,
                "no" : no
            }
        )

    """Returns post header data(title, writer, date) as dict"""
    def headers(self) -> dict:
        soup = bs4.BeautifulSoup(self.http_response.text, "html.parser")
        content = soup.find("div", {"class": "gallview_head"})
        title = content.find("span", {"class": "title_subject"}).get_text()
        date = content.find("span", {"class": "gall_date"}).get_text()

        writer_data = content.find("div", {"class": "gall_writer ub-writer"})
        nick = writer_data["data-nick"]
        ip = writer_data["data-ip"]
        uid = writer_data["data-uid"]

        headers = {}
        headers["title"] = title
        headers["nick"] = nick
        if ip != "":
            headers["nick"] += f"({ip})"
        headers["date"] = date

        return headers

    """Returns post body as string"""
    def body(self) -> str:
        soup = bs4.BeautifulSoup(self.http_response.text, "html.parser")
        write_div = soup.find("div", {'class': 'write_div'})
        imgs = write_div.find_all("img")
        for img in imgs:
            # img.replace_with(f"\n Image: [@click='{img['src']}']link[/]\n")
            img.replace_with("[이미지: 렌더링 구현예정]")
        body = write_div.get_text("\n")

        return body

    """Returns comment data as OrderedDict"""
    def comments(self, comment_page: int = 1) -> OrderedDict:
        soup = bs4.BeautifulSoup(self.http_response.text, "html.parser")

        COMMENT_HEADERS = HEADERS.copy()
        COMMENT_HEADERS.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "ko-KR,ko;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Host": "gall.dcinside.com",
            "Origin": "https://gall.dcinside.com",
            "Referer": f"{self.BASE_URL}?id={self.gallery_id}&no={self.no}",
            "Connection": "keep-alive",
            "X-Requested-With": "XMLHttpRequest"
        })

        gallery_id = soup.find("input", {"id": "gallery_id"})["value"]
        no = soup.find("input", {"id": "no"})["value"]
        e_s_n_o = soup.find("input", {"id": "e_s_n_o"})["value"]
        url = "https://gall.dcinside.com/board/comment/"

        data = {
            "id": gallery_id,
            "no": no,
            "cmt_id": gallery_id,
            "cmt_no": no,
            "comment_page": comment_page,
            "e_s_n_o": e_s_n_o,
            "_GALLTYPE_": "G"
        }

        json_response = requests.post(url, data=data, headers=COMMENT_HEADERS).json()

        comment_data = OrderedDict({
            "header": {"comment_cnt": json_response['total_cnt']},
            "comments": {}
        })

        if json_response["comments"] != None:
            for e in json_response["comments"]:
                if e["name"] == "댓글돌이":
                    continue
                comment = {}
                comment["no"] = e["no"]
                comment["depth"] = e["depth"]
                comment["c_no"] = e["c_no"]
                comment["memo"] = e["memo"]
                comment["reg_date"] = e["reg_date"]
                comment["name"] = e["name"]
                if e["nicktype"] == "00":
                    comment["name"] += "(" + e["ip"] + ")"

                depth = int(e["depth"])
                if depth == 0:
                    comment["subcomments"] = []
                    comment_data["comments"].update({comment["no"]: comment})
                else:
                    parents = comment_data["comments"].get(e["c_no"], "0")
                    parents["subcomments"].append(comment)

        return comment_data      

class MinorPost(Post):
    BASE_URL = "https://gall.dcinside.com/mgallery/board/view/"