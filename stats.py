import tkinter as tk
import database
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class Stats:
    def __init__(self, parent):
        self.parent = parent
        self.db = self.connectToDatabase()
        tk.Label(self.parent, text="Your statistics !").pack()
        self.label = []
        self.data = []
        for record in self.db.get_all_records():
            self.label.append(record[0])
            self.data.append(record[1])

        # for blank data
        if self.label == []:
            tk.Label(self.parent, text ="Start exercising to get data for analysis !").pack()
        else:
            self.plot()


    def connectToDatabase(self):
        return database.connectToDb('workoutBuddy.db', 'calories')

    def plot(self):
        self.fig = Figure(figsize= (5, 5), dpi= 100)
        self.graph = self.fig.add_subplot(111)
        self.graph.bar(self.label, self.data, 0.5)

        self.canvas = FigureCanvasTkAgg(self.fig,master=self.parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side= tk.TOP, fill= tk.BOTH, expand= 1)

        # for navigation of plot
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.parent)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side= tk.TOP, fill= tk.BOTH, expand=1)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Embedding in Tk")
    root.geometry('600x600')

    mystats = Stats(root)

    root.mainloop()
