import vlc, pafy, time, platform
import tkinter as tk

def getYoutubeStreamLink(url):
    video = pafy.new(url)
    print(video)
    best = video.getbest()     # get best resolution
    return best.url

class TkVlcYoutubeStreamer():
    def __init__(self, parent, link):
        self.videoFrame = tk.Frame(parent, width = parent.winfo_screenwidth(),
                                   height = parent.winfo_screenheight(), bg="black")

        self.controlFrame = tk.Frame(parent)
        self.controlFrame.pack()
        self.streamBtn = tk.Button(self.controlFrame, text = "Stream", command = lambda : self.stream(link))
        self.closeBtn = tk.Button(self.controlFrame, text = "Close", command= lambda: self.stop())
        self.streamBtn.grid(row=0, column=0)
        self.closeBtn.grid(row=0, column= 1)
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
        # time.sleep(50)


if __name__ == "__main__":
    link = "https://www.youtube.com/watch?v=He7-vOs_YPQ"
    root = tk.Tk()
    root.geometry("600x600")
    videoFrame = TkVlcYoutubeStreamer(root, getYoutubeStreamLink(link))

    root.mainloop()