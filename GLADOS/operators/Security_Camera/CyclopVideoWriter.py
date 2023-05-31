from typing import Tuple
import cv2 , sys,os,time,datetime

class VideoWriter:
    FILENAME_DELIM = "__"
    
    def __init__(self, channel: str, path=None,
                 resolution: Tuple[int, int] = (640, 480)):
        WRITERPATH = sys.path[0]
        WRITERPATH = WRITERPATH + r"\data\videos"
        path = WRITERPATH
        self.channel = channel
        self.video_dir = path
        self.full_filepath = None
        #self._generate_file_name()
        self._make_target_dir(path)
        
        self.fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
        self.resolution = resolution
        self.frame_buffer = []
        self.first_frame_time = time.monotonic()
        self.create_writer()

    def create_writer(self):
        self._generate_file_name()
        self.mp4_file = self.full_filepath + ".mp4"
        self.writer = cv2.VideoWriter(self.mp4_file, self.fourcc, int(30), self.resolution)
        return self.writer
    @staticmethod
    def _make_target_dir(path: str):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def add_frame(self, frame):
        resized_frame = cv2.resize(frame, self.resolution)
        if not self.frame_buffer:
            self.first_frame_time = time.monotonic()
        self.frame_buffer.append(resized_frame)
    
    def write(self):
        #self._generate_file_name()
        print("Writing video to: " + self.full_filepath + " ...")
        fps = self._calculate_fps()
        # Write to .webm

        # Write to .mp4
        mp4_file = self.full_filepath + ".mp4"
        for frame in self.frame_buffer:
            self.writer.write(frame)
        self.writer.release()
        del self.writer
        self._clear_frame_buffer()

    def reset(self):
        self._clear_frame_buffer()
        self.first_frame_time = time.monotonic()

    def _clear_frame_buffer(self):
        self.frame_buffer = []

    def _generate_file_name(self):
        date = datetime.datetime.now()
        filename = self.channel + self.FILENAME_DELIM + date.strftime("%Y-%m-%d_%H-%M-%S")
        self.full_filepath = os.path.join(self.video_dir, filename)

    def _calculate_fps(self) -> int:
        elapsed_time = time.monotonic() - self.first_frame_time
        return int(len(self.frame_buffer) / elapsed_time)