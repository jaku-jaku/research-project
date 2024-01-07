### Super Impose Video Frames:
# %% -------------------------------- Import Lib -------------------------------- %% #
import cv2
import os
from PIL import Image
import numpy as np


# %% ------------------------------- SUPER IMPOSE -------------------------------- %% #
# ours:
from utils.uwarl_util import create_all_folders

class VideoSuperMan:
    _video_dir  :str = ""
    _output_dir :str = ""
    _gap  = 120 # every X frames
    
    def __init__(self, video_dir, output_dir, gap):
        self._video_dir = video_dir
        self._output_dir = output_dir
        self._gap = gap
    
    def _create_subfolder(self, folder_name):
        path = f"{self._output_dir}/{folder_name}"
        create_all_folders(path)
        return path
        
    def super_impose(self, filename, file_type=".mov"):
        intermediate_output_path_ = self._create_subfolder(filename)
        file_path_ = f"{self._video_dir}/{filename}{file_type}"
        frame_count_  = self._sample_frames(file_path_, intermediate_output_path_)
        out_image_ = self._impose_frames_from_directory(filename, frame_count_, intermediate_output_path_, self._output_dir)
        return out_image_
        
    #Extract frames from video into a folder
    def _sample_frames(self, file_path, intermediate_folder, if_static_salient=False):
        vCap = cv2.VideoCapture(file_path)
        frame_count = 1
        tick = 0
        N_frames = vCap.get(cv2.CAP_PROP_FRAME_COUNT)
        indices_ = range(0, int(N_frames), int(self._gap))
        N_samples = len(indices_)
        print("N_frames:",N_frames, " N_samples:", N_samples)
        
        sa = None
        for i in indices_:
            vCap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret,frame = vCap.read()
            if ret:
                if if_static_salient:
                    sa = cv2.saliency.StaticSaliencyFineGrained_create()
                    (success, saliencyMap) = sa.computeSaliency(frame)
                    print("success:", success)
                    saliencyMap = (saliencyMap * 255).astype("uint8")
                    threshMap = cv2.threshold(saliencyMap, 0, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                    frame_rgba = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
                    frame_rgba[:, :, 3] = threshMap
                    
                    print(f"Exporting frame {i}..")
                    cv2.imwrite(f'{intermediate_folder}/frame_{frame_count}.png',frame_rgba)
                    cv2.imwrite(f'{intermediate_folder}/saliency_{frame_count}.jpg',threshMap)
                    frame_count += 1 
                else:
                    cv2.imwrite(f'{intermediate_folder}/frame_{frame_count}.png',frame)
                    frame_count += 1 
            else:
                break 

        vCap.release()
        cv2.destroyAllWindows()
        return frame_count

    def _impose_frames_from_directory(self, filename, frame_count, inter_folder, output_dir):
        output_file_name_ = f"{output_dir}/super_{filename}.png"
        print(f"Super Imposing {frame_count} frames..")
        alpha = 1.0
        if frame_count > 1:
            for i in range(1, frame_count):
                print(">>> Overlapping frame:", i)
                try:
                    img_new_ = cv2.imread(f"{inter_folder}/frame_{i}.png", cv2.IMREAD_UNCHANGED)
                    if i > 1:
                        # alpha_ = alpha_/2 + alpha_base
                        # Alpha factor
                        # rgb_channels = img_new_[:, :, 0:3]
                        # alpha_channel = img_new_[:, :,  3]
                        # alpha_factor = alpha_channel[:,:,np.newaxis].astype(np.float32) / 255.0
                        # alpha_factor = np.concatenate((alpha_factor,alpha_factor,alpha_factor), axis=2)
                        # base = rgb_channels.astype(np.float32) * alpha_factor
                        img_base_ = img_base_ + 0.5 * img_new_
                        alpha += 0.5
                    else:
                        # base:
                        img_base_ = img_new_
                except:
                    raise("Error opening images! Abort!")
            cv2.imwrite(output_file_name_, img_base_/alpha)
        
        return output_file_name_
        
        
# % ------------------------------- MAIN ----------------------------
king_ = VideoSuperMan(
    video_dir="/Users/jaku/Desktop/demo_record",
    output_dir="/Users/jaku/Desktop/demo_record/output",
    gap = 120
)

LIST_VIDEO_FILES = [
    "Demo_1207_UD_OCC3",
    "Demo_1213_Clips_LR_FWD",
    "Demo_1213_Clips_LR_RVR",
    "Demo_1213_Clips_LR_SPI",
    "Demo_1213_Clips_LR_CIR",
    "Demo_1213_Clips_LR_SQR",
    "Demo_1213_Clips_LR_TRI",
    "Demo_1213_Clips_UD_FWD",
    "Demo_1213_Clips_UD_RVR",
    "Demo_1213_Clips_UD_SPI",
    "Demo_1213_Clips_UD_CIR",
    "Demo_1213_Clips_UD_SQR",
    "Demo_1213_Clips_UD_TRI",
]
for file in LIST_VIDEO_FILES:
    print(" === Processing:", file, " === ")
    path = king_.super_impose(filename=file, file_type=".mp4")
    print(">>> Generated @", path)

