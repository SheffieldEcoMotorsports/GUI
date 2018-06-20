# importing tkinter
import tkinter as tk
from tkinter import ttk
from random import random
# import all the matplotlib stuff we need
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

class Queue:
    def __init__(self):
        self.items = []

    # adds data at start of queue
    def enqueue(self, item):
        self.items.insert(0, item)

    # removes data from beginning of queue
    def dequeue(self):
        return self.items.pop()

    # returns size of queue
    def size(self):
        return len(self.items)

style.use("ggplot")

# a font we'll be using
LARGE_FONT = ("Verdana", 12)
LARGER_FONT = ("Verdana", 16)

# number of data points that can be viewed at a time on each graph
VIEW_LIMIT = 100

#Base page layout. Other pages can be built from this
class Page(tk.Frame):
    def __init__(self, parent, controller, pageName):
        tk.Frame.__init__(self, parent, background="white")
        self.controller = controller
        self.parent = parent
        self.pageName = pageName
        
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        
        # frame to contain the header elements of each page
        self.header = tk.Frame(self)
        self.header.grid(column=0, row=0, columnspan=5, sticky="NSEW")
        self.header.rowconfigure(0, weight=1)
        
        # Page heading
        self.heading = tk.Label(self.header, text=pageName, font=LARGER_FONT)
        self.heading.grid(column=0, row=0)
        
        self.buttonsFrame = tk.Frame(self.header, background="white")
        self.buttonsFrame.grid(column=1, row=0)
        
    #adds buttons along the header leading to the other pages
    def getOtherPages(self, controller, header, otherPagesDict):
        # list to store the buttons leading to other pages
        self.otherPagesButtons = []
        self.keys = {}
        count = 0

        for key in otherPagesDict:
            self.keys[otherPagesDict[key].pageName] = key
            self.otherPagesButtons.append(ttk.Button(self.buttonsFrame, text=otherPagesDict[key].pageName,
                                                     command=lambda i=key: controller.show_frame(i)))
            self.otherPagesButtons[count].grid(column=count, row=0, sticky="NSEW")
            count += 1

class GraphPage(Page):
    def __init__(self, parent, controller, pageName, graphCount):
        Page.__init__(self, parent, controller, pageName)
        self.graphCount = graphCount
        
        # List to store the running average
        # Each item in the list is another list
        # Index 1 is the running average itself
        # Index 2 is the StringVar() to update the tkinter label with
        self.avgs = []
        for i in range(self.graphCount):
            self.avgs.append([0, tk.StringVar()])
        
        #Adds a frame to contain labels for the names of each graph
        graphNamesFrame = tk.Frame(self, background="white")
        graphNamesFrame.grid(column=1, row=1, sticky="NSEW")
        
        # Stores the labels showing the graph names in a list and configures them
        self.graphNames = []
        for i in range(self.graphCount):
            graphNamesFrame.rowconfigure(i+1, weight=5)
            self.graphNames.append(ttk.Label(graphNamesFrame, text="Example {}".format(i+1),
                                            font=LARGE_FONT, background="white"))
            self.graphNames[i].grid(column=0, row=i+1, sticky="NSEW")
        
        graphNamesFrame.rowconfigure(0, weight=2)
        graphNamesFrame.rowconfigure(len(self.avgs)+1, weight=2)
        
        # Adds a frame to contain the label for the running averages of each graph
        averages = tk.Frame(self, background="white")
        averages.grid(column=3, row=1, sticky="NSEW")
        
        #Configure column sizes
        self.columnconfigure(0, weight=1) 
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=25)  
        self.columnconfigure(3, weight=2)   
        self.columnconfigure(4, weight=1)
        
        self.rowconfigure(1, weight=1)
        
        #Adds some frames above and below the column showing the averages, so that they align with the graphs
        averages.rowconfigure(0, weight=2)
        averages.rowconfigure(len(self.avgs)+1, weight=2)
        
        # Stores the labels showing the running averages in a list and configures them
        self.avgLabels = []
        for i in range(self.graphCount):
            averages.rowconfigure(i+1, weight=5)
            self.avgLabels.append(ttk.Label(averages, textvariable=self.avgs[i][1],
                                            font=LARGE_FONT, background="white"))
            self.avgLabels[i].grid(column=0, row=i+1, sticky="NSEW")
        
        # create the matplotlib figure
        self.f = Figure(figsize=(5, 4), dpi=100)
        
        # add plots and store them in a list.
        self.plots = []
        for i in range(self.graphCount):
            arrangement = self.graphCount * 100 + 11 + i
            self.plots.append(self.f.add_subplot(arrangement))
            self.plots[i].set(xlabel="Time")
            
        # List to store Queues for the data for each graph
        # Each item in the list is another list
        # Index 0 in that list is the x data
        # Index 1 is the y data
        self.data = []
        for i in range(self.graphCount):
            self.data.append([Queue(), Queue()])
            
        # Displays graph
        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.get_tk_widget().grid(column=2, row=1, sticky="nesw")
        self.canvas._tkcanvas.grid(column=2, row=1, sticky="nesw")

        # animates graph
        self.ani = animation.FuncAnimation(self.f, self.animate, interval=500)
    
    # will animate a subplot given correct axes, the name of a file to write to, and queues to store data in
    def subAnimation(self, x, axes, file, x_queue, y_queue, avg):
        # opens file in append mode
        with open(file, "a") as file:
            # gets random piece of data
            data = random() * 150

            avg = avg + ((data - avg) / (x + 1))

            # writes data to file in correct format
            file.write(str(x) + "," + str(data) + "\n")
            # enqueues data to queues
            x_queue.enqueue(x)
            y_queue.enqueue(round(data))
            # if the queue gets larger than 50, then we can start dequeueing data
            if x_queue.size() == VIEW_LIMIT:
                x_queue.dequeue()
                # makes graph scroll along so only 50 pieces of data are shown at a time
                axes.set_xlim(x - VIEW_LIMIT, x)
            if y_queue.size() == VIEW_LIMIT:
                y_queue.dequeue()
            # plots data
            axes.clear()
            axes.plot(x_queue.items, y_queue.items, color="red")
            return avg

    # animates all subplots
    def animate(self, x):
        for i in range(self.graphCount):
            self.avgs[i][0] = self.subAnimation(x, self.plots[i], "data{}.txt".format(i), self.data[i][0], self.data[i][1], self.avgs[i][0])
            self.avgs[i][1].set( str(round(self.avgs[i][0], 2)) )