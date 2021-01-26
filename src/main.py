#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: Bartlomiej "furas" Burek (https://blog.furas.pl)
# date: 2021.01.26

import os
import tkinter
from tkCamera import tkCamera


"""TODO: add docstring"""


HOME = os.path.dirname(os.path.abspath(__file__))


class App:
    def __init__(self, parent, title, sources):
        """TODO: add docstring"""

        self.parent = parent

        self.parent.title(title)

        self.stream_widgets = []

        width = 400
        height = 300

        columns = 2
        for number, (text, source) in enumerate(sources):
            widget = tkCamera(self.parent, text, source, width, height, sources)
            row = number // columns
            col = number % columns
            widget.grid(row=row, column=col)
            self.stream_widgets.append(widget)

        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self, event=None):
        """TODO: add docstring"""

        print("[App] stoping threads")
        for widget in self.stream_widgets:
            widget.vid.running = False

        print("[App] exit")
        self.parent.destroy()


if __name__ == "__main__":

    sources = [  # (text, source)
        # local webcams
        ("me", 0),
        # remote videos (or streams)
        (
            "Zakopane, Poland",
            "https://imageserver.webcamera.pl/rec/krupowki-srodek/latest.mp4",
        ),
        ("Kraków, Poland", "https://imageserver.webcamera.pl/rec/krakow4/latest.mp4"),
        (
            "Warszawa, Poland",
            "https://imageserver.webcamera.pl/rec/warszawa/latest.mp4",
        ),
        # ('Baltic See, Poland', 'https://imageserver.webcamera.pl/rec/chlopy/latest.mp4'),
        # ('Mountains, Poland', 'https://imageserver.webcamera.pl/rec/skolnity/latest.mp4'),
        # local files
        # ('2021.01.25 20.37.50.avi', '2021.01.25 20.37.50.avi'),
    ]

    root = tkinter.Tk()
    App(root, "Tkinter and OpenCV", sources)
    root.mainloop()
