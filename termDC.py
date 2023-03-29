from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.screen import Screen

from LibTermDc.widgets import GalleryList, PostList, PostHeaderWidget, PostBodyWidget, CommentAreaWidget
from DCsdk import libDc

class PostReadScreen(Screen):
    BINDINGS = [
        ("q", "quit_post_read", "Quit"),
    ]

    def __init__(self, galleryId, postNo):
        Screen.__init__(self)
        # self.postNo = postNo 
        # self.galleryId = galleryId
        self.html = libDc.GetPost(galleryId, postNo).text
        self.commentData = libDc.GetComment(self.html)

    def compose(self) -> ComposeResult:
        yield PostHeaderWidget(libDc.ParsePostHeader(self.html))
        yield PostBodyWidget(libDc.ParsePostBody(self.html))
        if self.commentData["comments"] != []:
            yield CommentAreaWidget(self.commentData["comments"])
        yield Footer()

    def action_quit_post_read(self) -> None:
        self.app.pop_screen()
        self.compose()
        
class PostListScreen(Screen):
    BINDINGS = [("q", "quit_post_list", "Quit")]

    def __init__(self, galleryId):
        Screen.__init__(self)
        self.galleryId = galleryId 

    def compose(self) -> ComposeResult:
        yield PostList()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(PostList)
        rows = iter(libDc.getPosts(self.galleryId))

        table.add_rows(rows)
        table.focus()

    def action_quit_post_list(self) -> None:
        self.app.pop_screen()

    def on_data_table_row_selected(self, event) -> None:
        table = self.query_one(PostList)
        postNo = table.get_row_at(event.cursor_row)[0]
        self.app.push_screen(PostReadScreen(self.galleryId, postNo))
    

class termDC(App):
    CSS_PATH = "termDC.css"
    def compose(self) -> ComposeResult:
        yield Header()
        yield GalleryList()

    def on_mount(self) -> None:
        table = self.query_one(GalleryList)
        table.add_row("프로그래밍 갤러리", key="programming")
        table.add_row("식물 갤러리", key="tree")
        table.focus()
    
    def on_data_table_row_selected(self, event) -> None:
        GalleryId = event.row_key.value
        self.app.push_screen(PostListScreen(GalleryId))
