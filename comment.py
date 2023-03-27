import requests

headers = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
    # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    # "Accept": "application/json, text/javascript, */*; q=0.01",
    # "Accept-Language": "ko-KR,ko;q=0.9",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Host": "gall.dcinside.com",
    # "Origin": "https://gall.dcinside.com",
    # "Referer": "https://gall.dcinside.com/board/view/?id=programming&no=2445209&page=1",
    # "Connection": "keep-alive",
    "X-Requested-With": "XMLHttpRequest"
}

if __name__ == '__main__':
    url = "https://gall.dcinside.com/board/comment/"
    data = {
        "id": "programming",
        "no": 2445209,
        "cmt_id": "programming",
        "cmt_no": 2445209,
        "comment_page": 1,
        "e_s_n_o": "3eabc219ebdd65f7",
        "_GALLTYPE_": "G"
    }
    resp = requests.post(url, data=data, headers=headers)
    commentResp = resp.json()
    for comment in commentResp["comments"]:
        print(comment["name"], ": ", comment["memo"])