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
    def __init__(self, PostHeaderData):
        super().__init__()
        self.title = PostHeaderData["title"]
        self.writer = PostHeaderData["nick"]
        self.date = PostHeaderData["date"]

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
    def __init__(self, commentObject):
        super().__init__()
        self.commentObject = commentObject

    def compose(self) -> ComposeResult:
        yield CommentWriterStatic(self.commentObject["name"])
        yield CommentMemoStatic(self.commentObject["memo"])
        yield CommentDateStatic(self.commentObject["reg_date"])
        yield SubCommentItemStatic(self.commentObject["subcomments"])


class SubCommentItemStatic(Static):
    def __init__(self, subCommentObject):
        super().__init__()
        self.subCommentObject = subCommentObject

    def compose(self) -> ComposeResult:
        for e in self.subCommentObject:
            yield CommentWriterStatic("┗ " + e["name"], classes="subCommentAreaWidget")
            yield CommentMemoStatic(e["memo"], classes="subCommentAreaWidget")
            yield CommentDateStatic(e["reg_date"], classes="subCommentAreaWidget")


class CommentAreaWidget(Widget):
    def __init__(self, commentData):
        super().__init__()
        self.commentData = commentData

    def compose(self) -> ComposeResult:
        # render
        yield CommentAreaHeaderStatic(self.commentData["header"])
        for comment in self.commentData["comments"].values():
            yield CommentItemStatic(comment)
