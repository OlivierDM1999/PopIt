from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
import cv2
import numpy as np



class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
    def __del__(self):
        self.cap.release()
    def get_frame(self):
        ret, frame = self.cap.read()
        frame_flip = cv2.flip(frame, 1)
        ret, frame = cv2.imencode('.jpg', frame_flip)

        return frame.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_stream(request):
    video_object=gen(VideoCamera())
    return StreamingHttpResponse(video_object,
                    content_type='multipart/x-mixed-replace; boundary=frame')



def index(request): 
    return render(request,"hello.html")


def game(request):
    return render(request,"game.html")



