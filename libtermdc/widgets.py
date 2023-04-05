from textual.widgets import Static, DataTable
from textual.app import ComposeResult, Widget

### Gallery List ###


class GalleryList(DataTable):
    def __init__(self):
        super().__init__()
        self.cursor_type = "row"
        self.add_columns("Gallery")

## PostList ###


class PostList(DataTable):
    def __init__(self):
        super().__init__()
        self.cursor_type = "row"
        self.add_columns("No", "Writer", "Title", "Date")

### PostRead###


class PostTitleStatic(Static):
    pass


class PostWriterStatic(Static):
    pass


class PostDateStatic(Static):
    pass


class PostHeaderWidget(Widget):
    def __init__(self, headers):
        super().__init__()
        self.title = headers["title"]
        self.writer = headers["nick"]
        self.date = headers["date"]

    def compose(self) -> ComposeResult:
        # render
        yield PostTitleStatic(self.title)
        yield PostWriterStatic(self.writer)
        yield PostDateStatic(self.date)


class PostBodyWidget(Static):
    pass

## Comments ###


class CommentAreaHeaderStatic(Static):
    pass


class CommentWriterStatic(Static):
    pass


class CommentMemoStatic(Static):
    pass


class CommentDateStatic(Static):
    pass


class CommentItemStatic(Static):
    def __init__(self, comment):
        super().__init__()
        self.comment = comment

    def compose(self) -> ComposeResult:
        yield CommentWriterStatic(self.comment["name"])
        yield CommentMemoStatic(self.comment["memo"])
        yield CommentDateStatic(self.comment["reg_date"])
        yield SubCommentItemStatic(self.comment["subcomments"])


class SubCommentItemStatic(Static):
    def __init__(self, subcomments):
        super().__init__()
        self.subcomments = subcomments

    def compose(self) -> ComposeResult:
        for subcomment in self.subcomments:
            yield CommentWriterStatic("┗ " + subcomment["name"], classes="subCommentAreaWidget")
            yield CommentMemoStatic(subcomment["memo"], classes="subCommentAreaWidget")
            yield CommentDateStatic(subcomment["reg_date"], classes="subCommentAreaWidget")


class CommentAreaWidget(Widget):
    def __init__(self, comment_data):
        super().__init__()
        self.comment_data = comment_data

    def compose(self) -> ComposeResult:
        # render
        yield CommentAreaHeaderStatic(self.comment_data["header"])
        for comment in self.comment_data["comments"].values():
            yield CommentItemStatic(comment)
