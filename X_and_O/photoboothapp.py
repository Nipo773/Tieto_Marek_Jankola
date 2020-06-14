# import the necessary packages
from __future__ import print_function
from XOmodel import train
from PIL import Image
from PIL import ImageTk
import numpy as np
import tkinter as tki
import threading
import datetime
import imutils
import cv2
import os

class PhotoBoothApp:
    def __init__(self, vs, outputPath):
        # store the video stream object and output path, then initialize
    	# the most recently read frame, thread for reading frames, and
    	# the thread stop event
        self.vs = vs
        self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.model = train()
        # initialize the root window and image panel
        self.root = tki.Tk()
        self.panel = None

    	# create a button, that when pressed, will take the current
    	# frame and save it to file
        btn = tki.Button(self.root, text="Snapshot!",
            command=self.takeSnapshot)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10,
            pady=10)
    	# start a thread that constantly pools the video sensor for
    	# the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
    	# set a callback to handle when the window is closed
        self.root.wm_title("PyImageSearch PhotoBooth")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def videoLoop(self):
    	# DISCLAIMER:
    	# I'm not a GUI developer, nor do I even pretend to be. This
    	# try/except statement is a pretty ugly hack to get around
    	# a RunTime error that Tkinter throws due to threading
        try:
    		# keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
    			# grab the frame from the video stream and resize it to
    			# have a maximum width of 300 pixels
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=300)
    	
    			# OpenCV represents images in BGR order; however PIL
    			# represents images in RGB order, so we need to swap
    			# the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
		
    			# if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)
		
    			# otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def takeSnapshot(self):
    	# grab the current timestamp and use it to construct the
    	# output path
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        try:
            os.mkdir("output")
        except OSError:
            print ("Creation of the directory %s failed" % "output")

        p = os.path.sep.join(("output", filename))
    	# save the file
        cv2.imwrite(p, self.frame.copy())
        image = np.array(Image.open("output/" + filename).resize((28,28)))
        image = image.reshape(1,28,28,3)
        pred = np.argmax(self.model.predict(image), axis=1)

        if pred[0] == 1:
            print("There is X in the photo")
            label = tki.Label(self.root, text= "There is X in the photo")
            #this creates a new label to the GUI
            label.pack() 
        else:
            print("There is O in the photo")
            label = tki.Label(self.root, text= "There is O in the photo")
            #this creates a new label to the GUI
            label.pack() 
        
        print("[INFO] saved {}".format(filename))
    def onClose(self):
    	# set the stop event, cleanup the camera, and allow the rest of
    	# the quit process to continue
    	print("[INFO] closing...")
    	self.stopEvent.set()
    	self.vs.stop()
    	self.root.quit()

