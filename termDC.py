import pkg_resources
pkg_resources.require("textual==0.17.0")

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.screen import Screen

from LibTermDc.widgets import GalleryList, PostList, PostHeaderWidget, PostBodyWidget, CommentAreaWidget
from dcsdk.libdc import Gallery, Post

class PostReadScreen(Screen):
    BINDINGS = [
        ("q", "quit_post_read", "Quit"),
    ]

    def __init__(self, gallery_id, post_no):
        Screen.__init__(self)
        self.Post = Post(gallery_id, post_no)

    def compose(self) -> ComposeResult:
        yield PostHeaderWidget(self.Post.headers())
        yield PostBodyWidget(self.Post.body())
        yield CommentAreaWidget(self.Post.comments())
        yield Footer()

    def action_quit_post_read(self) -> None:
        self.app.pop_screen()
        self.compose()
        
class PostListScreen(Screen):
    BINDINGS = [
        ("q", "quit_post_list", "Quit"),
        ("n", "next_page", "Next Page"),
        ("p", "prev_page", "Previous Page"),
        ("r", "refresh", "Refresh"),
    ]

    def __init__(self, gallery_id):
        Screen.__init__(self)
        self.Gallery = Gallery(gallery_id, 1)

    def compose(self) -> ComposeResult:
        yield PostList()
        yield Footer()

    def on_mount(self) -> None:
        self.populate_list()
        self.query_one(PostList).focus()

    def on_data_table_row_selected(self, event) -> None:
        table = self.query_one(PostList)
        post_no = table.get_row_at(event.cursor_row)[0]
        self.app.push_screen(PostReadScreen(self.Gallery.id, post_no))

    def action_quit_post_list(self) -> None:
        self.app.pop_screen()

    def action_next_page(self) -> None:
        self.Gallery.increment_page()
        self.populate_list()

    def action_prev_page(self) -> None:
        self.Gallery.decrement_page()
        self.populate_list()

    def action_refresh(self) -> None:
        self.populate_list()

    def populate_list(self):
        rows = iter(self.Gallery.posts())
        table = self.query_one(PostList)
        table.clear()
        table.add_rows(rows)        

class IndexScreen(Screen):
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

class termDC(App):
    CSS_PATH = "termDC.css"

    def on_mount(self) -> None:
        self.push_screen(IndexScreen())

