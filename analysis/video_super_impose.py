### Super Impose Video Frames:
# %% -------------------------------- Import Lib -------------------------------- %% #
import cv2
import numpy as np


from matplotlib import pyplot as plt
# %% ------------------------------- SUPER IMPOSE -------------------------------- %% #
# ours:
from utils.uwarl_util import create_all_folders

def image_histogram_equalization(image, number_bins=256):
    # from http://www.janeriksolem.net/histogram-equalization-with-python-and.html

    # get image histogram
    image_histogram, bins = np.histogram(image.flatten(), number_bins, density=True)
    cdf = image_histogram.cumsum() # cumulative distribution function
    cdf = (number_bins-1) * cdf / cdf[-1] # normalize

    # use linear interpolation of cdf to find new pixel values
    image_equalized = np.interp(image.flatten(), bins[:-1], cdf)

    return image_equalized.reshape(image.shape), cdf
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
        
    def super_impose(
        self, 
        filename:str, 
        if_skip_sampling:bool, 
        file_type:str=".mov", 
        if_fwd:bool=False, 
    ):
        intermediate_output_path_ = self._create_subfolder(filename)
        file_path_ = f"{self._video_dir}/{filename}{file_type}"
        frame_count_  = self._sample_frames(file_path_, intermediate_output_path_, if_skip_sampling=if_skip_sampling)
        out_image_ = self._impose_frames_from_directory(filename, frame_count_, intermediate_output_path_, self._output_dir, if_fwd=if_fwd)
        return out_image_
        
    #Extract frames from video into a folder
    def _sample_frames(self, file_path, intermediate_folder, 
        if_skip_sampling=False,
        methods="MOG2", # methods in ["sub", "MOG2"]
        if_floor_filter = False,
        t_offset = 0,
    ):
        vCap = cv2.VideoCapture(file_path)
        frame_count = 1
        tick = 0
        N_frames = vCap.get(cv2.CAP_PROP_FRAME_COUNT)
        indices_ = list(range(t_offset, int(N_frames), int(self._gap))) + [N_frames]
        N_samples = len(indices_)
        print("N_frames:",N_frames, " N_samples:", N_samples)
        
        if if_skip_sampling:
            return N_samples
            
        # - apply initial empty bkg: 
        path_bkg = f"{intermediate_folder}/../background_cropped.png"
        frame_bkg = cv2.imread(path_bkg)
        # - prep bkg subtraction:
        if methods == "MOG2":
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
            fgbg = cv2.createBackgroundSubtractorMOG2()
            fgmask = fgbg.apply(frame_bkg)
        else:
            background_gray = cv2.cvtColor(frame_bkg, cv2.COLOR_BGR2GRAY)
        if if_floor_filter:
            lower_color = np.array([78, 5, 150])
            upper_color = np.array([138, 8, 176])

        mask_ = None
        for i in indices_:
            vCap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret,frame = vCap.read()
            if ret:
                path_frame = f"{intermediate_folder}/frame_{frame_count}.png"
                path_frame2 = f"{intermediate_folder}/de_frame_{frame_count}.png"
                # frame = frame[0:900, 340:1800]
                frame = frame[0:987, 0:1600]
                cv2.imwrite(path_frame,frame)
                frame_count += 1 
                if methods == "MOG2":
                    fgmask = fgbg.apply(frame)
                    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
                    cv2.imwrite(path_frame2, fgmask)
                    mask_new_ = cv2.imread(path_frame2, cv2.IMREAD_UNCHANGED)
                else:
                    image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    diff = cv2.absdiff(background_gray, image_gray)
                    threshold_value = 30
                    _, mask_new_ = cv2.threshold(diff, threshold_value, 255, cv2.THRESH_BINARY)
                if if_floor_filter:
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    mask = cv2.inRange(hsv, lower_color, upper_color)
                    plt.figure(); plt.imshow(mask);
                    mask_inverse = cv2.bitwise_not(mask)
                    mask_new_ = cv2.bitwise_and(mask_new_, mask_inverse)
                # create cumulated masks:
                if mask_ is not None:
                    mask_ = mask_ + mask_new_
                else:
                    mask_ = mask_new_
            else:
                break 

        vCap.release()
        cv2.destroyAllWindows()
        # save cumulated masks:
        if mask_ is not None:
            path_frame = f"{intermediate_folder}/cumulated_de_frames.png"
            cv2.imwrite(path_frame, mask_)
        return frame_count

    def _impose_frames_from_directory(self, 
        filename, frame_count, 
        inter_folder, output_dir,
        t_start = 1,
        if_cropping = True,
        if_fwd = False,
        fg_alpha=[0.5,0.5],
        alpha=[0.2,0.8],
    ):
        tag = "_fwd" if if_fwd else ""
        output_file_name_ = f"{output_dir}/super_{filename}{tag}.png"
        print(f"Super Imposing {frame_count} frames..")
        img_base_ = None
        if frame_count > 2:
            items = range(t_start+1, frame_count, 1) if if_fwd else range(frame_count-1, t_start, -1)
            for i in items:
                print(">>> Overlapping frame:", i)
                try:
                    img_new_ = cv2.imread(f"{inter_folder}/frame_{i}.png", cv2.IMREAD_UNCHANGED)
                    mask_new_ = cv2.imread(f"{inter_folder}/de_frame_{i}.png", cv2.IMREAD_UNCHANGED)
                    _, mask_new_ = cv2.threshold(mask_new_, 5, 255, cv2.THRESH_BINARY)

                    print(img_new_.shape)
                    print(mask_new_.shape)
                    # img_new_[:,:,0], _ = image_histogram_equalization(img_new_[:,:,0])
                    # img_new_[:,:,1], _ = image_histogram_equalization(img_new_[:,:,1])
                    # img_new_[:,:,2], _ = image_histogram_equalization(img_new_[:,:,2])
                    # background
                    # img_background_ = cv2.imread(f"{inter_folder}/frame_{i}.png")
                    # img_new_[:,:,:3] = img_new_[:,:,:3] + img_background_[:,:,:3] * 0.1
                    # img_new_ = img_new_.astype(np.float32)/255.0
                    if img_base_ is not None:
                        # - apply mask:
                        fg = cv2.bitwise_and(img_new_, img_new_, mask=mask_new_)
                        fg_orig = cv2.bitwise_and(img_base_, img_base_, mask=mask_new_)
                        fg = cv2.addWeighted(fg_orig, fg_alpha[0], fg, fg_alpha[1], 0.2) # lets blend instead of overriding
                        plt.figure(); plt.imshow(fg);
                        mask_inv_ = cv2.bitwise_not(mask_new_)
                        bk = cv2.bitwise_and(img_base_, img_base_, mask=mask_inv_)
                        plt.figure(); plt.imshow(bk);
                        
                        # combine foreground+background
                        img_base_ = cv2.bitwise_or(fg, bk)
                    else:
                        img_base_ = img_new_
                        # img_base_ = (img_base_.astype(np.float32) * 0.9).astype(np.uint8)
                        
                    #     # base:
                    #     img_base_ = cv2.imread(f"{inter_folder}/frame_1.png", cv2.IMREAD_UNCHANGED)
                    #     img_base_ = cv2.cvtColor(img_base_, cv2.COLOR_RGB2RGBA)
                    #     img_base_ = img_base_.astype(np.float32)/255.0
                except:
                    raise("Error opening images! Abort!")
            
            # histogram:
            if 0:
                img_base_[:,:,0], _ = image_histogram_equalization(img_base_[:,:,0])
                img_base_[:,:,1], _ = image_histogram_equalization(img_base_[:,:,1])
                img_base_[:,:,2], _ = image_histogram_equalization(img_base_[:,:,2])
                img_base_[:,:,3], _ = image_histogram_equalization(img_base_[:,:,3])
            
            # Blending:
            index = items[-1]
            img_base_0 = cv2.imread(f"{inter_folder}/frame_{index}.png")
            print(np.max(img_base_0))
            print(np.max(img_base_))
            img_base_ = cv2.addWeighted(img_base_0, alpha[0], img_base_, alpha[1], 0)
            
            
            plt.figure()
            plt.imshow(img_base_)
            # Next we stack our equalized channels back into a single image
            if if_cropping:
                img_base_ = img_base_[:, 200:] # cropping
            cv2.imwrite(output_file_name_, img_base_)
        
        return output_file_name_
        
        
# % ------------------------------- MAIN ----------------------------
# king_ = VideoSuperMan(
#     video_dir="/Users/jaku/Desktop/demo_record",
#     output_dir="/Users/jaku/Desktop/demo_record/output",
#     gap = 120
# )

# LIST_VIDEO_FILES = [
#     # "Demo_1207_UD_OCC3",
#     "Demo_1213_Clips_LR_FWD",
#     "Demo_1213_Clips_LR_RVR",
#     "Demo_1213_Clips_LR_SPI",
#     "Demo_1213_Clips_LR_CIR",
#     "Demo_1213_Clips_LR_SQR",
#     "Demo_1213_Clips_LR_TRI",
#     "Demo_1213_Clips_LR_BEE",
#     "Demo_1213_Clips_UD_FWD",
#     "Demo_1213_Clips_UD_RVR",
#     "Demo_1213_Clips_UD_SPI",
#     "Demo_1213_Clips_UD_CIR",
#     "Demo_1213_Clips_UD_SQR",
#     "Demo_1213_Clips_UD_TRI",
#     "Demo_1213_Clips_UD_BEE",
#     "Demo_1213_Clips_H_FWD",
#     "Demo_1213_Clips_H_RVR",
#     "Demo_1213_Clips_H_SPI",
#     "Demo_1213_Clips_H_CIR",
#     "Demo_1213_Clips_H_SQR",
#     "Demo_1213_Clips_H_TRI",
#     "Demo_1213_Clips_H_BEE",
#     "Demo_1213_Clips_FIX_D",
#     "Demo_1213_Clips_FIX_U",
#     "Demo_1213_Clips_FIX_E",
# ]
king_ = VideoSuperMan(
    video_dir="/Users/jaku/JX-Platform/Github_Research/dual-vins-data/demo_record/video_1127",
    output_dir="/Users/jaku/JX-Platform/Github_Research/dual-vins-data/demo_record/video_1127/output",
    gap = 60
)

LIST_VIDEO_FILES = [
    "Demo_1127_Clips_UD_FWD",
    "Demo_1127_Clips_UD_RVR",
    "Demo_1127_Clips_UD_CIR",
    "Demo_1127_Clips_UD_CIR2",
    "Demo_1127_Clips_UD_BEE",
    "Demo_1127_Clips_UD_BEE2",
    "Demo_1127_Clips_UD_SQR",
    "Demo_1127_Clips_UD_TRI",
]
for file in LIST_VIDEO_FILES:
    print(" === Processing:", file, " === ")
    path = king_.super_impose(filename=file, file_type=".mp4", if_skip_sampling=False, if_fwd=False)
    print(">>> Generated @", path)


# %%