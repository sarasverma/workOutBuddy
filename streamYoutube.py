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

        # self.streamBtn = tk.Button(parent, text = "Stream", command = lambda : self.stream(link))
        # self.closeBtn = tk.Button(parent, text = "Close", command= lambda: self.close())
        # self.streamBtn.pack()
        # self.closeBtn.pack()
        self.videoFrame.pack()

        # overriding parent close functionality
        parent.protocol("WM_DELETE_WINDOW", lambda : self.close(parent))

        # intialize vlc
        self.vlcInstance = vlc.Instance()
        self.player = self.vlcInstance.media_player_new()
        self.stream(link)

    def getHandle(self):
        return self.videoFrame.winfo_id()

    def close(self, parent):
        self.player.stop()
        parent.destroy()


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