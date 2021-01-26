#!/usr/bin/env python

# author: Bartlomiej "furas" Burek (https://blog.furas.pl)
# date: 2021.01.26

import time
import threading
import cv2
import PIL.Image


"""TODO: add docstring"""


class VideoCapture:

    def __init__(self, video_source=0, width=None, height=None, fps=None):
        """TODO: add docstring"""

        self.video_source = video_source
        self.width = width
        self.height = height
        self.fps = fps

        self.running = False

        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("[MyVideoCapture] Unable to open video source", video_source)

        # Get video source width and height
        if not self.width:
            self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))    # convert float to int
        if not self.height:
            self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))  # convert float to int
        if not self.fps:
            self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))              # convert float to int

        # default value at start
        self.ret = False
        self.frame = None

        self.convert_color = cv2.COLOR_BGR2RGB
        #self.convert_color = cv2.COLOR_BGR2GRAY
        self.convert_pillow = True

        # default values for recording
        self.recording = False
        self.recording_filename = 'output.mp4'
        self.recording_writer = None

        # start thread
        self.running = True
        self.thread = threading.Thread(target=self.process)
        self.thread.start()

    def snapshot(self, filename=None):
        """TODO: add docstring"""

        if not self.ret:
            print('[MyVideoCapture] no frame for snapshot')
        else:
            if not filename:
                filename = time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg")

            if not self.convert_pillow:
                cv2.imwrite(filename, self.frame)
                print('[MyVideoCapture] snapshot (using cv2):', filename)
            else:
                self.frame.save(filename)
                print('[MyVideoCapture] snapshot (using pillow):', filename)

    def start_recording(self, filename=None):
        """TODO: add docstring"""

        if self.recording:
            print('[MyVideoCapture] already recording:', self.recording_filename)
        else:
            # VideoWriter constructors
            #.mp4 = codec id 2
            if filename:
                self.recording_filename = filename
            else:
                self.recording_filename = time.strftime("%Y.%m.%d %H.%M.%S", time.localtime()) + ".avi"
            #fourcc = cv2.VideoWriter_fourcc(*'I420') # .avi
            #fourcc = cv2.VideoWriter_fourcc(*'MP4V') # .avi
            fourcc = cv2.VideoWriter_fourcc(*'MP42') # .avi
            #fourcc = cv2.VideoWriter_fourcc(*'AVC1') # error libx264
            #fourcc = cv2.VideoWriter_fourcc(*'H264') # error libx264
            #fourcc = cv2.VideoWriter_fourcc(*'WRAW') # error --- no information ---
            #fourcc = cv2.VideoWriter_fourcc(*'MPEG') # .avi 30fps
            #fourcc = cv2.VideoWriter_fourcc(*'MJPG') # .avi
            #fourcc = cv2.VideoWriter_fourcc(*'XVID') # .avi
            #fourcc = cv2.VideoWriter_fourcc(*'H265') # error


            self.recording_writer = cv2.VideoWriter(self.recording_filename, fourcc, self.fps, (self.width, self.height))
            self.recording = True
            print('[MyVideoCapture] started recording:', self.recording_filename)

    def stop_recording(self):
        """TODO: add docstring"""

        if not self.recording:
            print('[MyVideoCapture] not recording')
        else:
            self.recording = False
            self.recording_writer.release()
            print('[MyVideoCapture] stop recording:', self.recording_filename)

    def record(self, frame):
        """TODO: add docstring"""

        # write frame to file
        if self.recording_writer and self.recording_writer.isOpened():
            self.recording_writer.write(frame)

    def process(self):
        """TODO: add docstring"""

        while self.running:
            ret, frame = self.vid.read()

            if ret:
                # process image
                frame = cv2.resize(frame, (self.width, self.height))

                # it has to record before converting colors
                if self.recording:
                    self.record(frame)

                if self.convert_pillow:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = PIL.Image.fromarray(frame)
            else:
                print('[MyVideoCapture] stream end:', self.video_source)
                # TODO: reopen stream
                self.running = False
                if self.recording:
                    self.stop_recording()
                break

            # assign new frame
            self.ret = ret
            self.frame = frame

            # sleep for next frame
            time.sleep(1/self.fps)

    def get_frame(self):
        """TODO: add docstring"""

        return self.ret, self.frame

    # Release the video source when the object is destroyed
    def __del__(self):
        """TODO: add docstring"""

        # stop thread
        if self.running:
            self.running = False
            self.thread.join()

        # relase stream
        if self.vid.isOpened():
            self.vid.release()

