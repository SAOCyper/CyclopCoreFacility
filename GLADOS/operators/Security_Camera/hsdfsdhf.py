import cv2 ,sys , datetime , os
from CyclopVideoWriter import VideoWriter
cam = cv2.VideoCapture(0)
date = datetime.datetime.now()
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
WRITERPATH = sys.path[0]
WRITERPATH = WRITERPATH + r"\data\videos"
filename = "0" + "__" + date.strftime("%Y-%m-%d_%H-%M-%S")
full_filepath = WRITERPATH + r"\{}".format(filename) 
""" full_filepath = os.path.join(WRITERPATH, filename) """
mp4_file = full_filepath + ".mp4"
videoWriter = cv2.VideoWriter(mp4_file,fourcc, int(15),(640,480))
while True:
    ret , _frame = cam.read()
    if ret:
        videoWriter.write(_frame)
    else:
        break
    cv2.imshow('frame',_frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
videoWriter.release
cam.release()