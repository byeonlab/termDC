from textual.widgets import Static, DataTable
from textual.app import ComposeResult, Widget

### Gallery List ###
class GalleryList(DataTable):
    def __init__(self):
        DataTable.__init__(self)
        self.cursor_type = "row"
        self.add_columns("Gallery")

## PostList ###
class PostList(DataTable):
    def __init__(self):
        DataTable.__init__(self)
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
        Widget.__init__(self)
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
        Static.__init__(self)
        self.commentObject = commentObject

    def compose(self) -> ComposeResult:
        yield CommentWriterStatic(self.commentObject["name"])
        yield CommentMemoStatic(self.commentObject["memo"])
        yield CommentDateStatic(self.commentObject["reg_date"])

class CommentAreaWidget(Widget):
    def __init__(self, commentData):
        Widget.__init__(self)
        self.commentData = commentData

    def compose(self) -> ComposeResult:
        # render
        yield CommentAreaHeaderStatic(self.commentData["header"])
        for comment in self.commentData["comments"]:
            yield CommentItemStatic(comment)
