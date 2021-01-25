    import tkinter
    import tkinter.filedialog
    import cv2
    import PIL.Image, PIL.ImageTk
    import time
    import threading

    class MyVideoCapture:

        def __init__(self, video_source=0, width=None, height=None, fps=None):
        
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
                self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))  # convert float to int

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
            if not self.ret:
                print('[MyVideoCapture] no frame for snapshot')
            else:
                if not filename:
                    filename = time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg")
                    
                if not self.convert_pillow:
                    cv2.imwrite(filename, self.frame)
                else:
                    self.frame.save(filename)
        
        def start_recording(self, filename=None):
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
            if not self.recording:
                print('[MyVideoCapture] not recording')
            else:
                self.recording = False
                self.recording_writer.release() 
                print('[MyVideoCapture] stop recording:', self.recording_filename)
                   
        def record(self, frame):
            # write frame to file         
            if self.recording_writer and self.recording_writer.isOpened():
                self.recording_writer.write(frame)
     
         
        def process(self):
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
            return self.ret, self.frame
        
        # Release the video source when the object is destroyed
        def __del__(self):
            # stop thread
            if self.running:
                self.running = False
                self.thread.join()

            # relase stream
            if self.vid.isOpened():
                self.vid.release()
                
     
    class tkCamera(tkinter.Frame):

        def __init__(self, parent, text="", video_source=0, width=None, height=None):
            super().__init__(parent)
            
            self.video_source = video_source
            self.width  = width
            self.height = height

            #self.window.title(window_title)
            self.vid = MyVideoCapture(self.video_source, self.width, self.height)
                    
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


            print('[tkCamera] source:', self.video_source)
            print('[tkCamera] fps:', self.vid.fps, 'delay:', self.delay)
            
            self.image = None
            
            self.dialog = None
                    
            self.running = True
            self.update_frame()

        def start(self):
            #if not self.running:
            #    self.running = True
            #    self.update_frame()
            self.vid.start_recording()

        def stop(self):
            #if self.running:
            #   self.running = False
            self.vid.stop_recording()
        
        def snapshot(self):
            # Get a frame from the video source
            #ret, frame = self.vid.get_frame()
            #if ret:
            #    cv2.imwrite(time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg"), cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))
            
            # Save current frame in widget - not get new one from camera - so it can save correct image when it stoped
            #if self.image:
            #    self.image.save(time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg"))

            self.vid.snapshot()
                
        def update_frame(self):
            # widgets in tkinter already have method `update()` so I have to use different name -

            # Get a frame from the video source
            ret, frame = self.vid.get_frame()
            
            if ret:
                #self.image = PIL.Image.fromarray(frame)
                self.image = frame
                self.photo = PIL.ImageTk.PhotoImage(image=self.image)
                self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
            
            if self.running:
                self.after(self.delay, self.update_frame)

        def select_source(self):
            # open only one dialog
            if not self.dialog:
                self.dialog = tkinter.Toplevel(self)

                tkinter.Label(self.dialog, text="Sources:").pack(fill='both', expand=True)
                
                for item in sources:
                    name, source = item
                    b = tkinter.Button(self.dialog, text=name, command=lambda data=item:self.on_select(data))
                    b.pack(fill='both', expand=True)
                    
                b = tkinter.Button(self.dialog, text="Open...", command=self.on_select_file)
                b.pack(fill='both', expand=True)
                    
        def on_select(self, item):
            name, source = item
            print('selected:', name, source)

            self.label['text'] = name
            self.video_source = source
            self.vid = MyVideoCapture(self.video_source, self.width, self.height)

            self.dialog.destroy()
            self.dialog = None        

        def on_select_file(self):
            
            result = tkinter.filedialog.askopenfilename(
                                            initialdir=".", 
                                            title="Select video file", 
                                            filetypes=(("AVI files", "*.avi"), ("MP4 files","*.mp4"), ("all files","*.*"))
                                        )
            
            if result:
                self.label['text'] = result.split('/')[-1]
                self.video_source = result
                self.vid = MyVideoCapture(self.video_source, self.width, self.height)

                self.dialog.destroy()
                self.dialog = None        
            
    class App:

        def __init__(self, window, window_title, video_sources):
            self.window = window

            self.window.title(window_title)
            
            self.vids = []

            columns = 2
            for number, source in enumerate(video_sources):
                text, stream = source
                vid = tkCamera(self.window, text, stream, 400, 300)
                x = number % columns
                y = number // columns
                vid.grid(row=y, column=x)
                self.vids.append(vid)
            
            self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.window.mainloop()
        
        def on_closing(self, event=None):
            print('[App] stoping threads')
            for source in self.vids:
                source.vid.running = False
            print('[App] exit')
            self.window.destroy()


    if __name__ == '__main__':     

        sources = [
            ('me', 0), 
            ('Zakopane, Poland', 'https://imageserver.webcamera.pl/rec/krupowki-srodek/latest.mp4'),
            ('Kraków, Poland', 'https://imageserver.webcamera.pl/rec/krakow4/latest.mp4'),
            ('Warszawa, Poland', 'https://imageserver.webcamera.pl/rec/warszawa/latest.mp4'),
            #('Baltic See, Poland', 'https://imageserver.webcamera.pl/rec/chlopy/latest.mp4'),
            #('Mountains, Poland', 'https://imageserver.webcamera.pl/rec/skolnity/latest.mp4'),
            ('recorded', '/home/furas/Pulpit/Python - SO/2021.01/2021.01.24 - cv - tkinter - two cameras/2021.01.25 20.37.50.avi'),
        ]
            
        # Create a window and pass it to the Application object
        App(tkinter.Tk(), "Tkinter and OpenCV", sources)
