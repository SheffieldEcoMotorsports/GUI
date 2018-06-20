from pages import Page, GraphPage
import tkinter as tk

# Main backend of the GUI
# controls which page is shown
class semDataApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        # initialises inherited class
        tk.Tk.__init__(self, *args, **kwargs)

        # creates main container of the gui
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # dictionary to store frames in
        self.frames = {}
        
        #Make sure to add any new pages here
        self.pagesList = [Page1, Page2, Page3, Page4]
        
        # stores each page into the dictionary above
        for page in self.pagesList:
            frame = page(container, self)  # each page is an object
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        for page in self.frames:
            self.frames[page].getOtherPages(self.frames[page].controller, self.frames[page].header, self.frames)

        self.show_frame(Page1)

    # shows a frame by raising it to the top
    def show_frame(self, cont):
        self.frames[cont]
        frame = self.frames[cont]
        frame.tkraise()

# Page 1 of the GUI
class Page1(GraphPage):
    def __init__(self, parent, controller):
        GraphPage.__init__(self, parent, controller, "Page 1", 4)

# Page 2 of the GUI
class Page2(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller, "Page 2")

# Page 3 of the GUI
class Page3(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller, "Page 3")
        

# Page 4 of the GUI
class Page4(GraphPage):
    def __init__(self, parent, controller):
        GraphPage.__init__(self, parent, controller, "Page 4", 2)

        
app = semDataApp()
app.geometry("1920x1080")

app.mainloop()