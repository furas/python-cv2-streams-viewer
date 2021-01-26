# python-cv2-streams-viewer

Program uses `cv2` to display many streams from cameras, web pages, local files. 

It uses `thread` to process stream from `cv2`. 

It can record stream to local file. 

It uses `tkinter` to display it.

---


![image](https://raw.githubusercontent.com/furas/python-cv2-streams-viewer/main/screenshots/screenshot_2021-01-25_15-22-51.png)

![image](https://raw.githubusercontent.com/furas/python-cv2-streams-viewer/main/screenshots/screenshot_2021-01-26_00-39-13.png)


---

### Notes:

It started as answer for question on Stackoverflow: [How display multi videos with threading using tkinter in python?](https://stackoverflow.com/questions/65876044/how-display-multi-videos-with-threading-using-tkinter-in-python/)


See similar idea on blog `pyImageSearch` in [Increasing webcam FPS with Python and OpenCV](https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/). 

It creates class

```
 from imutils.video import WebcamVideoStream
```

---

**2021.01.26**

Code from single file `main.py` splited into files `videocapture.py`, `tkCamera.py`, `main.py` and moved to folder `src`.
