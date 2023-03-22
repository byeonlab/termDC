const axios = require('axios');
const cheerio = require("cheerio");

const headers = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
}

const buildTargetUrl = (urlPrefix, galleryID, galleryPage) => {
    return urlPrefix + galleryID + "&page=" + galleryPage;
}

const urlPrefix = "https://gall.dcinside.com/board/lists?id=";
const galleryID = "programming";
const galleryPage = "1";

const getPostList = async () => {
    try {
      return await axios.get(buildTargetUrl(urlPrefix, galleryID, galleryPage), {
        headers: headers
      });
    } catch (error) {
      console.error(error);
    }
};

getPostList()
    .then(html => {
        let posts = []
        const $ = cheerio.load(html.data);

        const $trs = $("table.gall_list tr.us-post")
        $trs.each(function (i, e) {
                posts[i] = {
                    no: $(this).find("td.gall_num").text(),
                    title: $(this).find("td.gall_tit a").text(),
                    uri: $(this).find("td.gall_tit a").attr("href"),
                    // 고닉: 닉네임(O), IP(X), UID(O)
                    // 유독: 닉네임(O), IP(O), UID(X)
                    writerNick: $(this).find("td.gall_writer.ub-writer").attr("data-nick"),
                    writerIP: $(this).find("td.gall_writer.ub-writer").attr("data-ip"),
                    writerUID: $(this).find("td.gall_writer.ub-writer").attr("data-uid"),
                    date: $(this).find("td.gall_date").attr("title")

                }
            }
        )
        return posts;
    }
).then(res => console.log(res));
