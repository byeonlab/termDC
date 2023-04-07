# Built-in libraries
import json
import pkg_resources
pkg_resources.require("textual==0.17.0")

# Textual libraries
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.screen import Screen

# termDC libraries
from libtermdc.widgets import GalleryList, PostList, PostHeaderWidget, PostBodyWidget, CommentAreaWidget
from dcsdk.libdc import Gallery, MinorGallery, Post, MinorPost

class PostReadScreen(Screen):
    BINDINGS = [
        ("q", "quit_post_read", "Quit"),
    ]

    """Screen that displays details of post with given gallery id and post number"""
    def __init__(self, gallery_id: str, gallery_type: str, post_no: str):
        super().__init__()
        if gallery_type == "major":
            self.post = Post(gallery_id, post_no)
        if gallery_type == "minor":
            self.post = MinorPost(gallery_id, post_no)

    """Renders details of post and app footer"""
    def compose(self) -> ComposeResult:
        yield PostHeaderWidget(self.post.headers())
        yield PostBodyWidget(self.post.body())
        yield CommentAreaWidget(self.post.comments())
        yield Footer()

    """Pops itself on 'q' input"""
    def action_quit_post_read(self) -> None:
        self.app.pop_screen()
        
class PostListScreen(Screen):
    BINDINGS = [
        ("q", "quit_post_list", "Quit"),
        ("n", "next_page", "Next Page"),
        ("p", "prev_page", "Previous Page"),
        ("r", "refresh", "Refresh"),
    ]

    """Screen that displays posts of gallery with a given gallery metadata"""
    def __init__(self, gallery_id: str, gallery_type: str):
        super().__init__()
        if gallery_type == "major":
            self.gallery = Gallery(gallery_id)
        if gallery_type == "minor":
            self.gallery = MinorGallery(gallery_id)

    """Renders table for post list and app footer"""
    def compose(self) -> ComposeResult:
        yield PostList()
        yield Footer()

    """Populates table for post list with actual posts"""
    def on_mount(self) -> None:
        self.__populate_list()
        self.query_one(PostList).focus()

    """Pushes PostReadScreen with given gallery id and post number when a row is selected"""
    def on_data_table_row_selected(self, event) -> None:
        table = self.query_one(PostList)
        post_no = table.get_row_at(event.cursor_row)[0]
        self.app.push_screen(PostReadScreen(self.gallery.id, self.gallery.TYPE, post_no))

    """Pops itself on 'q' input"""
    def action_quit_post_list(self) -> None:
        self.app.pop_screen()

    """Goes to the next page of post list"""
    def action_next_page(self) -> None:
        self.gallery.increment_page()
        self.__populate_list()

    """Goes to the previous page of post list"""
    def action_prev_page(self) -> None:
        self.gallery.decrement_page()
        self.__populate_list()

    """Refreshes current page of post list"""
    def action_refresh(self) -> None:
        self.__populate_list()

    """(Private) Populates post list with current page"""
    def __populate_list(self) -> None:
        rows = iter(self.gallery.posts())
        table = self.query_one(PostList)
        table.clear()
        table.add_rows(rows)        

class GalleryListScreen(Screen):
    """Index screen that displays gallery list"""
    def __init__(self, galleries: list):
        super().__init__()
        self.galleries = galleries

    """Renders app header and gallery list"""
    def compose(self) -> ComposeResult:
        yield Header()
        yield GalleryList()

    """Populates gallery list"""
    def on_mount(self) -> None:
        table = self.query_one(GalleryList)
        for gallery in self.galleries:
            table.add_row(gallery["name"], gallery["type"], key=gallery["id"])
        table.focus()

    """Push PostListScreen with given gallery id when row is selected"""
    def on_data_table_row_selected(self, event) -> None:
        gallery_id = event.row_key.value
        row_data = self.query_one(GalleryList).get_row(gallery_id)
        gallery_type = row_data[1]

        self.app.push_screen(PostListScreen(gallery_id, gallery_type))

class termDC(App):
    CSS_PATH = "termDC.css"

    """Pushes GalleryListScreen on application startup"""
    def on_mount(self) -> None:
        with open("data.json") as data_file:
            data = json.load(data_file)
        galleries = data["galleries"]
        self.push_screen(GalleryListScreen(galleries))

