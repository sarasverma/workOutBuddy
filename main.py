import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import database, youtubeInfoExtract, streamYoutube

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # sql connection
        self.db = self.databaseConnection()

        # config
        self.title("Workout buddy!")
        self.geometry("600x600")
        self.protocol('WM_DELETE_WINDOW', self.close)

        # different sections
        self.tabControl = ttk.Notebook(self)
        self.tabControl.pack(expand=1, fill='both')

        self.scroll = tk.Scrollbar(self)
        self.scroll.pack(side= tk.RIGHT, fill= tk.Y)


        # render layout
        self.feedPage()
        self.statsPage()
        self.poseCorrectionPage()

        self.tabControl.add(self.feedFrame, text= "Feed")
        self.tabControl.add(self.statFrame, text= "Statistic")
        self.tabControl.add(self.poseCorrectionFrame, text= "Pose correction")

    def feedPage(self):
        self.feedFrame = ttk.Frame(self.tabControl)
        self.feedFrame.pack()

        self.vidLinkEntry = tk.Entry(self.feedFrame, width=self.winfo_width()*50)
        self.vidLinkEntry.pack()
        tk.Button(self.feedFrame, text="Add video", command= lambda : self.addVideo(self.vidLinkEntry.get())
                  ,bg="red", fg="white").pack()

        self.feedHeading = ttk.Label(self.feedFrame, text="Your feeds..")
        self.feedHeading.pack()

        self.feedVideoFrame = tk.Frame(self.feedFrame)
        self.feedVideoFrame.pack(side= tk.LEFT)
        # card for youtube videoes
        self.cards = []
        self.imgs = []
        self.cardCount = -1
        for videoInfo in self.db.get_all_records():
            self.cardCount += 1
            self.imgs.append(ImageTk.PhotoImage(Image.open(fr"img/{videoInfo[0]}.png").resize(
                (self.winfo_width() *100, self.winfo_width()*100))))
            self.cards.append(tk.Button(self.feedVideoFrame, text = videoInfo[1],
                                        command= lambda id=videoInfo[0]: self.openVideo(f"https://youtu.be/{id}")
                                        ,image= self.imgs[self.cardCount]))
            self.cards[self.cardCount].pack()

        if self.cardCount == -1:
            tk.Label(self.feedVideoFrame, text="No videoes in feed !").pack()

    def statsPage(self):
        self.statFrame = tk.Frame(self.tabControl)
        self.statFrame.pack()

    def poseCorrectionPage(self):
        self.poseCorrectionFrame = tk.Frame(self.tabControl)
        self.poseCorrectionFrame.pack()

    def openVideo(self, link):
        self.videoPlayerFrame = tk.Frame(self.feedFrame)
        videoFrame = streamYoutube.TkVlcYoutubeStreamer(self.videoPlayerFrame, streamYoutube.getYoutubeStreamLink(link))
        self.videoPlayerFrame.pack(side= tk.RIGHT)
        pass

    def databaseConnection(self):
        return database.connectToDb("workoutBuddy.db", "workouts")

    def addVideo(self, url):
        try:
            videoInfo = youtubeInfoExtract.getInfo(url)
            self.db.insert_record(videoInfo)
            self.cardCount += 1
            self.imgs.append(ImageTk.PhotoImage(ImageTk.PhotoImage(Image.open(fr"img/{videoInfo['id'][1:-1]}.png").resize(
                (self.winfo_width() *100, self.winfo_width()*100)))))
            self.cards.append(tk.Button(self.feedVideoFrame, text= videoInfo['title'],
                                        command=lambda : self.openVideo(f"https://youtu.be/{videoInfo['id']}")
                                        , image= self.imgs[self.cardCount]))
            self.cards[self.cardCount].pack()

        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self)

    def close(self):
        self.db.close()
        self.destroy()

if __name__ == "__main__":
    myApp = App()
    myApp.mainloop()