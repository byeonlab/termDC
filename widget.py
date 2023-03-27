from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Header, Footer, DataTable, Button, Static
from textual.screen import Screen

import gal
ROWS = gal.getPosts()

class postDetail(Static):
    # self __init__(self, num):
    #     self.content = ReadPost(num)

    # def compose(self) -> ComposeResult:
    #     """Create child widgets for the app."""
    #     # yield Header()
   
    #     # yield DataTable()

    def on_mount(self) -> None:
        self.focus()

    
class postReadScreen(Screen):
    BINDINGS = [("q", "quit_post_detail", "Quit")]

    def __init__(self, num):
        Screen.__init__(self)
        self.num = num 

    def compose(self) -> ComposeResult:
        yield postDetail(gal.ReadPost(self.num))
        yield Footer()

    # def on_button_pressed(self, event: Button.Pressed) -> None:
    #     if event.button.id == "quit":
    #         self.app.exit()
    #     else:
           

    def action_quit_post_detail(self) -> None:
        # self.unmount()
        self.app.pop_screen()
        # def action_toggle_dark(self) -> None:
    #     """An action to toggle dark mode."""
    #     self.dark = not self.dark

    

class termDC(App):

    # BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        # yield Header()
        # yield Footer()
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        rows = iter(ROWS)
        table.add_columns(*next(rows))
        table.add_rows(rows)
        table.focus()
    
    def on_data_table_row_selected(self, event) -> None:
        table = self.query_one(DataTable)
        # print("test")
        # self.push_screen(postReadScreen("2445356"))
        self.push_screen(postReadScreen(table.get_row_at(event.cursor_row)[0]))
    
        # table.mount(postDetail())
    # def action_toggle_dark(self) -> None:
    #     """An action to toggle dark mode."""
    #     self.dark = not self.dark

app = termDC()
if __name__ == "__main__":
 
    app.run()