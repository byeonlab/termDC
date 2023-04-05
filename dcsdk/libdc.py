import requests
import bs4
from collections import OrderedDict

"""HTTP Headers for gallery requests"""
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
}

class Gallery:
    """Represents specific gallery with gallery id"""
    def __init__(self, id: str, page: int = 1):
        self.id = id
        self.page = page

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
            "https://gall.dcinside.com/board/lists", 
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
            title = tr.find("td", {"class": "gall_tit"}).find("a").text
            if tr.find("span", {"class": "reply_num"}):
                title += tr.find("span", {"class": "reply_num"}).text

            # num
            num = tr.find("td", {"class": "gall_num"}).text

            # writer
            writer_data = tr.find("td", {"class": "gall_writer ub-writer"})
            ip = writer_data["data-ip"]
            nick = writer_data["data-nick"]
            writer = nick
            if ip is not "":
                writer += f"({ip})" 

            # date
            date = tr.find("td", {"class": "gall_date"}).text

            posts.append((num, writer, title, date))

        return posts

class Post:
    """Represents a post with a specific gallery id and post number"""
    def __init__(self, gallery_id: str, no: str):
        self.gallery_id = gallery_id
        self.no = no
        self.http_response = requests.get(
            "https://gall.dcinside.com/board/view/",
            headers=HEADERS,
            params={
                "id" : gallery_id,
                "no" : no
            }
        )

    """Returns html code for a post"""
    def get_html(self) -> str:
        return self.http_response.text

    """Returns post header data(title, writer, date) as dict"""
    def headers(self) -> dict:
        soup = bs4.BeautifulSoup(self.http_response.text, "html.parser")
        content = soup.find("div", {"class": "gallview_head"})
        title = content.find("span", {"class": "title_subject"}).text
        date = content.find("span", {"class": "gall_date"}).text

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
        body = ""

        for element in write_div:
            if element.text == "":
                continue

            body += f"{element.text}\n"

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
            "Referer": f"https://gall.dcinside.com/board/view/?id={self.gallery_id}&no={self.no}",
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
            "header": f"댓글 수: {json_response['total_cnt']}",
            "comments": {}
        })

        if json_response["comments"] != None:
            for e in json_response["comments"]:
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
