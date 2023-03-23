const axios = require("axios");
const cheerio = require("cheerio");
const inquirer = require("inquirer");

const headers = {
  "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
};

const getPageHtml = async (url) => {
  try {
    return await axios.get(url, {
      headers: headers,
    });
  } catch (error) {
    console.error(error);
  }
};

const parsePosts = (html) => {
  let posts = [];
  const $ = cheerio.load(html.data);
  const $trs = $("table.gall_list tr.us-post");

  $trs.each(function (i, e) {
      no = $(this).find("td.gall_num").text(),
      title = $(this).find("td.gall_tit a").text(),
      url = "https://gall.dcinside.com" + $(this).find("td.gall_tit a").attr("href"),
      writerNick = $(this).find("td.gall_writer.ub-writer").attr("data-nick"),
      writerIP = $(this).find("td.gall_writer.ub-writer").attr("data-ip"),
      writerUID = $(this).find("td.gall_writer.ub-writer").attr("data-uid"),
      date = $(this).find("td.gall_date").attr("title"),
      posts[i] = {
        name: no + " | " + writerNick + " | " + title,
        value: {
          no: no,
          title: title,
          url: url,
          // 고닉: 닉네임(O), IP(X), UID(O)
          // 유독: 닉네임(O), IP(O), UID(X)
          writerNick: writerNick,
          writerIP: writerIP,
          writerUID: writerUID,
          date: date,
        },
      }});

  return posts;
};

const promptPostList = (galleryID, galleryPage) => {
  getPageHtml("https://gall.dcinside.com/board/lists?id=" + galleryID + "&page=" + galleryPage)
    .then((html) => parsePosts(html))
    .then((posts) => {
      inquirer.prompt([
        {
          pageSize: 50,
          type: "list",
          name: "post",
          message: "gallery",
          choices: posts,
        },

      ])
      .then(answers => {
        console.clear();
        promptPostDetail(answers.post, galleryID, galleryPage);
      });
    });
};

const promptPostDetail = (post, galleryID, galleryPage) => {
  getPageHtml(post.url)
    .then(html => {
      const $ = cheerio.load(html.data);
      const $write_div = $("div.write_div");
      // content = $write_div.text();
      content = "\n";
      content += post.title + "\n";
      content += post.date + "\n";
      content += post.writerNick;
      if (post.writerIP != "") {
        content += "(" + post.writerIP + ")";
      }
      content += "\n";
      content += "---------------------------------------------------------------------------------\n"
      $write_div.children().each(function (index, element) {
        content += $(this).text() + "\n";
      });
      return content;
    })
    .then(content => {
      inquirer.prompt([
        {
          type: "list",
          name: "menu",
          message: content + "\n",
          choices: [
            "return",
            "exit"
          ],
        },
      ])
      .then(answers => {
        // console.log(answers.menu)
        if (answers.menu == "return") { //debug 필요
          console.clear();
          promptPostList(galleryID, galleryPage);
        }
        if (answers.menu == "exit") { //debug 필요
          console.clear();
          return 0;
        }
      });
    })
}




const galleryID = "programming";
const galleryPage = "1";

promptPostList(galleryID, galleryPage);