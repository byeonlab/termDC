const axios = require('axios');
const cheerio = require("cheerio");
const inquirer = require("inquirer");

const headers = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
}

const buildTargetUrl = (urlPrefix, galleryID, galleryPage) => {
    return urlPrefix + galleryID + "&page=" + galleryPage;
}

const urlPrefix = "https://gall.dcinside.com/board/lists?id=";
const galleryID = "programming";
const galleryPage = "1";

const getPageHtml = async (url) => {
    try {
      return await axios.get(url, {
        headers: headers
      });
    } catch (error) {
      console.error(error);
    }
};

getPageHtml(buildTargetUrl(urlPrefix, galleryID, galleryPage))
    .then(html => {
        let posts = []
        const $ = cheerio.load(html.data);

        const $trs = $("table.gall_list tr.us-post")
        $trs.each(function (i, e) {
                no = $(this).find("td.gall_num").text(),
                title = $(this).find("td.gall_tit a").text(),
                url = "https://gall.dcinside.com" + $(this).find("td.gall_tit a").attr("href"),
                writerNick = $(this).find("td.gall_writer.ub-writer").attr("data-nick"),
                writerIP = $(this).find("td.gall_writer.ub-writer").attr("data-ip"),
                writerUID = $(this).find("td.gall_writer.ub-writer").attr("data-uid"),
                date = $(this).find("td.gall_date").attr("title"),

                posts[i] = {
                    name: no + " | " +  writerNick + " | "  + title, 
                    value: {
                      no: no,
                      title: title,
                      url: url,
                      // 고닉: 닉네임(O), IP(X), UID(O)
                      // 유독: 닉네임(O), IP(O), UID(X)
                      writerNick: writerNick,
                      writerIP: writerIP,
                      writerUID: writerUID,
                      date: date
                    }
                }
            }
        )
        return posts;
    }
).then(posts => {
     inquirer
    .prompt([
      {
        type: 'list',
        name: 'post',
        message: 'gallery',
        choices: posts,
      },
    ]).then(answers => {
      getPageHtml(answers.post.url)
      .then(html => {
        const $ = cheerio.load(html.data);
        const $ps = $("div.write_div p");

        $ps.each(function (index, element) {
          console.log($(this).text());
        });
      });
    }
    )
  }
);
