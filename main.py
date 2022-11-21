import tkinter as tk
from tkinter import ttk, messagebox
import database, youtubeInfoExtract

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # sql connection
        self.db = self.databaseConnection()

        # config
        self.title("Workout buddy!")
        self.geometry("600x600")
        self.protocol('WM_DELETE_WINDOW', self.close)

        # render layout
        self.feedPage()

    def feedPage(self):
        self.feedFrame = ttk.Frame(self)
        self.feedFrame.pack()

        self.vidLinkEntry = tk.Entry(self.feedFrame)
        self.vidLinkEntry.pack()
        tk.Button(self.feedFrame, text="Add video", command= lambda : self.addVideo(self.vidLinkEntry.get()) ).pack()

        self.feedHeading = ttk.Label(self.feedFrame, text="Your feeds..")
        self.feedHeading.pack()

        # card for youtube videoes
        # print(db)
        cards = []
        cardCount = -1
        for videoInfo in self.db.get_all_records():
            cardCount += 1
            cards.append(tk.Button(text = videoInfo[1], command= lambda id=videoInfo[0]: self.openVideo(f"https://youtu.be/{id}")))
            cards[cardCount].pack()

        if cardCount == -1:
            tk.Label(self.feedFrame, text="No videoes in feed !").pack()


    def openVideo(self, link):
        print(link)
        pass

    def addVideo(self):
        pass

    def databaseConnection(self):
        return database.connectToDb("workoutBuddy.db", "workouts")

    def addVideo(self, url):
        try:
            self.db.insert_record(youtubeInfoExtract.getInfo(url))
        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self)

    def close(self):
        self.db.close()
        self.destroy()

if __name__ == "__main__":
    myApp = App()
    myApp.mainloop()