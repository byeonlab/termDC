import requests
import bs4

def createUrl(pageNo):
    return "https://search.dcinside.com/post/p/%d/sort/1/q/.EC.95.A0.ED.94.8C.ED.8E.98.EC.9D.B4"%(pageNo)

if __name__ == '__main__':
    pages = list(range(1, 10))

    output = ""

    for page in pages:
        url = createUrl(page)
        resp = requests.get(url)
        
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        ul = soup.find("ul", {"class": "sch_result_list"})
        lis = ul.find_all("li")
        
        for li in lis:
            # print(li)
            title = li.find("a", {"class": "tit_txt"}).text
            url = li.find("a", {"class": "tit_txt"})["href"]
            summary = li.find("p", {"class": "link_dsc_txt"}).text
            sub = li.find("p", {"class": "link_dsc_txt dsc_sub"})
            gallery = sub.find("a", {"class": "sub_txt"}).text

            # if "비자" not in title + summary:
            #     continue

            output += "[ " + gallery + " ]" + "\n"
            output += title + "\n"
            output += summary + "\n"
            output += url + "\n"
            output += "\n"

    with open("output.txt", 'w') as f:
        f.write(output)
    

        # print (ul)