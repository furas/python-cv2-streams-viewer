import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

class MyVideoCapture:

    def __init__(self, video_source=0, width=None, height=None):
    
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = width
        self.height = height
    
        # Get video source width and height
        if not self.width:
            self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))    # convert float to int
        if not self.height:
            self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))  # convert float to int

        self.ret = False
        self.frame = None

    def process(self):
        ret = False
        frame = None
        
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                frame = cv2.resize(frame, (self.width, self.height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        self.ret = ret
        self.frame = frame
        
        
    def get_frame(self):
        self.process()
        return self.ret, self.frame
    
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
 
 
class tkCamera(tkinter.Frame):

    def __init__(self, window, video_source=0, width=None, height=None):
        super().__init__(window)
        
        self.window = window
        
        #self.window.title(window_title)
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source, width, height)

        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()
         
        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor='center', expand=True)
         
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update_widget()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    
    def update_widget(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        
        if ret:
            self.image = PIL.Image.fromarray(frame)
            self.photo = PIL.ImageTk.PhotoImage(image=self.image)
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        
        self.window.after(self.delay, self.update_widget)


class App:

    def __init__(self, window, window_title, video_sources):
        self.window = window

        self.window.title(window_title)
        
        self.vids = []
        
        for source in video_sources:
            vid = tkCamera(window, source, 400, 300)
            vid.pack()
            self.vids.append(vid)
        
        # Create a canvas that can fit the above video source size
         
        self.window.mainloop()
    
if __name__ == '__main__':     

    sources = [
        0, 
        #'https://imageserver.webcamera.pl/rec/krupowki-srodek/latest.mp4',
        #'https://imageserver.webcamera.pl/rec/skolnity/latest.mp4',
        'https://imageserver.webcamera.pl/rec/krakow4/latest.mp4',
    ]
    
        
    # Create a window and pass it to the Application object
    App(tkinter.Tk(), "Tkinter and OpenCV", sources)
