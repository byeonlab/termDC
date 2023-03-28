from textual.app import App, ComposeResult
# from textual.containers import Grid
from textual.widgets import Header, Footer, DataTable, Static
from textual.screen import Screen

import libDc

class GalleryList(DataTable):
    def __init__(self):
        DataTable.__init__(self)
        self.cursor_type = "row"
        self.add_columns("Gallery")
        self.add_row("프로그래밍 갤러리", key="programming")
        self.add_row("국내야구 갤러리", key="baseball_new11")
        self.focus()

class PostHeaderWidget(Static):
    def __init__(self, content):
        Static.__init__(self)
        self.content = content

    def on_mount(self) -> None:
        self.update(self.content)

class PostBodyWidget(Static):
    def __init__(self, content):
        Static.__init__(self)
        self.content = content

    def on_mount(self) -> None:
        self.update(self.content)

class CommentAreaWidget(Static):
    def __init__(self, content):
        Static.__init__(self)
        self.content = content

    def on_mount(self) -> None:
        self.update(self.content)

class PostReadScreen(Screen):
    BINDINGS = [
        ("q", "quit_post_read", "Quit"),
        # ("r", "refresh", "Refresh")
        ]

    def __init__(self, galleryId, postNo):
        Screen.__init__(self)
        self.postNo = postNo 
        self.galleryId = galleryId
        self.postResponse = libDc.GetPost(galleryId, postNo)

    def compose(self) -> ComposeResult:
        yield PostHeaderWidget(libDc.ParsePostHeader(self.postResponse.text))
        yield PostBodyWidget(libDc.ParsePostBody(self.postResponse.text))
        yield CommentAreaWidget(libDc.GetComment(self.postResponse.text))
        yield Footer()

    def action_quit_post_read(self) -> None:
        self.app.pop_screen()
        self.compose()
        
class PostList(DataTable):
    def __init__(self, galleryId):
        DataTable.__init__(self)

        rows = iter(libDc.getPosts(galleryId=galleryId))

        self.cursor_type = "row"
        self.add_columns("No", "Writer", "Title")
        self.add_rows(rows)
    

class PostListScreen(Screen):
    BINDINGS = [("q", "quit_post_list", "Quit")]

    def __init__(self, galleryId):
        Screen.__init__(self)
        self.galleryId = galleryId 

    def compose(self) -> ComposeResult:
        yield PostList(self.galleryId)
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(PostList)
        table.focus()

    def action_quit_post_list(self) -> None:
        self.app.pop_screen()

    def on_data_table_row_selected(self, event) -> None:
        table = self.query_one(PostList)
        postNo = table.get_row_at(event.cursor_row)[0]
        self.app.push_screen(PostReadScreen(self.galleryId, postNo))
    

class termDC(App):
    CSS_PATH = "CommentArea.css"
    def compose(self) -> ComposeResult:
        yield Header()
        yield GalleryList()

    def on_mount(self) -> None:
        table = self.query_one(GalleryList)
        table.focus()
    
    def on_data_table_row_selected(self, event) -> None:
        GalleryId = event.row_key.value
        self.app.push_screen(PostListScreen(GalleryId))
