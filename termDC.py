# Built-in libraries
import json
import pkg_resources
pkg_resources.require("textual==0.19.0")

# Textual libraries
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, Input, Button
from textual.containers import Grid, Vertical
from textual.screen import Screen, ModalScreen
from textual.binding import Binding

# termDC libraries
from libtermdc.widgets import GalleryList, PostListHeader, PostList, PostHeaderWidget, PostBodyWidget, CommentAreaWidget
from dcsdk.libdc import Gallery, MinorGallery, Post, MinorPost

class GoPageModalScreen(ModalScreen):
    """ModalScreen for page number input"""

    def compose(self) -> ComposeResult:
        yield Grid(
            Input(placeholder="Page Number", id="question"),
            Button("OK", id="ok"),Button("Cancel", id="cancel"),
            id="dialog"
        )
        yield Footer()
    
    """Focus input field"""
    def on_mount(self) -> None:
        self.query_one(Input).focus()

    """Button actions"""
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            new_page = int(self.query_one(Input).value)
            parent_screen = self.app.screen_stack[-2]
            parent_screen.gallery.set_page(new_page)
            parent_screen.post_list_header.update_page(new_page)
            parent_screen.populate_list()
            self.app.pop_screen()

        elif event.button.id == "cancel":
            self.app.pop_screen()

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
        ("g", "go_page", "Go Page"),
        ("r", "refresh", "Refresh"),
    ]

    """Screen that displays posts of gallery with a given gallery metadata"""
    def __init__(self, gallery_name: str, gallery_id: str, gallery_type: str):
        super().__init__()
        if gallery_type == "major":
            self.gallery = Gallery(gallery_id)
        if gallery_type == "minor":
            self.gallery = MinorGallery(gallery_id)

        self.post_list_header = PostListHeader(gallery_name=gallery_name)   
        self.post_list = PostList()

    """Renders table for post list and app footer"""
    def compose(self) -> ComposeResult:
        yield (
            Vertical(
                self.post_list_header,
                self.post_list,
                id="post_list_container"
            )
        )
        yield Footer()

    """Populates table for post list with actual posts"""
    def on_mount(self) -> None:
        self.populate_list()
        self.post_list_header.update_page()
        self.post_list.focus()

    """Pushes PostReadScreen with given gallery id and post number when a row is selected"""
    def on_data_table_row_selected(self, event) -> None:
        post_no = self.post_list.get_row_at(event.cursor_row)[0]
        self.app.push_screen(PostReadScreen(self.gallery.id, self.gallery.TYPE, post_no))

    """Pops itself on 'q' input"""
    def action_quit_post_list(self) -> None:
        self.app.pop_screen()

    """Goes to the next page of post list"""
    def action_next_page(self) -> None:
        self.gallery.increment_page()
        self.populate_list()
        self.post_list_header.update_page(self.gallery.page)

    """Goes to the previous page of post list"""
    def action_prev_page(self) -> None:
        self.gallery.decrement_page()
        self.populate_list()
        self.post_list_header.update_page(self.gallery.page)

    """Refreshes current page of post list"""
    def action_refresh(self) -> None:
        self.populate_list()

    """Populates post list with current page"""
    def populate_list(self) -> None:
        rows = iter(self.gallery.posts())
        self.post_list.clear()
        self.post_list.add_rows(rows)        

    """Go to the page of input number"""
    def action_go_page(self) -> None:
        self.app.push_screen(GoPageModalScreen())

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
        gallery_name = row_data[0]
        gallery_type = row_data[1]
        self.app.push_screen(PostListScreen(gallery_name, gallery_id, gallery_type))

class termDC(App):
    CSS_PATH = "termDC.css"

    """Pushes GalleryListScreen on application startup"""
    def on_mount(self) -> None:
        with open("data.json") as data_file:
            data = json.load(data_file)
        galleries = data["galleries"]

        self.push_screen(GalleryListScreen(galleries))

if __name__ == "__main__":
    app = termDC()
    app.run()