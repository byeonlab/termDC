from textual.widgets import Static, DataTable
from textual.app import ComposeResult, Widget

### Gallery List ###
class GalleryList(DataTable):
    """DataTable for gallery list"""
    def __init__(self):
        super().__init__()
        self.cursor_type = "row"
        self.add_columns("Name", "Type")

##$ Post List ###
class PostListHeader(Widget):
    def __init__(self, gallery_name: str, page: int = 1):
        super().__init__()
        self.gallery_name = gallery_name

    def compose(self) -> ComposeResult:
        yield Static()
    
    def on_mount(self):
        self.update_page()

    def update_page(self, page: int = 1):
        self.query_one(Static).update(f"{self.gallery_name} (page: {page})")

class PostList(DataTable):
    """Datatable for post list"""
    def __init__(self):
        super().__init__()
        self.cursor_type = "row"
        self.add_columns("No", "Writer", "Title", "Date")

### Post Details ###
class PostTitleStatic(Static):
    """Displays post title"""
    pass

class PostWriterStatic(Static):
    """Displays post writer"""
    pass


class PostDateStatic(Static):
    """Displays post date"""
    pass


class PostHeaderWidget(Widget):
    """Widget for post header"""
    def __init__(self, headers):
        super().__init__()
        self.title = headers["title"]
        self.writer = headers["nick"]
        self.date = headers["date"]

    """Renders post header"""
    def compose(self) -> ComposeResult:
        # render
        yield PostTitleStatic(self.title)
        yield PostWriterStatic(self.writer)
        yield PostDateStatic(self.date)

class PostBodyWidget(Static):
    """Displays post body"""
    pass

## Comments ###
class CommentAreaHeaderStatic(Static):
    """Displays comment area header"""
    def __init__(self, comment_header: dict):
        super().__init__()
        self.comment_header = comment_header

    def on_mount(self) -> None:
        self.update(f"댓글 수: {self.comment_header['comment_cnt']}")

class CommentWriterStatic(Static):
    """Displays comment writer"""
    pass


class CommentMemoStatic(Static):
    """Displays comment memo"""
    pass


class CommentDateStatic(Static):
    """Displays comment date"""
    pass


class CommentItemWidget(Widget):
    """Displays comment item"""
    def __init__(self, comment):
        super().__init__()
        self.comment = comment

    def compose(self) -> ComposeResult:
        yield CommentWriterStatic(self.comment["name"])
        yield CommentMemoStatic(self.comment["memo"])
        yield CommentDateStatic(self.comment["reg_date"])
        yield SubCommentItemStatic(self.comment["subcomments"])


class SubCommentItemStatic(Static):
    """Displays subcomments"""
    def __init__(self, subcomments):
        super().__init__()
        self.subcomments = subcomments

    def compose(self) -> ComposeResult:
        for subcomment in self.subcomments:
            yield CommentWriterStatic("┗ " + subcomment["name"], classes="subCommentAreaWidget")
            yield CommentMemoStatic(subcomment["memo"], classes="subCommentAreaWidget")
            yield CommentDateStatic(subcomment["reg_date"], classes="subCommentAreaWidget")


class CommentAreaWidget(Widget):
    """Widget for comment area"""
    def __init__(self, comment_data):
        super().__init__()
        self.comment_data = comment_data

    """Renders comment area header and comments"""
    def compose(self) -> ComposeResult:
        # render
        yield CommentAreaHeaderStatic(self.comment_data["header"])
        for comment in self.comment_data["comments"].values():
            yield CommentItemWidget(comment)
