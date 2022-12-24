import ttkbootstrap as ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import database, youtubeInfoExtract, streamYoutube, stats

class App(ttk.Window):
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

        # add video
        self.feedAddVideoFrame = ttk.Frame(self.feedFrame)
        self.feedAddVideoFrame.pack()
        self.vidLinkEntry = ttk.Entry(self.feedAddVideoFrame, width = 50)
        self.vidLinkEntry.pack(side="left")
        ttk.Button(self.feedAddVideoFrame, text="Add video", bootstyle= "danger"
                ,command= lambda : self.addVideo(self.vidLinkEntry.get())).pack(side= "right", padx= 2)
        self.feedHeading = ttk.Label(self.feedFrame, text="Your feeds..")
        self.feedHeading.pack()

        # video feed
        # canvas for scroll bar
        self.feedVideoCanvas = ttk.Canvas(self.feedFrame)
        self.feedVideoCanvas.pack(side= "left", fill="both", expand="yes")

        self.feedVideoFrame = ttk.Frame(self.feedVideoCanvas)
        self.feedVideoCanvas.create_window((0, 0), window= self.feedVideoFrame)

        # scroll bar
        self.scrollBar = ttk.Scrollbar(self.feedFrame, orient='vertical', command= self.feedVideoCanvas.yview)
        self.scrollBar.pack(side='right', fill='y')
        self.feedVideoCanvas.configure(yscrollcommand = self.scrollBar.set)
        self.feedVideoCanvas.bind('<Configure>', lambda e: self.feedVideoCanvas.configure(scrollregion = self.feedVideoCanvas.bbox('all')))

        # card for youtube videoes
        self.cards = []
        self.imgs = []
        self.cardCount = -1
        for videoInfo in self.db.get_all_records():
            self.cardCount += 1
            self.imgs.append(ImageTk.PhotoImage(Image.open(fr"img/{videoInfo[0]}.png").resize(
                (600, 400))))
            self.cards.append(ttk.Button(self.feedVideoFrame, text = videoInfo[1],
                                        command= lambda id=videoInfo[0]: self.openVideo(f"https://youtu.be/{id}")
                                        ,image= self.imgs[self.cardCount], bootstyle="light"))
            self.cards[self.cardCount].pack(pady= 4)

        # no video available
        if self.cardCount == -1:
            ttk.Label(self.feedVideoFrame, text="No videoes in feed !").pack()

    def statsPage(self):
        self.statFrame = ttk.Frame(self.tabControl)
        self.statFrame.pack()

        # adding stat stuff
        stats.Stats(self.statFrame)

    def poseCorrectionPage(self):
        self.poseCorrectionFrame = ttk.Frame(self.tabControl)
        self.poseCorrectionFrame.pack()

    def openVideo(self, link):
        self.videoPlayerFrame = ttk.Frame(self.feedFrame)
        videoFrame = streamYoutube.TkVlcYoutubeStreamer(self.videoPlayerFrame, streamYoutube.getYoutubeStreamLink(link))
        self.videoPlayerFrame.pack()

    def databaseConnection(self):
        return database.connectToDb("workoutBuddy.db", "workouts")

    def addVideo(self, url):
        try:
            videoInfo = youtubeInfoExtract.getInfo(url)
            self.db.insert_record(videoInfo)
            self.cardCount += 1
            self.imgs.append(ImageTk.PhotoImage(Image.open(fr"img/{videoInfo['id'][1:-1]}.png").resize(
                (600, 400))))
            self.cards.append(ttk.Button(self.feedVideoFrame, text= videoInfo['title'],
                                        command=lambda : self.openVideo(f"https://youtu.be/{videoInfo['id']}")
                                        , image= self.imgs[self.cardCount], bootstyle  ="light"))
            self.cards[self.cardCount].pack()

        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self)

    def close(self):
        self.db.close()
        self.destroy()

if __name__ == "__main__":
    myApp = App()
    myApp.mainloop()