#!/usr/bin/env python

# author: Bartlomiej "furas" Burek (https://blog.furas.pl)
# date: 2021.01.26

import PIL.ImageTk
import tkinter
import tkinter.filedialog
from videocapture import VideoCapture


"""TODO: add docstring"""


class tkSourceSelect(tkinter.Toplevel):

    def __init__(self, parent, other_sources=None):
        """TODO: add docstring"""

        super().__init__(parent)

        self.other_sources = other_sources

        # default values at start
        self.item = None
        self.name = None
        self.source = None

        # GUI
        button = tkinter.Button(self, text="Open file...", command=self.on_select_file)
        button.pack(fill='both', expand=True)

        if self.other_sources:
            tkinter.Label(self, text="Other Sources:").pack(fill='both', expand=True)

            for item in self.other_sources:
                text, source = item
                button = tkinter.Button(self, text=text, command=lambda data=item:self.on_select_other(data))
                button.pack(fill='both', expand=True)

    def on_select_file(self):
        """TODO: add docstring"""

        result = tkinter.filedialog.askopenfilename(
                                        initialdir=".",
                                        title="Select video file",
                                        filetypes=(("AVI files", "*.avi"), ("MP4 files","*.mp4"), ("all files","*.*"))
                                    )

        if result:
            self.item = item
            self.name = name
            self.source = source

            print('[tkSourceSelect] selected:', name, source)

            self.destroy()

    def on_select_other(self, item):
        """TODO: add docstring"""

        name, source = item

        self.item = item
        self.name = name
        self.source = source

        print('[tkSourceSelect] selected:', name, source)

        self.destroy()


class tkCamera(tkinter.Frame):

    def __init__(self, parent, text="", source=0, width=None, height=None, sources=None):
        """TODO: add docstring"""

        super().__init__(parent)

        self.source = source
        self.width  = width
        self.height = height
        self.other_sources = sources

        #self.window.title(window_title)
        self.vid = VideoCapture(self.source, self.width, self.height)

        self.label = tkinter.Label(self, text=text)
        self.label.pack()

        self.canvas = tkinter.Canvas(self, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(self, text="Start", command=self.start)
        self.btn_snapshot.pack(anchor='center', side='left')

        self.btn_snapshot = tkinter.Button(self, text="Stop", command=self.stop)
        self.btn_snapshot.pack(anchor='center', side='left')

        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(self, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(anchor='center', side='left')

        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(self, text="Source", command=self.select_source)
        self.btn_snapshot.pack(anchor='center', side='left')

        # After it is called once, the update method will be automatically called every delay milliseconds
        # calculate delay using `FPS`
        self.delay = int(1000/self.vid.fps)

        print('[tkCamera] source:', self.source)
        print('[tkCamera] fps:', self.vid.fps, 'delay:', self.delay)

        self.image = None

        self.dialog = None

        self.running = True
        self.update_frame()

    def start(self):
        """TODO: add docstring"""

        #if not self.running:
        #    self.running = True
        #    self.update_frame()
        self.vid.start_recording()

    def stop(self):
        """TODO: add docstring"""

        #if self.running:
        #   self.running = False
        self.vid.stop_recording()

    def snapshot(self):
        """TODO: add docstring"""

        # Get a frame from the video source
        #ret, frame = self.vid.get_frame()
        #if ret:
        #    cv2.imwrite(time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg"), cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))

        # Save current frame in widget - not get new one from camera - so it can save correct image when it stoped
        #if self.image:
        #    self.image.save(time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg"))

        self.vid.snapshot()

    def update_frame(self):
        """TODO: add docstring"""

        # widgets in tkinter already have method `update()` so I have to use different name -

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.image = frame
            self.photo = PIL.ImageTk.PhotoImage(image=self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

        if self.running:
            self.after(self.delay, self.update_frame)

    def select_source(self):
        """TODO: add docstring"""

        # open only one dialog
        if self.dialog:
            print('[tkCamera] dialog already open')
        else:
            self.dialog = tkSourceSelect(self, self.other_sources)

            self.label['text'] = self.dialog.name
            self.source = self.dialog.source

            self.vid = MyVideoCapture(self.source, self.width, self.height)

