import os
import tkinter.messagebox as mbox
from threading import Thread
from tkinter import Tk, Frame, Checkbutton, BooleanVar, BOTH, Label, Button, StringVar, Entry, Text

from youtube_dl import YoutubeDL


class YdlGUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack(fill=BOTH, expand=True)
        self.parent.title("youtube-dl GUI")
        # Initialise variables
        self._extract_audio = BooleanVar()
        self._video_url = StringVar()
        # Initialise
        self._logger = LogWindow(self)
        self._init_ui()

    def _init_ui(self):
        # Label to specify video link
        lbl_video_url = Label(self, text="Video URL:")
        lbl_video_url.place(x=20, y=20)
        # Entry to enter video url
        entr_video_url = Entry(self, width=50, textvariable=self._video_url)
        entr_video_url.place(x=100, y=20)
        # Checkbutton to extract audio
        cb_extract_audio = Checkbutton(self, var=self._extract_audio, text="Only keep audio")
        cb_extract_audio.pack()
        cb_extract_audio.place(x=20, y=60)
        # Button to start downloading
        b_start_download = Button(self, text="Start download", command=self.download)
        b_start_download.place(x=20, y=90)
        # Log window to log progress
        self._logger.place(x=20, y=130)

    def start_youtube_dl(self):
        # Start downloading the specified url
        output_tmpl = os.path.dirname(os.path.abspath(__file__)) + '/%(title)s-%(id)s.%(ext)s'
        options = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'socket_timeout': '15',
            'progress_hooks': [self._logger.log],
            'ignoreerrors': True,
            'outtmpl': output_tmpl,
        }
        if self._extract_audio.get():
            options['format'] = 'bestaudio/best',
            options['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '3',
            }]
        dl = YoutubeDL(options)
        status = dl.download([self._video_url.get()])
        if status != 0:
            mbox.showerror("youtube-dl error", "An error happened whilst processing your video(s)")
        else:
            mbox.showinfo("youtube-dl finished", "Your video(s) have been successfully processed")

    def download(self):
        thr = Thread(target=self.start_youtube_dl)
        thr.start()


class LogWindow(Text):
    def __init__(self, parent):
        Text.__init__(self, parent)
        self.parent = parent

    def log(self, info):
        if '_percent_str' in info:
            progress = info['_percent_str']
        else:
            progress = '100%'
        filename = info['filename'].split(os.sep)[-1]
        self.insert('1.0', "{:s} for {:s} \n".format(progress, filename))


def main():
    root = Tk()
    root.geometry("640x480")
    app = YdlGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()