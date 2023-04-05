import pkg_resources
pkg_resources.require("textual==0.17.0")

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.screen import Screen

from libtermdc.widgets import GalleryList, PostList, PostHeaderWidget, PostBodyWidget, CommentAreaWidget
from dcsdk.libdc import Gallery, Post

class PostReadScreen(Screen):
    BINDINGS = [
        ("q", "quit_post_read", "Quit"),
    ]

    def __init__(self, gallery_id, post_no):
        super().__init__()
        self.post = Post(gallery_id, post_no)

    def compose(self) -> ComposeResult:
        yield PostHeaderWidget(self.post.headers())
        yield PostBodyWidget(self.post.body())
        yield CommentAreaWidget(self.post.comments())
        yield Footer()

    def action_quit_post_read(self) -> None:
        self.app.pop_screen()
        
class PostListScreen(Screen):
    BINDINGS = [
        ("q", "quit_post_list", "Quit"),
        ("n", "next_page", "Next Page"),
        ("p", "prev_page", "Previous Page"),
        ("r", "refresh", "Refresh"),
    ]

    def __init__(self, gallery_id):
        super().__init__()
        self.gallery = Gallery(gallery_id)

    def compose(self) -> ComposeResult:
        yield PostList()
        yield Footer()

    def on_mount(self) -> None:
        self.populate_list()
        self.query_one(PostList).focus()

    def on_data_table_row_selected(self, event) -> None:
        table = self.query_one(PostList)
        post_no = table.get_row_at(event.cursor_row)[0]
        self.app.push_screen(PostReadScreen(self.gallery.id, post_no))

    def action_quit_post_list(self) -> None:
        self.app.pop_screen()

    def action_next_page(self) -> None:
        self.gallery.increment_page()
        self.populate_list()

    def action_prev_page(self) -> None:
        self.gallery.decrement_page()
        self.populate_list()

    def action_refresh(self) -> None:
        self.populate_list()

    def populate_list(self):
        rows = iter(self.gallery.posts())
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
        gallery_id = event.row_key.value
        self.app.push_screen(PostListScreen(gallery_id))

class termDC(App):
    CSS_PATH = "termDC.css"

    def on_mount(self) -> None:
        self.push_screen(IndexScreen())

