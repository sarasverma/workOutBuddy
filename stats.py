import ttkbootstrap as ttk
from tkinter import messagebox
import database
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from datetime import date

class Stats:
    def __init__(self, parent):
        self.parent = parent
        self.db = self.connectToDatabase()

        # add calorie frame
        self.addCalorieFrame = ttk.Frame(parent)
        self.addCalorieFrame.pack()
        self.addCalorieEntry = ttk.Entry(self.addCalorieFrame)
        self.addCalorieEntry.pack(side="left")
        ttk.Button(self.addCalorieFrame, text="Add Calorie", bootstyle="success", command= lambda : self.addCalories()).pack(side="right", padx=2, pady=2)

        ttk.Label(parent, text="Your statistics !", font= ('Helvetica bold', 26)).pack()

        # graph
        self.graphFrame = ttk.Frame(parent)
        self.graphFrame.pack()

        self.label = []
        self.data = []
        for record in self.db.get_all_records():
            self.label.append(record[0])
            self.data.append(record[1])

        # for blank data
        if self.label == []:
            ttk.Label(self.graphFrame, text ="Start exercising to get data for analysis !").pack()
        else:
            self.plot()

    def connectToDatabase(self):
        return database.connectToDb('workoutBuddy.db', 'calories')

    def addCalories(self):
        if self.addCalorieEntry.get().isdigit():
            try:
                self.db.insert_record({"calories_burnt": self.addCalorieEntry.get()})
                self.update(self.addCalorieEntry.get())
            except Exception as err:
                # handle same day request
                if "UNIQUE" in str(err):
                    todayDate = date.today()
                    currentVal = self.db.get_record('date', todayDate)[0][1]
                    self.db.update_record('date', todayDate, 'calories_burnt', currentVal + int(self.addCalorieEntry.get()))
                    self.update(currentVal + int(self.addCalorieEntry.get()))
        else:
            messagebox.showerror("Error", "Calories burnt should be integer value only !", parent=self.graphFrame)

    def plot(self):
        self.fig = Figure(figsize= (5, 5), dpi= 100)
        self.graph = self.fig.add_subplot(111)
        self.bars = self.graph.bar(self.label, self.data, 0.5)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand= 1)

        # for navigation of plot
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graphFrame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    def update(self, value):
        # destroy previous graph
        self.graphFrame.destroy()

        self.graphFrame = ttk.Frame(self.parent)
        self.graphFrame.pack()
        self.label.append(str(date.today()))
        self.data.append(value)
        # re render
        self.plot()

if __name__ == '__main__':
    root = ttk.Window()
    root.title("Embedding in Tk")
    root.geometry('600x600')

    mystats = Stats(root)

    root.mainloop()
