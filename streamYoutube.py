import vlc, pafy, platform
import ttkbootstrap as ttk
def getYoutubeStreamLink(url):
    video = pafy.new(url)
    best = video.getbest()     # get best resolution
    return best.url

class TkVlcYoutubeStreamer():
    def __init__(self, parent, link):
        self.videoFrame = ttk.Frame(parent, width = parent.winfo_screenwidth(),
                                   height = parent.winfo_screenheight(), bootstyle="dark")

        self.controlFrame = ttk.Frame(parent)
        self.controlFrame.pack()
        self.streamBtn = ttk.Button(self.controlFrame, text = "Stream", command = lambda : self.stream(link)
                                    )
        self.closeBtn = ttk.Button(self.controlFrame, text = "Close", command= lambda: self.stop())
        self.streamBtn.grid(row=0, column=0, padx=5, pady=2)
        self.closeBtn.grid(row=0, column= 1, padx=5, pady=2)
        self.videoFrame.pack()

        # intialize vlc
        self.vlcInstance = vlc.Instance()
        self.player = self.vlcInstance.media_player_new()

    def getHandle(self):
        return self.videoFrame.winfo_id()

    def stop(self):
        self.player.stop()
        self.controlFrame.destroy()

    def stream(self, link):
        media = self.vlcInstance.media_new(link)
        media.get_mrl()
        self.player.set_media(media)

        # render in video frame
        if platform.system() == 'Windows':
            self.player.set_hwnd(self.getHandle())
        else:
            self.player.set_xwindow(self.getHandle())
        self.player.play()


if __name__ == "__main__":
    link = "https://www.youtube.com/watch?v=U3aoGDjDI2s"
    root = ttk.Window()
    root.geometry("600x600")
    videoFrame = TkVlcYoutubeStreamer(root, getYoutubeStreamLink(link))

    root.mainloop()