# EEE 111 Project
# Nicolas Faller, Jr.
# 2018 - 08343

# This program emulates the facial recognition
# capabilities of Snapchat, wherein a user
# may apply "filters" on the webcam feed

# Import necessary libraries
import cv2 # Webcam display
import face_recognition # Face recognition
import math # Mathematical solutions

## CLASSES ##

# "Filter" class for building multiple filters
class Filter:
    def __init__(self, name, part):
        self.name = name
        self.path = "filters/"+name+".png"
        self.part = part
    def name(self):
        return self.name
    def path(self):
        return self.path
    def part(self):
        return self.part
    def overlay(self, frame, x, y, w, ontop=True):
        filt = cv2.imread(self.path, -1)
        (filt, yf) = adjust(filt, w, y, ontop)
        frame = draw(frame, filt, x, yf)

## FUNCTIONS ##

# The "draw" function overlays the filter on to the frame
def draw(frame, filt, x0, y0):
    (h, w) = (filt.shape[0], filt.shape[1])
    (hframe, wframe) = (frame.shape[0], frame.shape[1])

    if y0 + h >= hframe:
        filt = filt[0:hframe-y0,:,:]
    if x0 + w >= wframe:
        filt = filt[:,0:wframe-x0,:]
    if x0 < 0:
        filt = filt[:,abs(x0)::,:]
        w = filt.shape[1]
        x0 = 0
    for c in range(3):
        frame[y0 : y0+h, x0: x0+w, c] = \
                filt[:,:,c] * (filt[:,:,3]/255.0) + frame[y0 : y0+h, x0: x0+w, c] * (1.0 - filt[:,:,3]/255.0)
    return frame

# The "adjust" function adjusts the size of the filter
def adjust(filt, hw, hy, ontop = True):
    (hfilt, wfilt) = (filt.shape[0], filt.shape[1])
    factor = hw/wfilt
    filt = cv2.resize(filt, (0,0), fx=factor, fy=factor)
    (hfilt, wfilt) = (filt.shape[0], filt.shape[1])

    yo = hy - hfilt if ontop else hy
    if yo < 0:
        filt = filt[abs(yo)::,:,:]
    return(filt, yo)

# Determines the "boundaries" (size) of face
def facebound(frame):
    facebounds = face_recognition.face_locations(frame)
    for bound in facebounds:
        x = bound[3]
        y = bound[0]
        w = bound[1]-bound[3]
        h = bound[2]-bound[0]
        return (x, y, w, h)

# Main loop
def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (0,0), fx=0.75, fy=0.75)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
            time.sleep(1)
            cap.release()
            cv2.destroyAllWindows

        if facebound(frame) != None:
            x, y, w, h = facebound(frame)
            equations = Filter("equations", "head")
            equations.overlay(frame, x, y, w)
        
        cv2.imshow("Input", frame)

## MAIN PROGRAM ##

main()
