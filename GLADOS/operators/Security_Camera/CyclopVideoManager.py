import os
from datetime import datetime
from typing import List, Dict
from Security_Camera.converter_init import Converter
from Security_Camera.CyclopVideoWriter import VideoWriter
import sys
import subprocess
from ffmpeg import video
import shutil
from pathlib import Path
class VideoManager:
    VIDEO_FORMATS = {
        "webm": ".webm",
        "mp4": ".mp4"
    }
    def _root_path(self):
        return os.path.abspath(os.sep)
    
    def _create_root_directory(self):
        self.root_folder = os.path.join(self.root_path,r"CYCLOPSERVERDATA\videos")
        if not os.path.exists(self.root_folder):
            os.makedirs(self.root_folder)

    def __init__(self, video_dir=r"\data\videos"):
        path = sys.path[0]
        video_dir = path + video_dir
        self.video_dir = video_dir
        self.local_video_dir = r"\data\videos"
        self.converter = Converter()
        path2 = Path(path).parent
        self.static_folder = os.path.join(os.path.abspath(os.path.join(path2, os.pardir)),r"GLADOS\operators\website\static\videos")
        self.root_path = self._root_path()
        self._create_root_directory()
    def move_mp4_to_root_folder(self, video_format: str = "mp4"):
        cp_mp4_files = [filename for filename in self._get_all_filenames() if self._is_video_file(filename, video_format)]
        
        for cp in cp_mp4_files:
            current_path = os.path.join(self.video_dir,cp)
            target_path = os.path.join(self.root_folder,cp)
            shutil.move(current_path,target_path )
    def move_webm_to_local_folder(self,video_format: str = "webm"):
        cp_webm_files = [filename for filename in self._get_root_file_names() if self._is_video_file(filename, video_format)]
        for cp in cp_webm_files:
            current_path = os.path.join(self.root_folder,cp)
            target_path = os.path.join(self.video_dir,cp)
            shutil.move(current_path,target_path )
    def move_local_files_to_static_folder(self,video_format: str = "webm"):
        cp_webm_files = [filename for filename in self._get_all_filenames() if self._is_video_file(filename, video_format)]
        for cp in cp_webm_files:
            current_path = os.path.join(self.video_dir,cp)
            target_path = os.path.join(self.static_folder,cp)
            shutil.move(current_path,target_path )
    def convert_to_webm_file(self):
        self.move_mp4_to_root_folder()
        files_local , files_global = self.get_full_video_filenames("mp4")
        print(files_local ,files_global)
        
        for file in files_global:
            file_name = file[:-3]
            if not os.path.exists("{}webm".format(file_name)):
                video.trans_code_modified(input_file=file,width=int(640),height=int(480),crf=5,rate=int(1080),out_file="{}webm".format(file_name))
        self.remove_file(files_local)
        self.move_webm_to_local_folder()
        
        self.remove_file(files_global)
        self.move_local_files_to_static_folder()
    def remove_file(self,files):
        for file in files:
            if file.endswith(".mp4"):
                os.remove(file)
        return True
    
    def remove_directory(self,filepath):
        shutil.rmtree(filepath)
        return True
    def get_video_filenames(self, video_format: str = "webm") -> List[str]:
        file_names = [filename for filename in self._get_all_filenames() if self._is_video_file(filename, video_format)]
        full_file_names = []
        for file in file_names:
            file = os.path.join(self.video_dir,file)
            full_file_names.append(file)

        # Get video timestamps from the filename
        datetimes_to_filenames = {}
        """ for file_name in file_names:
            try:
                name = self._remove_file_type(file_name, self.VIDEO_FORMATS.get(video_format))
            except ValueError:
                continue
            channel, timestamp_iso = name.split(VideoWriter.FILENAME_DELIM)
            video_timestamp = datetime.fromisoformat(timestamp_iso)
            datetimes_to_filenames.update({video_timestamp: file_name})
        # Return sorted list of video files, with most recent video first
        datetimes = list(datetimes_to_filenames.keys())
        datetimes.sort(reverse=True)
        return [datetimes_to_filenames[key] for key in datetimes] """
        return file_names
    def get_static_video_filenames(self, video_format: str = "webm")-> List[str]:
        file_names = [filename for filename in self._get_static_file_names() if self._is_video_file(filename, video_format)]
        full_static_file_names = []
        for file in file_names:
            full_static_file_name = os.path.join(self.static_folder,file)
            full_static_file_names.append(full_static_file_name)
        return file_names , full_static_file_names
    def get_full_video_filenames(self, video_format: str = "mp4") -> List[str]:
        file_names = [filename for filename in self._get_root_file_names() if self._is_video_file(filename, video_format)]
        file_names_local = [filename for filename in self._get_all_filenames() if self._is_video_file(filename, video_format)]
        full_file_names = []
        full_file_names_global = []
        for file in file_names_local:
            file = os.path.join(self.video_dir,file)
            full_file_names.append(file)   
        for file in file_names:
            file_global = os.path.join(self.root_folder,file)
            full_file_names_global.append(file_global)
        return full_file_names , full_file_names_global
    def get_video_filenames_by_date(self, video_format: str = "mp4") -> Dict[str, List[str]]:
        all_filenames = [filename for filename in self._get_all_filenames() if self._is_video_file(filename, video_format)]
        filenames_by_date = {}
        for filename in all_filenames:
            try:
                name = self._remove_file_type(filename)
            except ValueError:
                continue
            channel, timestamp_iso = name.split(VideoWriter.FILENAME_DELIM)
            date = timestamp_iso.split("T")[0]
            if date not in filenames_by_date.keys():
                filenames_by_date[date] = []
            filenames_by_date[date].append(filename)
        return filenames_by_date
    def _get_all_filenames(self) -> List[str]:
        return os.listdir(self.video_dir)   
    def _get_root_file_names(self)-> List[str]:
        return os.listdir(self.root_folder)
    def _get_static_file_names(self) -> List[str]:
        return os.listdir(self.static_folder)
    @staticmethod
    def _is_video_file(filename: str, file_type: str) -> bool:
        return file_type in filename
    @staticmethod
    def _remove_file_type(filename: str, file_type: str) -> str:
        if file_type in filename:
            return filename.replace(file_type, "")
        raise ValueError("File is not a supported file type")